"""The Agent general class"""
import os

import numpy as np

from train.reward import local_state_from_global, normalize_game_state


class Agent:
    """The Agent general class"""

    def __init__(self, name, experience):
        self.name = name
        self.experience = experience
        if self.experience is not None:
            try:
                self.experience.metric = np.load(os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '..'))
                                                 + '/variables/' + self.name + '/'
                                                 + self.name + '.npy')
            except FileNotFoundError:
                print("Metric file not found")
                self.experience.metric = np.array([])

    def get_policies(self, sess, game_state):
        policies = np.zeros(game_state[0].shape + (5,))
        for y in range(len(game_state[0])):
            for x in range(len(game_state[0][0])):
                if game_state[0][y][x] == 1:
                    policies[y][x] = self.get_policy(sess,
                                                     normalize_game_state(local_state_from_global(game_state, x, y)))
        return policies

    def get_policy(self, sess, state):
        pass

    def choose_actions(self, sess, game_state, debug=False):
        # Here the state is not yet normalized !
        moves = np.zeros_like(game_state[0], dtype=np.int64) - 1
        for y in range(len(game_state[0])):
            for x in range(len(game_state[0][0])):
                if game_state[0][y][x] == 1:
                    moves[y][x] = self.choose_action(sess,
                                                     normalize_game_state(local_state_from_global(game_state, x, y)),
                                                     debug=debug)
        return moves

    def choose_action(self, sess, state, frac_progress=1.0, debug=False):
        pass

    def update_agent(self, sess):
        pass
