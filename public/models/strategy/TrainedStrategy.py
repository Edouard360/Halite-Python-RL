"""The Trained Bot"""
import json
import os
import warnings

import numpy as np
import tensorflow as tf
from tensorflow.python.framework.errors_impl import InvalidArgumentError

from public.hlt import format_moves
from public.models.agent.VanillaAgent import VanillaAgent
from public.models.strategy.Strategy import Strategy
from public.state.state import get_game_state, State1
from public.util.dijkstra import build_graph_from_state, dijkstra
from public.util.path import move_to, path_to
from train.experience import ExperienceVanilla
from train.reward.reward import Reward


class TrainedStrategy(Strategy):
    """The trained strategy"""

    def __init__(self, tf_scope='global'):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
        tf.reset_default_graph()
        warnings.filterwarnings("ignore")

        config = open(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../strategy.json'))).read()
        config = json.loads(config)
        self.name = config["saving_name"]
        self.state = State1(scope=config["agent"]["scope"])
        self.reward = Reward(state=self.state)
        self.experience = ExperienceVanilla(self.state.local_size, self.name)
        with tf.variable_scope(tf_scope):
            self.agent1 = VanillaAgent(s_size=self.state.local_size, h_size=config["agent"]["h_size"])

    def init_session(self, sess=None, saver=None):
        if sess is None:
            global_variables = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='global')
            self.saver = tf.train.Saver(global_variables)
            init = tf.global_variables_initializer()
            self.sess = tf.Session()
            self.sess.run(init)
            try:
                self.saver.restore(self.sess, os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '..'))
                                   + '/variables/' + self.name + '/'
                                   + self.name)
            except InvalidArgumentError:
                print("Model not found - initiating new one")
        else:
            self.sess = sess
            self.saver = saver

    def set_id(self, my_id):
        super(TrainedStrategy, self).set_id(my_id)
        self.agent1_moves = []
        self.agent1_game_states = []

    def compute_moves(self, game_map, train=False):
        """Compute the moves given a game_map"""
        game_state = get_game_state(game_map, self.my_id)
        g = build_graph_from_state(game_state[0])
        dist_dict, closest_dict = dijkstra(g.g, 0)
        self.agent1_game_states += [game_state]
        self.agent1_moves += [np.zeros_like(game_state[0], dtype=np.int64) - 1]
        self.agent1_local_game_states = np.array([]).reshape(0, self.state.local_size)
        dijkstra_moves = np.zeros_like(game_state[0], dtype=np.int64) - 1
        agent1_positions = []
        for (y, x), k in np.ndenumerate(game_state[0]):
            if k == 1:
                if (y, x) in dist_dict and dist_dict[(y, x)] in [1, 2]:
                    agent1_positions += [(y, x)]
                    game_state_n = self.state.get_local_and_normalize(game_state, x, y).reshape(1,
                                                                                                self.state.local_size)
                    self.agent1_local_game_states = np.concatenate((self.agent1_local_game_states, game_state_n),
                                                                   axis=0)
                else:
                    if game_state[1][y][x] > 10:  # Set a minimum strength
                        y_t, x_t = y, x
                        y_t, x_t = closest_dict[(y_t, x_t)]
                        dijkstra_moves[y][x] = move_to(
                            path_to((x, y), (x_t, y_t), len(game_state[0][0]), len(game_state[0])))
        actions = self.agent1.choose_actions(self.sess, self.agent1_local_game_states, train)
        for (y, x), d in zip(agent1_positions, actions):
            self.agent1_moves[-1][y][x] = d

        return format_moves(game_map, -(self.agent1_moves[-1] * dijkstra_moves))

    def add_episode(self):
        all_states, all_moves, all_rewards = self.reward.all_rewards_function(self.agent1_game_states,
                                                                              self.agent1_moves)
        self.experience.add_episode(self.agent1_game_states, all_states, all_moves, all_rewards)

    def update_agent(self):
        train_states, train_moves, train_rewards = self.experience.batch()
        self.agent1.update_agent(self.sess, train_states, train_moves, train_rewards)

    def save(self):
        directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) + '/variables/' + self.name
        if not os.path.exists(directory):
            print("Creating directory named :" + self.name)
            os.makedirs(directory)
        self.saver.save(self.sess, directory + '/' + self.name)
        self.experience.save_metric(directory + '/' + self.name)

    def get_policies(self, game_states):
        policies = []
        for game_state in game_states:
            policies += [np.zeros(game_state[0].shape + (5,))]
            for (y, x), k in np.ndenumerate(game_state[0]):
                if k == 1:
                    policies[-1][y][x] = self.agent1.get_policy(
                        self.sess, self.state.get_local_and_normalize(game_state, x, y))
        return np.array(policies)

    def close(self):
        """Close the tensorflow session"""
        self.sess.close()
