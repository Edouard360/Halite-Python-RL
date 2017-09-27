"""
Tests the reward function
"""
from train.reward import discount_rewards
import unittest

import numpy as np


class TestReward(unittest.TestCase):
    def test_length_discount_rewards(self):
        self.assertTrue(len(discount_rewards(np.array([1]))) == 1)
        self.assertTrue(len(discount_rewards(np.array([1, 3]))) == 2)


if __name__ == '__main__':
    unittest.main()
