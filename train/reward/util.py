"""Useful for computing the rewards"""
import numpy as np


def discount_rewards(r, gamma=0.8):
    """ take 1D float array of rewards and compute discounted reward """
    discounted_r = np.zeros_like(r, dtype=np.float64)
    running_add = 0
    for t in reversed(range(0, r.size)):
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r


def get_total_prod(game_state):
    return np.sum(game_state[0] * game_state[2])


def get_prod(game_state):
    return game_state[0] * game_state[2]


def get_total_strength(game_state):
    return np.sum(game_state[0] * game_state[1])


def get_strength(game_state):
    return game_state[0] * game_state[1]


def get_total_number(game_state):
    return np.sum(game_state[0])


def production_increments_function(game_states):
    return np.array([get_total_prod(game_states[i + 1]) - get_total_prod(game_states[i])
                     for i in range(len(game_states) - 1)])
