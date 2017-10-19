"""The reward.py file to compute the reward"""
import numpy as np

from public.hlt import NORTH, EAST, SOUTH, WEST
from train.reward.util import get_prod


class Reward:
    """The reward class"""

    def __init__(self, state, discount_factor=0.6):
        self.discount_factor = discount_factor
        self.state = state

    def raw_rewards_function(self, game_states):
        return np.array(
            [0.1 * np.power(get_prod(game_states[i + 1]) - get_prod(game_states[i]), 2)
             for i in range(len(game_states) - 1)])

    def individual_states_and_rewards(self, game_state, move, discounted_reward):
        """Self-explanatory"""
        states = []
        moves = []
        rewards = []

        for (y, x), k in np.ndenumerate(game_state[0]):
            if k == 1 and move[y][x] != -1:
                states += [self.state.get_local_and_normalize(game_state, x, y)]
                moves += [move[y][x]]
                rewards += [discounted_reward[y][x]]
        return states, moves, rewards

    def discounted_reward_function(self, next_reward, move_before, strength_before, discount_factor=1.0):
        """Self-explanatory"""
        reward = np.zeros_like(next_reward)

        def take_value(matrix, x, y):
            return np.take(np.take(matrix, x, axis=1, mode='wrap'), y, axis=0, mode='wrap')

        for (y, x), d in np.ndenumerate(move_before):
            if d != -1:
                dy = (-1 if d == NORTH else 1) if (d == SOUTH or d == NORTH) else 0
                dx = (-1 if d == WEST else 1) if (d == WEST or d == EAST) else 0
                reward[y][x] = discount_factor * take_value(next_reward, x + dx, y + dy) \
                    if strength_before[y][x] >= take_value(strength_before, x + dx, y + dy) \
                    else 0
        return reward

    def discounted_rewards_function(self, game_states, moves):
        """Self-explanatory"""
        raw_rewards = self.raw_rewards_function(game_states)
        discounted_rewards = np.zeros_like(raw_rewards, dtype=np.float64)
        running_reward = np.zeros_like(raw_rewards[0], dtype=np.float64)
        for t, (raw_reward, move, game_state) in reversed(list(enumerate(zip(raw_rewards, moves, game_states)))):
            running_reward = self.discounted_reward_function(running_reward, move, game_state[1],
                                                             discount_factor=self.discount_factor) + \
                             self.discounted_reward_function(raw_reward, move, game_state[1])
            discounted_rewards[t] = running_reward - 0.01
        return discounted_rewards

    def all_individual_states_and_rewards(self, game_states, moves, discounted_rewards):
        """Self-explanatory"""
        all_states = []
        all_moves = []
        all_rewards = []
        for game_state, move, discounted_reward in zip(game_states, moves, discounted_rewards):
            states_, moves_, rewards_ = self.individual_states_and_rewards(
                game_state, move, discounted_reward)
            all_states += states_
            all_moves += moves_
            all_rewards += rewards_
        return np.array(all_states), np.array(all_moves), np.array(all_rewards)

    def all_rewards_function(self, game_states, moves):
        discounted_rewards = self.discounted_rewards_function(game_states, moves)
        return self.all_individual_states_and_rewards(game_states[:-1], moves, discounted_rewards)
