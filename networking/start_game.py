"""The start_game function to launch the halite.exe"""
import subprocess
import argparse
import os


def start_game(port=2000, width=10, height=10, max_strength=25, max_turn=25, max_game=1,
               silent_bool=True, timeout=True, quiet=True,
               n_pipe_players=1, slave_players=None):
    """
    The start_game function to launch the halite.exe.
    Execute with the -h option for help.
    """
    path_to_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    for i in range(n_pipe_players):
        subprocess.call([path_to_root + "/networking/kill.sh", str(port + i)])  # Free the necessary ports
    # subprocess.call([path_to_root + "/networking/kill.sh", str(port+1)]) # TODO automatic call to subprocess
    halite = path_to_root + '/public/halite '
    dimensions = '-d "' + str(height) + ' ' + str(width) + '" '

    max_strength = '-z ' + str(max_strength) + ' '
    max_turn = '-x ' + str(max_turn) + ' '
    max_game = '-g ' + str(max_game) + ' '
    silent_bool = '-j ' if silent_bool else ''
    timeout = '-t ' if timeout else ''
    quiet = '-q ' if quiet else ''
    pipe_players = [
        "python3 " + path_to_root + "/networking/pipe_socket_translator.py " + str(port + i) for i in
        range(n_pipe_players)
    ]
    slave_players = [
        "python3 " + path_to_root + "/public/" + slave_player + ' slave' for slave_player in slave_players
    ] if slave_players is not None else []  # slave is the slave argument
    players = pipe_players + slave_players
    # "python3 " + path_to_root + "/networking/pipe_socket_translator.py " + str(port+1)
    n_player = '' if len(players) > 1 else '-n 1 '

    players = '"' + '" "'.join(players) + '"'
    print(players)
    print("Launching process")

    subprocess.call(
        halite + dimensions + n_player + max_strength + max_turn + silent_bool + timeout + quiet + max_game + players,
        shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int,
                        help="the port for the simulation - Useless if there are no pipe_players",
                        default=2000)
    parser.add_argument("-t", "--timeout", help="Doens't timeout if you set this flag is set",
                        action="store_true", default=False)
    parser.add_argument("-j", "--silent", help="Doesn't print *.hlt file",
                        action="store_true", default=False)
    parser.add_argument("-q", "--quiet", help="Doesn't output information to the console",
                        action="store_true", default=False)
    parser.add_argument("-s", "--strength", help="The max strength of the squares, if needed",
                        type=int, default=25)
    parser.add_argument("-dw", "--width", help="The width of the game",
                        type=int, default=10)
    parser.add_argument("-dh", "--height", help="The height of the game",
                        type=int, default=10)
    parser.add_argument("-m", "--maxturn", help="The total number of turns per game (maximum)",
                        type=int, default=25)
    parser.add_argument("-g", "--maxgame", help="The total number of games to play",
                        type=int, default=1)  # -1 for infinite game
    parser.add_argument("-pp", "--n_pipe_players",
                        help="The number of pipe players. You need to handle these players yourself. "
                             "Each of them has a port assigned.",
                        type=int, default=0)
    parser.add_argument("-sp", "--slave_players",
                        help="The slave players. Handled by the halite.exe. "
                             "You should write one of these two strings: "
                             "'MyBot.py' or 'OpponentBot.py' (multiple time if desired) ",
                        nargs='+', default=[])
    args = parser.parse_args()
    start_game(port=args.port, width=args.width, height=args.height, max_strength=args.strength, max_turn=args.maxturn,
               silent_bool=args.silent, timeout=args.timeout, max_game=args.maxgame, quiet=args.quiet,
               n_pipe_players=args.n_pipe_players,
               slave_players=args.slave_players)
