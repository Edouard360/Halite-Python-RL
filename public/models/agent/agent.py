import numpy as np

from train.reward import localStateFromGlobal


class Agent:
    def __init__(self, name, experience):
        self.name = name
        self.experience = experience
        if self.experience is not None:
            try:
                self.experience.metric = np.load('models/' + self.name + '.npy')
            except:
                print("New metric file created")
                self.experience.metric = np.array([])

    def choose_actions(self, sess, game_state, debug=False):
        moves = np.zeros_like(game_state[0], dtype=np.int64) - 1
        for y in range(len(game_state[0])):
            for x in range(len(game_state[0][0])):
                if (game_state[0][y][x] == 1):
                    moves[y][x] = self.choose_action(sess, localStateFromGlobal(game_state, x, y), debug=debug)
        return moves

    def update_agent(self, sess):
        pass
