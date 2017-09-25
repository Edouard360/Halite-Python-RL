import hlt
from hlt import NORTH, EAST, SOUTH, WEST, STILL, Move, Square
import random

while True:
    myID, game_map = hlt.get_init()
    hlt.send_init("RandomPythonBot")
    game_map.get_frame(hlt.get_string())

    for i in range(30):
        moves = [Move(square, random.choice((NORTH, EAST, SOUTH, WEST, STILL))) for square in game_map if
                 square.owner == myID]
        hlt.send_frame(moves)
        if (i != 29):
            game_map.get_frame(hlt.get_string())
