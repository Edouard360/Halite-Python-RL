# import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random
from hlt_networking import HLT
import sys

port = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
hlt = HLT(port=port)

myID, game_map = hlt.get_init()
hlt.send_init("MyPythonBot")

while True:
    game_map.get_frame(hlt.get_string())  # game_map.get_frame()
    moves = [Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL))) for square in game_map if
             square.owner == myID]
    hlt.send_frame(moves)
