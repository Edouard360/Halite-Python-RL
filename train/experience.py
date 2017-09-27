"""
Experience class definition
"""
import numpy as np

from train.reward import allRewards, rawRewards


class Experience:
    """
    Experience class to store moves, rewards and metric values
    """
    def __init__(self):
        self.moves = np.array([])
        self.rewards = np.array([])

        self.metric = np.array([])

    def add_episode(self, game_states, moves):
        # moves is not used here, kept for inheritance reasons
        # TODO Edouard to act on this
        # pylint: disable=W0612,W0613
        production_increments = np.sum(np.sum(rawRewards(game_states), axis=2), axis=1)
        self.metric = np.append(self.metric, production_increments.dot(np.linspace(2.0, 1.0, num=len(game_states) - 1)))

    def batch(self, size):
        pass

    def save_metric(self, name):
        np.save(name, self.metric)


class ExperienceVanilla(Experience):
    """
    Stores states in addition to the inherited attributes of Experience
    """
    def __init__(self):
        super(ExperienceVanilla, self).__init__()
        self.states = np.array([]).reshape(0, 27)

    def add_episode(self, game_states, moves):
        super(ExperienceVanilla, self).add_episode(game_states, moves)
        all_states, all_moves, all_rewards = allRewards(game_states, moves)

        self.states = np.concatenate((self.states, all_states.reshape(-1, 27)), axis=0)
        self.moves = np.concatenate((self.moves, all_moves))
        self.rewards = np.concatenate((self.rewards, all_rewards))

    def batch(self, size=128):
        indices = np.random.randint(len(self.states), size=min(int(len(self.states) / 2), size))
        return self.states[indices], self.moves[indices], self.rewards[indices]
