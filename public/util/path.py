"""The path to another point"""
import random

from public.hlt import EAST, WEST, NORTH, SOUTH


def path_to(start, end, width, height):
    """Given start = (x,y), end = (x,y), end return dx, dy"""
    x1, y1 = start
    x2, y2 = end

    def settle(p1, p2, modulo):
        dp = min(abs(p1 - p2), modulo - abs(p1 - p2))
        if p1 < p2 and p2 - p1 != dp:  # TODO contract formula
            dp = -dp
        elif p1 > p2 and p1 - p2 == dp:
            dp = -dp
        return dp

    return settle(x1, x2, width), settle(y1, y2, height)


def move_to(dxy):
    """Move to the closest square given the tuple (dx, dy)"""
    dx, dy = dxy
    assert abs(dx) > 0 or abs(dy) > 0, "No closer move possible"
    prob_east_west = abs(dx) / (abs(dx) + abs(dy))
    if random.uniform(0, 1) < prob_east_west:  # Act east_west
        move = EAST if dx > 0 else WEST
    else:  # Act north_south
        move = SOUTH if dy > 0 else NORTH
    return move
