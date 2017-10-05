import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

mode = 'server' if (len(sys.argv) == 1) else 'local'

if mode == 'server' or sys.argv[1]=='slave':  # 'server' mode
    import hlt
else:  # 'local' mode
    import context

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
    hlt = context.HLT(port=port)

from public.models.bot.trainedBot import TrainedBot

bot = TrainedBot()

while True:
    myID, game_map = hlt.get_init()
    hlt.send_init("MyBot")
    bot.setID(myID)

    while (mode == 'server' or hlt.get_string() == 'Get map and play!'):
        game_map.get_frame(hlt.get_string())
        moves = bot.compute_moves(game_map)
        hlt.send_frame(moves)
