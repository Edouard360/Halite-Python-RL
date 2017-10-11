"""The Random Bot"""
import random

from public.hlt import EAST, Move, NORTH, SOUTH, STILL, WEST
from public.models.strategy.Strategy import Strategy


class RandomStrategy(Strategy):
    def compute_moves(self, game_map):
        """Compute the moves given a game_map"""
        return [Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL))) for square in game_map if
                square.owner == self.my_id]
