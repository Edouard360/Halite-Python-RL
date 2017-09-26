from public.models.agent.vanillaAgent import VanillaAgent
from public.models.bot.bot import Bot
from train.reward import getGameState, formatMoves
import tensorflow as tf


class TrainedBot(Bot):
    def __init__(self, myID=None):
        lr = 1e-3;
        s_size = 9 * 3;
        a_size = 5;
        h_size = 50
        self.agent = VanillaAgent(None, lr, s_size, a_size, h_size)
        super(TrainedBot, self).__init__(myID)

    def compute_moves(self, game_map, sess=None):
        game_state = getGameState(game_map, self.myID)
        return formatMoves(game_map, self.agent.choose_actions(sess, game_state))
