import numpy as np
from public.hlt import NORTH, EAST, SOUTH, WEST, STILL, Move

STRENGTH_SCALE = 255
PRODUCTION_SCALE = 10


def getGameState(game_map, myID):
    game_state = np.reshape(
        [[(square.owner == myID) + 0, square.strength, square.production] for square in game_map],
        [game_map.width, game_map.height, 3])
    return np.swapaxes(np.swapaxes(game_state, 2, 0), 1, 2)


def normalizeGameState(game_state):
    return game_state / np.array([1, STRENGTH_SCALE, PRODUCTION_SCALE])[:, np.newaxis, np.newaxis]


def getGameProd(game_state):
    return np.sum(game_state[0] * game_state[2])


def getStrength(game_state):
    return np.sum(game_state[0] * game_state[1])
    # np.sum([square.strength for square in game_map if square.owner == myID])


def getNumber(game_state):
    return np.sum(game_state[0])
    # np.sum([square.strength for square in game_map if square.owner == myID])


def discount_rewards(r, gamma=0.8):
    """ take 1D float array of rewards and compute discounted reward """
    discounted_r = np.zeros_like(r, dtype=np.float64)
    running_add = 0
    for t in reversed(range(0, r.size)):
        running_add = running_add * gamma + r[t]
        discounted_r[t] = running_add
    return discounted_r


def localStateFromGlobal(game_state, x, y, size=1):
    # TODO: for now we still take a square, but a more complex shape could be better.
    return np.take(np.take(game_state, range(y - size, y + size + 1), axis=1, mode='wrap'),
                   range(x - size, x + size + 1), axis=2, mode='wrap')


def rawRewards(game_states):
    return np.array([game_states[i + 1][0] * game_states[i + 1][2] - game_states[i][0] * game_states[i][2]
                     for i in range(len(game_states) - 1)])


def strengthRewards(game_states):
    return np.array([(getStrength(game_states[i + 1]) - getStrength(game_states[i]))
                     for i in range(len(game_states) - 1)])


def discountedReward(next_reward, move_before, strength_before, discount_factor=1.0):
    reward = np.zeros_like(next_reward)

    def take_value(matrix, x, y):
        return np.take(np.take(matrix, x, axis=1, mode='wrap'), y, axis=0, mode='wrap')

    for y in range(len(reward)):
        for x in range(len(reward[0])):
            d = move_before[y][x]
            if d != -1:
                dy = (-1 if d == NORTH else 1) if (d == SOUTH or d == NORTH) else 0
                dx = (-1 if d == WEST else 1) if (d == WEST or d == EAST) else 0
                discount_factor = discount_factor if (d != STILL or discount_factor == 1.0) else 0.9
                reward[y][x] = discount_factor * take_value(next_reward, x + dx, y + dy) if strength_before[y][
                                                                                                x] >= take_value(
                    strength_before, x + dx, y + dy) else 0

    return reward


def discountedRewards(game_states, moves):
    raw_rewards = rawRewards(game_states)
    # strength_rewards = strengthRewards(game_states)
    discounted_rewards = np.zeros_like(raw_rewards, dtype=np.float64)
    running_reward = np.zeros_like(raw_rewards[0])
    for t in reversed(range(0, len(raw_rewards))):
        running_reward = discountedReward(running_reward, moves[t], game_states[t][1],
                                          discount_factor=0.2) + discountedReward(
            raw_rewards[t], moves[t], game_states[t][1])
        discounted_rewards[t] = running_reward  # + 0.2*(moves[t]==STILL)*(game_states[t][2])
        ##TODO : HERE FOR STRENGTH ! INDEPENDENT
    return discounted_rewards


def individualStatesAndRewards(game_state, move, discounted_reward):
    states = []
    moves = []
    rewards = []
    for y in range(len(game_state[0])):
        for x in range(len(game_state[0][0])):
            if (game_state[0][y][x] == 1):
                states += [normalizeGameState(localStateFromGlobal(game_state, x, y))]
                moves += [move[y][x]]
                rewards += [discounted_reward[y][x]]
    return states, moves, rewards


def allIndividualStatesAndRewards(game_states, moves, discounted_rewards):
    all_states = []
    all_moves = []
    all_rewards = []
    for game_state, move, discounted_reward in zip(game_states, moves, discounted_rewards):
        states_, moves_, rewards_ = individualStatesAndRewards(game_state, move, discounted_reward)
        all_states += states_
        all_moves += moves_
        all_rewards += rewards_
    return np.array(all_states), np.array(all_moves), np.array(all_rewards)


def allRewards(game_states, moves):
    # game_states n+1, moves n
    discounted_rewards = discountedRewards(game_states, moves)
    return allIndividualStatesAndRewards(game_states[:-1], moves, discounted_rewards)


def formatMoves(game_map, moves):
    moves_to_send = []
    for y in range(len(game_map.contents)):
        for x in range(len(game_map.contents[0])):
            if moves[y][x] != -1:
                moves_to_send += [Move(game_map.contents[y][x], moves[y][x])]
    return moves_to_send
