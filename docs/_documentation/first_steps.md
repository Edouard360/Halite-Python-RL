---
layout: default
title:  "First Steps"

---


## Run the Bot

In your console:

`cd networking; python start_game.py`

In another tab

`cd public; python MyBot.py`

This will run 1 game. Options can be added to starting the game, among which:

`python start_game.py -g 5 -x 30 -z 50`

Will run 5 games, of at most 30 turns, which at most squares of strength 50.

All the options available for start_game might by listed (_with a clear description_) using the -h flag:

`python start_game.py -h`

## Visualize the Bot

In your console:

`cd visualize export FLASK_APP=visualize.py;flask run`

Then either:

Look at http://127.0.0.1:5000/performance.png for performance insights.

Or at http://127.0.0.1:5000/ for games replay.

## Working with PyCharm

To run the Bot in Pycharm, you should provide a **mute** argument, since `MyBot.py` needs to know it's not on the Halite server, but running locally. 

Go to edit configuration and add the script argument `slave` (so that the bot knows it is in slave mode).