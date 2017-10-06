"""Importing the game from aws"""
import json
import urllib.request
import numpy as np


def game_states_from_url(game_url):
    """
    We host known games on aws server and we run the tests according to these games, from which we know the output
    :param game_url: The url of the game on the server (string).
    :return:
    """
    game = json.loads(urllib.request.urlopen(game_url).readline().decode("utf-8"))

    owner_frames = np.array(game["frames"])[:, :, :, 0][:, np.newaxis, :, :]
    strength_frames = np.array(game["frames"])[:, :, :, 1][:, np.newaxis, :, :]
    production_frames = np.repeat(np.array(game["productions"])[np.newaxis, np.newaxis, :, :], len(owner_frames),
                                  axis=0)
    moves = np.array(game['moves'])

    game_states = np.concatenate(([owner_frames, strength_frames, production_frames]), axis=1)
    return game_states, moves
