"""
Experience class definition
"""
import numpy as np

from train.reward.util import production_increments_function


class Experience:
    """
    Experience class to store moves, rewards and metric values
    """

    def __init__(self):
        self.moves = np.array([])
        self.rewards = np.array([])

        self.metric = np.array([])

    def add_episode(self, game_states, moves):
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

    def __init__(self, reward):
        super(ExperienceVanilla, self).__init__()
        self.reward = reward
        self.states = np.array([]).reshape(0, self.reward.state.local_size)

    def add_episode(self, game_states, moves):
        self.compute_metric(game_states)
        all_states, all_moves, all_rewards = self.reward.all_rewards_function(game_states, moves)

        self.states = np.concatenate((self.states, all_states.reshape(-1, self.reward.state.local_size)), axis=0)
        self.moves = np.concatenate((self.moves, all_moves))
        self.rewards = np.concatenate((self.rewards, all_rewards))

    def batch(self, size=128):
        indices = np.random.randint(len(self.states), size=min(int(len(self.states) / 2), size))
        return self.states[indices], self.moves[indices], self.rewards[indices]
