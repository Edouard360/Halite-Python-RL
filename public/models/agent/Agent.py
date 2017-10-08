"""The Agent general class"""
import os

import numpy as np
import tensorflow as tf
from tensorflow.python.framework.errors_impl import InvalidArgumentError


class Agent:
    """The Agent general class"""

    def __init__(self, name, state, experience):
        self.name = name
        self.experience = experience
        self.state = state
        if self.experience is not None:
            try:
                self.experience.metric = np.load(os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '..'))
                                                 + '/variables/' + self.name + '/'
                                                 + self.name + '.npy')
            except FileNotFoundError:
                print("Metric file not found")
                self.experience.metric = np.array([])

    def choose_actions(self, sess, state, frac_progress=1.0, debug=False):
        pass

    def update_agent(self, sess):
        pass


def start_agent(agent_class, state):
    """Start and return a tf session and its corresponding agent"""
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
    tf.reset_default_graph()

    with tf.device("/cpu:0"):
        with tf.variable_scope('global'):
            agent = agent_class(state)

    global_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='global')
    saver = tf.train.Saver(global_variables)
    init = tf.global_variables_initializer()

    sess = tf.Session()
    sess.run(init)
    try:
        saver.restore(sess, os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..'))
                      + '/variables/' + agent.name + '/'
                      + agent.name)
    except InvalidArgumentError:
        print("Model not found - initiating new one")
    return sess, agent
