import random

from public.hlt import EAST, Move, NORTH, SOUTH, STILL, WEST
from public.models.bot.bot import Bot


class RandomBot(Bot):
    def __init__(self, myID):
        super(RandomBot, self).__init__(myID)

    def compute_moves(self, game_map, sess=None):
        [Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL))) for square in game_map if
         square.owner == self.myID]
