"""This main.py file runs the training."""
import os
import sys
import threading

import tensorflow as tf
from tensorflow.python.framework.errors_impl import InvalidArgumentError

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from public.models.agent.VanillaAgent import VanillaAgent
    from public.state.state import State1
    from train.experience import ExperienceVanilla
    from train.worker import Worker
    from train.reward.reward import Reward
except:
    raise

port = int(sys.argv[1]) if len(sys.argv) > 1 else 2000

tf.reset_default_graph()  # Clear the Tensorflow graph.

with tf.device("/cpu:0"):
    with tf.variable_scope('global'):
        state = State1(scope=2)
        master_experience = ExperienceVanilla(Reward(state))
        master_agent = VanillaAgent(state, master_experience)

    num_workers = 8
    n_simultations = 5000

    workers = []
    if num_workers > 1:
        for i in range(num_workers):
            with tf.variable_scope('worker_' + str(i)):
                state = State1(scope=2)
                experience = ExperienceVanilla(Reward(state))
                workers.append(Worker(port, i, VanillaAgent(state, experience)))
    else:
        workers.append(Worker(port, 0, master_agent))
    # We need only to save the global
    global_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='global')
    saver = tf.train.Saver(global_variables)
    init = tf.global_variables_initializer()

# Launch the tensorflow graph
with tf.Session() as sess:
    sess.run(init)
    try:
        saver.restore(sess, os.path.abspath(
            os.path.dirname(__file__)) + '/../public/models/variables/' + master_agent.name + '/' + master_agent.name)
    except InvalidArgumentError:
        print("Model not found - initiating new one")

    coord = tf.train.Coordinator()
    worker_threads = []
    print("I'm the main thread running on CPU")

    if num_workers == 1:
        workers[0].work(sess, saver, n_simultations)
    else:
        for worker in workers:
            worker_work = lambda worker=worker: worker.work(sess, saver, n_simultations)
            t = threading.Thread(target=(worker_work))  # Process instead of threading.Thread multiprocessing.Process
            t.start()
            worker_threads.append(t)
        coord.join(worker_threads)
