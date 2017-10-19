"""The state file"""
import numpy as np

STRENGTH_SCALE = 255
PRODUCTION_SCALE = 10


class State:
    def __init__(self, local_size):
        self.local_size = local_size

    def get_local(self, game_state, x, y):
        pass

    def get_local_and_normalize(self, game_state, x, y):
        return self.get_local(game_state, x, y) / np.array([1, STRENGTH_SCALE, PRODUCTION_SCALE])[:, np.newaxis]


class State1(State):
    def __init__(self, scope=1):
        self.scope = scope
        super(State1, self).__init__(local_size=3 * ((2 * scope + 1) ** 2))

    def get_local(self, game_state, x, y):
        # all the axes remain through the operation, because of range
        return np.take(np.take(game_state, range(y - self.scope, y + self.scope + 1), axis=1, mode='wrap'),
                       range(x - self.scope, x + self.scope + 1), axis=2, mode='wrap').reshape(3, -1)


class State2(State):
    def __init__(self, scope=2):
        self.scope = scope
        super(State2, self).__init__(local_size=3 * (2 * (scope ** 2) + 2 * scope + 1))

    def get_local(self, game_state, x, y):
        to_concat = ()
        for i in range(self.scope + 1):
            slice_s = np.take(np.take(game_state,
                                      range(x - (self.scope - i), x + (self.scope - i) + 1), axis=2, mode='wrap'),
                              [y - i, y + i] if i != 0 else y, axis=1, mode='wrap')
            slice_s = slice_s.reshape(3, -1)
            to_concat += (slice_s,)
        return np.concatenate(to_concat, axis=1)


def get_game_state(game_map, my_id):
    game_state = np.reshape(
        [[(square.owner == my_id) + 0, square.strength, square.production] for square in game_map],
        [game_map.height, game_map.width, 3])
    return np.swapaxes(np.swapaxes(game_state, 2, 0), 1, 2)
