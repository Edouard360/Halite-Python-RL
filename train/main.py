"""This main.py file runs the training."""
import os
import sys
import threading

import tensorflow as tf
from tensorflow.python.framework.errors_impl import InvalidArgumentError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from public.models.strategy.TrainedStrategy import TrainedStrategy
    from train.worker import Worker
except:
    raise

port = int(sys.argv[1]) if len(sys.argv) > 1 else 2000

strategy = TrainedStrategy(tf_scope='global')

num_workers = 1
n_simultations = 10

workers = []
if num_workers > 1:
    for i in range(num_workers):
        workers.append(Worker(port, i, TrainedStrategy(tf_scope='worker_' + str(i))))
else:
    workers.append(Worker(port, 0, strategy))
# We need only to save the global
global_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='global')
saver = tf.train.Saver(global_variables)
init = tf.global_variables_initializer()

# Launch the tensorflow graph
with tf.Session() as sess:
    sess.run(init)
    try:
        saver.restore(sess, os.path.abspath(
            os.path.dirname(__file__)) + '/../public/models/variables/' + strategy.name + '/' + strategy.name)
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
