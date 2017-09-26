# import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
from hlt_networking import HLT
import sys

def assign_move(square, game_map):
    for direction, neighbor in enumerate(game_map.neighbors(square)):
        if neighbor.owner != myID and neighbor.strength < square.strength:
            return Move(square, direction)

    if square.strength < 5 * square.production:
        return Move(square, STILL)
    else:
        return Move(square, random.choice((NORTH, WEST)))

port = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
hlt = HLT(port=port)

while True:
    myID, game_map = hlt.get_init()
    hlt.send_init("MyPythonBot")
    while (hlt.get_string() == 'Get map and play!'):
        game_map.get_frame(hlt.get_string())
        moves = [assign_move(square, game_map) for square in game_map if
                 square.owner == myID]
        hlt.send_frame(moves)
