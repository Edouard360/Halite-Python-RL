import multiprocessing
import subprocess
import time

import tensorflow as tf

from networking.hlt_networking import HLT
from train.reward import getGameState, formatMoves


def update_target_graph(from_scope, to_scope):
    from_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, from_scope)
    to_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, to_scope)

    op_holder = []
    for from_var, to_var in zip(from_vars, to_vars):
        op_holder.append(to_var.assign(from_var))
    return op_holder


class Worker():
    def __init__(self, port, number, agent):
        self.name = 'worker_' + str(number)
        self.number = number
        self.port = port + number

        def worker():
            subprocess.call(['./networking/runGameDebugConfig.sh', str(self.port)])  # runSimulation

        self.p = multiprocessing.Process(target=worker)
        self.p.start()
        time.sleep(1)

        self.hlt = HLT(port=self.port)
        self.agent = agent

        self.update_local_ops = update_target_graph('global', self.name)

    def work(self, sess, coord, saver, n_simultations):
        print("Starting worker " + str(self.number))

        with sess.as_default(), sess.graph.as_default():
            for i in range(n_simultations):  # while not coord.should_stop():
                if (i % 10 == 1 and self.number == 0):
                    print("Simulation: " + str(i))  # self.port)
                sess.run(self.update_local_ops)  # GET THE WORK DONE FROM OTHER
                myID, game_map = self.hlt.get_init()
                self.hlt.send_init("MyPythonBot")

                moves = []
                game_states = []
                while (self.hlt.get_string() == 'Get map and play!'):
                    game_map.get_frame(self.hlt.get_string())
                    game_states += [getGameState(game_map, myID)]
                    moves += [self.agent.choose_actions(sess, game_states[-1])]
                    self.hlt.send_frame(formatMoves(game_map, moves[-1]))

                self.agent.experience.add_episode(game_states, moves)
                self.agent.update_agent(sess)

                if self.number == 0:
                    saver.save(sess, './public/models/' + self.agent.name)
                    self.agent.experience.save_metric('./public/models/' + self.agent.name)

        self.p.terminate()
