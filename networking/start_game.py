import subprocess
import argparse
import os

def start_game(port, dim=10, max_strength=25, max_turn=25, max_game=1,silent_bool=True, timeout=False, quiet=True):
    path_to_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    subprocess.call([path_to_root + "/networking/kill.sh", str(port)])
    halite = path_to_root + '/public/halite '
    dimensions = '-d "' + str(dim) + ' ' + str(dim) + '" '

    max_strength = '-z ' + str(max_strength) + ' '
    max_turn = '-x ' + str(max_turn) + ' '
    max_game = '-g ' + str(max_game) + ' '
    silent_bool = '-j ' if silent_bool else ''
    timeout = '-t ' if timeout else ''
    quiet = '-q ' if quiet else ''
    players = [
        "python3 " + path_to_root + "/networking/pipe_socket_translator.py " + str(port)
    ]
    n_player = '' if len(players) > 1 else '-n 1 '

    players = '"' + '" "'.join(players) + '"'

    print("Launching process")
    subprocess.call(halite + dimensions + n_player + max_strength + max_turn + silent_bool + timeout + quiet + max_game +players,
                    shell=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="the port for the simulation", default=2000)
    parser.add_argument("-t", "--timeout", help="timeout", action="store_true")
    parser.add_argument("-j", "--silent", help="silent", action="store_true", default=True)
    parser.add_argument("-q", "--quiet", help="quiet", action="store_true", default=False)
    parser.add_argument("-s", "--strength", help="max strength", type=int, default=25)
    parser.add_argument("-d", "--dimension", help="max dimension", type=int, default=10)
    parser.add_argument("-m", "--maxturn", help="max turn", type=int, default=25)
    parser.add_argument("-g", "--maxgame", help="max game", type=int, default=1) # -1 for infinite game
    args = parser.parse_args()
    start_game(str(args.port), dim=args.dimension, max_strength=args.strength, max_turn=args.maxturn,
               silent_bool=args.silent, timeout=args.timeout, max_game=args.maxgame, quiet=args.quiet)
