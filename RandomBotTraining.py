import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random


def assign_move(square, game_map):
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.owner != myID and neighbor.strength < square.strength:
            return Move(square, direction)

    if square.strength < 5 * square.production:
        return Move(square, STILL)
    else:
        return Move(square, random.choice((NORTH, WEST)))


while True:
    myID, game_map = hlt.get_init()
    hlt.send_init("RandomPythonBot")
    while (hlt.get_string() == 'Get map and play!'):
        game_map.get_frame(hlt.get_string())
        moves = [assign_move(square, game_map) for square in game_map if
                 square.owner == myID]
        hlt.send_frame(moves)
