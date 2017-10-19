"""The Opponent.py file that executes the ImprovedBot.py"""
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
try:
    from public.models.strategy.ImprovedStrategy import ImprovedStrategy
    from networking.hlt_networking import HLT
except:
    raise

mode = 'server' if (len(sys.argv) == 1) else 'local'
if mode == 'server' or sys.argv[1] == 'slave':  # 'server' mode
    import hlt
else:  # 'local' mode
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    hlt = HLT(port=port)

bot = ImprovedStrategy()

while True:
    my_id, game_map = hlt.get_init()
    hlt.send_init("OpponentBot")
    bot.set_id(my_id)

    while mode == 'server' or hlt.get_string() == 'Get map and play!':
        game_map.get_frame(hlt.get_string())
        moves = bot.compute_moves(game_map)
        hlt.send_frame(moves)
