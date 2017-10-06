"""The reward.py file to compute the reward"""
import numpy as np
from public.hlt import NORTH, EAST, SOUTH, WEST, Move

STRENGTH_SCALE = 255
PRODUCTION_SCALE = 10


def get_game_state(game_map, my_id):
    game_state = np.reshape(
        [[(square.owner == my_id) + 0, square.strength, square.production] for square in game_map],
        [game_map.height, game_map.width, 3])
    return np.swapaxes(np.swapaxes(game_state, 2, 0), 1, 2)


def normalize_game_state(game_state):
    return game_state / np.array([1, STRENGTH_SCALE, PRODUCTION_SCALE])[:, np.newaxis, np.newaxis]


def get_game_prod(game_state):
    return np.sum(game_state[0] * game_state[2])


def get_strength(game_state):
    return np.sum(game_state[0] * game_state[1])
    # np.sum([square.strength for square in game_map if square.owner == my_id])


def get_number(game_state):
    return np.sum(game_state[0])
    # np.sum([square.strength for square in game_map if square.owner == my_id])


def discount_rewards(r, gamma=0.8):
    """ take 1D float array of rewards and compute discounted reward """
    discounted_r = np.zeros_like(r, dtype=np.float64)
    running_add = 0
    for t in reversed(range(0, r.size)):
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r


def take_surrounding_square(game_state, x, y, size=1):
    return np.take(np.take(game_state, range(y - size, y + size + 1), axis=1, mode='wrap'),
                   range(x - size, x + size + 1), axis=2, mode='wrap')


def local_state_from_global(game_state, x, y, size=1):
    # TODO: for now we still take a square, but a more complex shape could be better.
    return np.take(np.take(game_state, range(y - size, y + size + 1), axis=1, mode='wrap'),
                   range(x - size, x + size + 1), axis=2, mode='wrap')


def raw_rewards_metric(game_states):
    return np.array([game_states[i + 1][0] * game_states[i + 1][2] - game_states[i][0] * game_states[i][2]
                     for i in range(len(game_states) - 1)])


def raw_rewards_function(game_states):
    return np.array(
        [0.0001 * np.power(game_states[i + 1][0] * game_states[i + 1][2] - game_states[i][0] * game_states[i][2], 4)
         for i in range(len(game_states) - 1)])


def strength_rewards(game_states):
    return np.array([(get_strength(game_states[i + 1]) - get_strength(game_states[i]))
                     for i in range(len(game_states) - 1)])


def discounted_reward_function(next_reward, move_before, strength_before, discount_factor=1.0):
    """
    Given all the below arguments, return the discounted reward.
    :param next_reward:
    :param move_before:
    :param strength_before:
    :param discount_factor:
    :return:
    """
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


def discounted_rewards_function(game_states, moves):
    """
    Compute height*width matrices of rewards - not yet individualized
    :param game_states: The list of game states
    :param moves: The list of moves
    :return:
    """
    raw_rewards = raw_rewards_function(game_states)
    # strength_rewards = strength_rewards(game_states)
    discounted_rewards = np.zeros_like(raw_rewards, dtype=np.float64)
    running_reward = np.zeros_like(raw_rewards[0], dtype=np.float64)
    for t, (raw_reward, move, game_state) in reversed(list(enumerate(zip(raw_rewards, moves, game_states)))):
        running_reward = discounted_reward_function(running_reward, move, game_state[1],
                                                    discount_factor=0.6) + \
                         discounted_reward_function(raw_reward, move, game_state[1])
        discounted_rewards[t] = running_reward
    return discounted_rewards


def individual_states_and_rewards(game_state, move, discounted_reward):
    """
    Return the triplet states, moves, rewards for each of the square in one frame.
    :param game_state: One game state - still a 3*3*3 matrix
    :param move: The move for the given square
    :param discounted_reward: The global matrix of discounted reward at time t,
    from we we extract one frame
    :return:
    """
    states = []
    moves = []
    rewards = []
    for y in range(len(game_state[0])):
        for x in range(len(game_state[0][0])):
            if game_state[0][y][x] == 1:
                states += [normalize_game_state(local_state_from_global(game_state, x, y))]
                moves += [move[y][x]]
                rewards += [discounted_reward[y][x]]
    return states, moves, rewards


def all_individual_states_and_rewards(game_states, moves, discounted_rewards):
    all_states = []
    all_moves = []
    all_rewards = []
    for game_state, move, discounted_reward in zip(game_states, moves, discounted_rewards):
        states_, moves_, rewards_ = individual_states_and_rewards(game_state, move, discounted_reward)
        all_states += states_
        all_moves += moves_
        all_rewards += rewards_
    return np.array(all_states), np.array(all_moves), np.array(all_rewards)


def all_rewards_function(game_states, moves):
    # game_states n+1, moves n
    discounted_rewards = discounted_rewards_function(game_states, moves)
    return all_individual_states_and_rewards(game_states[:-1], moves, discounted_rewards)


def format_moves(game_map, moves):
    moves_to_send = []
    for y in range(len(game_map.contents)):
        for x in range(len(game_map.contents[0])):
            if moves[y][x] != -1:
                moves_to_send += [Move(game_map.contents[y][x], moves[y][x])]
    return moves_to_send
