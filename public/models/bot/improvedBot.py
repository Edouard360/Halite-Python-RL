import random

from public.hlt import Move, NORTH, STILL, WEST
from public.models.bot.bot import Bot


class ImprovedBot(Bot):
    def compute_moves(self, game_map, sess=None):
        moves = []
        for square in game_map:
            if square.owner == self.myID:
                for direction, neighbor in enumerate(game_map.neighbors(square)):
                    if neighbor.owner != self.myID and neighbor.strength < square.strength:
                        moves += [Move(square, direction)]
                if square.strength < 5 * square.production:
                    moves += [Move(square, STILL)]
                else:
                    moves += [Move(square, random.choice((NORTH, WEST)))]
        return moves
