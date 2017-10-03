from public.models.agent.vanillaAgent import VanillaAgent
from public.models.bot.bot import Bot
from train.reward import formatMoves, getGameState
import tensorflow as tf
import os


class TrainedBot(Bot):
    def __init__(self):
        lr = 1e-3;
        s_size = 9 * 3;
        a_size = 5;
        h_size = 50
        tf.reset_default_graph()

        with tf.device("/cpu:0"):
            with tf.variable_scope('global'):
                self.agent = VanillaAgent(None, lr, s_size, a_size, h_size)

        global_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='global')
        saver = tf.train.Saver(global_variables)
        init = tf.global_variables_initializer()

        self.sess = tf.Session()
        self.sess.run(init)
        try:
            saver.restore(self.sess, os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                                  '..')) + '/variables/' + self.agent.name + '/' + self.agent.name)
        except Exception:
            print("Model not found - initiating new one")

    def compute_moves(self, game_map):
        game_state = getGameState(game_map, self.myID)
        return formatMoves(game_map, self.agent.choose_actions(self.sess, game_state))

    def get_policies(self, game_state):
        # Warning this is not hereditary
        return self.agent.get_policies(self.sess, game_state)

    def close(self):
        self.sess.close()
