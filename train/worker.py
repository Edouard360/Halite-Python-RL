"""The worker class for training and parallel operations"""
import multiprocessing
import time

import tensorflow as tf

from networking.hlt_networking import HLT
from networking.start_game import start_game


def update_target_graph(from_scope, to_scope):
    from_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, from_scope)
    to_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, to_scope)

    op_holder = []
    for from_var, to_var in zip(from_vars, to_vars):
        op_holder.append(to_var.assign(from_var))
    return op_holder


class Worker:
    """
    The Worker class for training. Each worker has an individual port, number, and agent.
    Each of them work with the global session, and use the global saver.
    """

    def __init__(self, port, number, strategy):
        self.name = 'worker_' + str(number)
        self.number = number
        self.port = port + number

        def worker():
            start_game(self.port, quiet=True, max_game=-1, width=25, height=25, max_turn=50,
                       max_strength=60)  # Infinite games

        self.p = multiprocessing.Process(target=worker)
        self.p.start()
        time.sleep(1)

        self.hlt = HLT(port=self.port)  # Launching the pipe operation

        self.strategy = strategy
        self.update_local_ops = update_target_graph('global', self.name)

    def work(self, sess, saver, n_simultations):
        """
        Using the pipe operation launched at initialization,
        the worker works `n_simultations` games to train the
        agent
        :param sess: The global session
        :param n_simultations: Number of max simulations to run.
        Afterwards the process is stopped.
        :return:
        """
        self.strategy.init_session(sess, saver)
        with sess.as_default(), sess.graph.as_default():
            for i in range(n_simultations):  # while not coord.should_stop():
                if i % 10 == 1 and self.number == 0:
                    print("Simulation: " + str(i))  # self.port)
                sess.run(self.update_local_ops)  # GET THE WORK DONE FROM OTHER
                print("This is one simulation")
                my_id, game_map = self.hlt.get_init()
                self.hlt.send_init("MyPythonBot")
                self.strategy.set_id(my_id)
                while True:
                    get_map_and_play = self.hlt.get_string()
                    if get_map_and_play != 'Get map and play!':
                        print(get_map_and_play)
                        break
                    game_map.get_frame(self.hlt.get_string())
                    self.hlt.send_frame(self.strategy.compute_moves(game_map, train=True))
                self.strategy.add_episode()
                self.strategy.update_agent()

                if self.number == 0:
                    self.strategy.save()
        self.p.terminate()
