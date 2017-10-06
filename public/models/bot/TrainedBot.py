"""The Trained Bot"""
import os

import tensorflow as tf

from public.models.agent.VanillaAgent import VanillaAgent
from public.models.bot.Bot import Bot
from train.reward import format_moves, get_game_state


class TrainedBot(Bot):
    """The trained bot"""

    def __init__(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        tf.reset_default_graph()

        with tf.device("/cpu:0"):
            with tf.variable_scope('global'):
                self.agent = VanillaAgent()

        global_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='global')
        saver = tf.train.Saver(global_variables)
        init = tf.global_variables_initializer()

        self.sess = tf.Session()
        self.sess.run(init)
        try:
            saver.restore(self.sess, os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..'))
                          + '/variables/' + self.agent.name + '/'
                          + self.agent.name)
        except FileNotFoundError:
            print("Model not found - initiating new one")

    def compute_moves(self, game_map):
        """Compute the moves given a game_map"""
        game_state = get_game_state(game_map, self.my_id)
        return format_moves(game_map, self.agent.choose_actions(self.sess, game_state, debug=True))

    def get_policies(self, game_state):
        """Compute the policies given a game_state"""
        return self.agent.get_policies(self.sess, game_state)

    def close(self):
        """Close the tensorflow session"""
        self.sess.close()
