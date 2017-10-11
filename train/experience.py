"""
Experience class definition
"""
import os

import numpy as np

from train.reward.util import production_increments_function


class Experience:
    """
    Experience class to store moves, rewards and metric values
    """

    def __init__(self, max_size=10000, min_size=5000):
        self.max_size = max_size
        self.min_size = min_size
        self.moves = np.array([])
        self.rewards = np.array([])

        self.metric = np.array([])

    def add_episode(self, game_states, all_states, all_moves, all_rewards):
        pass

    def batch(self, size):
        pass

    def compute_metric(self, game_states):
        production_increments = production_increments_function(game_states)
        self.metric = np.append(self.metric, production_increments.dot(np.linspace(2.0, 1.0, num=len(game_states) - 1)))

    def save_metric(self, name):
        np.save(name, self.metric)


class ExperienceVanilla(Experience):
    """
    Stores states in addition to the inherited attributes of Experience
    """

    def __init__(self, s_size, name):
        super(ExperienceVanilla, self).__init__()
        self.s_size = s_size
        self.states = np.array([]).reshape(0, s_size)
        try:
            self.metric = np.load(os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..'))
                                  + '/public/models/variables/' + name + '/'
                                  + name + '.npy')
        except FileNotFoundError:
            print("Metric file not found")
            self.metric = np.array([])

    def add_episode(self, game_states, all_states, all_moves, all_rewards):
        self.compute_metric(game_states)

        self.states = np.concatenate((self.states, all_states.reshape(-1, self.s_size)), axis=0)
        self.moves = np.concatenate((self.moves, all_moves))
        self.rewards = np.concatenate((self.rewards, all_rewards))
        if len(self.states) >= self.max_size:
            self.resize()

    def resize(self):
        self.states = self.states[self.min_size:]
        self.moves = self.moves[self.min_size:]
        self.rewards = self.rewards[self.min_size:]

    def batch(self, size=128):
        indices = np.random.randint(len(self.states), size=min(int(len(self.states) / 2), size))
        return self.states[indices], self.moves[indices], self.rewards[indices]
