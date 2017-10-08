"""
Tests the reward function
"""
import unittest

import numpy as np

from public.state.state import State1
from tests.util import game_states_from_url
from train.experience import ExperienceVanilla
from train.reward.reward import Reward
from train.reward.util import discount_rewards
from train.worker import Worker


class TestReward(unittest.TestCase):
    """
    Tests the reward function
    """

    def test_length_discount_rewards(self):
        """
        Test the length of the discount reward
        """
        self.assertTrue(len(discount_rewards(np.array([1]))) == 1)
        self.assertTrue(len(discount_rewards(np.array([1, 3]))) == 2)

    def test_reward(self):
        """
        Test the length of the discount reward
        """
        game_url = 'https://s3.eu-central-1.amazonaws.com/halite-python-rl/hlt-games/trained-bot.hlt'
        game_states, moves = game_states_from_url(game_url)

        r = Reward(State1())
        raw_rewards = r.raw_rewards_function(game_states)
        self.assertTrue(len(raw_rewards) == len(game_states) - 1)

        all_states, all_moves, all_rewards = r.all_rewards_function(game_states, moves)
        self.assertTrue(len(all_states) >= len(game_states) - 1)
        self.assertTrue(len(all_moves) >= len(moves))
        self.assertTrue(len(all_rewards) == len(all_moves) and len(all_states) == len(all_moves))
        experience = ExperienceVanilla(r)
        experience.add_episode(game_states, moves)
        experience.add_episode(game_states, moves)
        self.assertTrue(len(experience.moves) == 2 * len(all_moves))
        batch_states, batch_moves, batch_rewards = experience.batch()
        self.assertTrue(len(batch_rewards) == len(batch_moves) and len(batch_states) == len(batch_moves))

    def test_worker(self):
        """
        Test if the worker port initiate and terminate with good port
        """
        worker = Worker(2000, 2, None)
        self.assertTrue(worker.port == 2002)
        worker.p.terminate()


if __name__ == '__main__':
    unittest.main()
