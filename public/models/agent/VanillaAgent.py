"""The Vanilla Agent"""

import numpy as np
import tensorflow as tf
import tensorflow.contrib.slim as slim

from public.models.agent.Agent import Agent
from public.util.dijkstra import build_graph_from_state, dijkstra
from public.util.path import move_to, path_to


class VanillaAgent(Agent):
    """The Vanilla Agent"""

    def __init__(self, state, experience=None, lr=1e-4, a_size=5, h_size=200):  # all these are optional ?
        super(VanillaAgent, self).__init__('vanilla-debug', state, experience)

        # These lines established the feed-forward part of the network. The agent takes a state and produces an action.
        self.state_in = tf.placeholder(shape=[None, state.local_size], dtype=tf.float32)

        hidden = slim.fully_connected(self.state_in, h_size, activation_fn=tf.nn.relu)

        self.policy = slim.fully_connected(hidden, a_size, activation_fn=tf.nn.softmax)
        self.predict = tf.argmax(self.policy, 1)

        # The next six lines establish the training proceedure. We feed the reward and predict into the network
        # to compute the loss, and use it to update the network.
        self.reward_holder = tf.placeholder(shape=[None], dtype=tf.float32)
        self.action_holder = tf.placeholder(shape=[None], dtype=tf.int32)

        self.indexes = tf.range(0, tf.shape(self.policy)[0]) * tf.shape(self.policy)[1] + self.action_holder
        self.responsible_outputs = tf.gather(tf.reshape(self.policy, [-1]), self.indexes)
        if experience is not None:
            loss = -tf.reduce_mean(tf.log(self.responsible_outputs) * self.reward_holder)

            self.tvars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope=tf.get_variable_scope().name)
            self.gradients = tf.gradients(loss, self.tvars)

            self.gradient_holders = []
            for idx in range(len(self.tvars)):
                placeholder = tf.placeholder(tf.float32, name=str(idx) + '_holder')
                self.gradient_holders.append(placeholder)

            global_vars = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, 'global')
            optimizer = tf.train.AdamOptimizer(learning_rate=lr)

            self.update_global = optimizer.apply_gradients(zip(self.gradient_holders, global_vars))  # self.tvars

    def get_policy(self, sess, state):
        return sess.run(self.policy, feed_dict={self.state_in: [state.reshape(-1)]})

    def get_policies(self, sess, game_state):
        policies = np.zeros(game_state[0].shape + (5,))
        for (y, x), k in np.ndenumerate(game_state[0]):
            if k == 1:
                policies[y][x] = self.get_policy(sess, self.state.get_local_and_normalize(game_state, x, y))
        return policies

    def choose_action(self, sess, state, train=True):
        # Here the state is normalized !
        if train:  # keep randomness
            a_dist = sess.run(self.policy, feed_dict={self.state_in: [state.reshape(-1)]})
            a = np.random.choice(a_dist[0], p=a_dist[0])
            a = np.argmax(a_dist == a)
        else:  # act greedily
            a = sess.run(self.predict, feed_dict={self.state_in: [state.reshape(-1)]})
        return a

    def choose_actions(self, sess, game_state, train=True):
        """Choose all actions using one call to tensorflow"""
        g = build_graph_from_state(game_state[0])
        dist_dict, closest_dict = dijkstra(g.g, 0)
        all_game_state_n = np.array([]).reshape(0, self.state.local_size)
        moves = np.zeros_like(game_state[0], dtype=np.int64) - 1
        moves_2 = np.zeros_like(game_state[0], dtype=np.int64) - 1
        moves_where = []
        for (y, x), k in np.ndenumerate(game_state[0]):
            if k == 1:
                if (y, x) in dist_dict and dist_dict[(y, x)] in [1, 2]:
                    moves_where += [(y, x)]
                    game_state_n = self.state.get_local_and_normalize(game_state, x, y).reshape(1,
                                                                                                self.state.local_size)
                    all_game_state_n = np.concatenate((all_game_state_n, game_state_n), axis=0)
                else:
                    if game_state[1][y][x] > 10:  # Set a minimum strength
                        y_t, x_t = y, x
                        y_t, x_t = closest_dict[(y_t, x_t)]
                        # while closest_dict[(y_t,x_t)]!=0: Pbbly unnecessary
                        #     y_t, x_t = closest_dict[(y_t, x_t)]
                        moves_2[y][x] = move_to(path_to((x, y), (x_t, y_t), len(game_state[0][0]), len(game_state[0])))
        if train:
            actions = sess.run(self.policy, feed_dict={self.state_in: all_game_state_n})
            actions = [np.argmax(action == np.random.choice(action, p=action)) for action in actions]
        else:
            actions = sess.run(self.predict, feed_dict={self.state_in: all_game_state_n})
        for (y, x), d in zip(moves_where, actions):
            moves[y][x] = d
        return moves, moves_2

    def update_agent(self, sess):
        states, moves, rewards = self.experience.batch()

        feed_dict = {self.state_in: states,
                     self.action_holder: moves,
                     self.reward_holder: rewards}
        grads = sess.run(self.gradients, feed_dict=feed_dict)
        feed_dict = dict(zip(self.gradient_holders, grads))
        _ = sess.run(self.update_global, feed_dict=feed_dict)
