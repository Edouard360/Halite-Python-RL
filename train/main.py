import multiprocessing
import sys
import threading

import tensorflow as tf

from public.models.agent.vanillaAgent import VanillaAgent
from train.experience import ExperienceVanilla
from train.worker import Worker

port = int(sys.argv[1]) if len(sys.argv) > 1 else 2000

tf.reset_default_graph()  # Clear the Tensorflow graph.

with tf.device("/cpu:0"):
    lr = 1e-3;
    s_size = 9 * 3;
    a_size = 5;
    h_size = 50

    with tf.variable_scope('global'):
        master_experience = ExperienceVanilla()
        master_agent = VanillaAgent(master_experience, lr, s_size, a_size, h_size)

    num_workers = 1  # multiprocessing.cpu_count()# (2)  Maybe set max number of workers / number of available CPU threads
    n_simultations = 15

    workers = []
    if num_workers > 1:
        for i in range(num_workers):
            with tf.variable_scope('worker_' + str(i)):
                experience = ExperienceVanilla()
                agent = VanillaAgent(experience, lr, s_size, a_size, h_size)
                workers.append(Worker(port, i, agent))
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
        saver.restore(sess, '../public/models/variables/' + master_agent.name+'/'+master_agent.name)
    except Exception:
        print("Model not found - initiating new one")

    coord = tf.train.Coordinator()
    worker_threads = []
    print("I'm the main thread running on CPU #%s" % multiprocessing.current_process().name)

    if (num_workers == 1):
        workers[0].work(sess, coord, saver, n_simultations)
    else:
        for worker in workers:
            worker_work = lambda: worker.work(sess, coord, saver, n_simultations)
            t = threading.Thread(target=(worker_work))  # Process instead of threading.Thread multiprocessing.Process
            t.start()
            worker_threads.append(t)
        coord.join(worker_threads)
