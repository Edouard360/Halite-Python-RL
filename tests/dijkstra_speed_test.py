"""Testing the speed of 2 dijkstra alternative"""
import numpy as np
import pytest

from public.util.dijkstra import build_graph_from_state, dijkstra
from tests.util import game_states_from_file


def dijkstra_naive(game_states):
    for game_state in game_states:
        g = build_graph_from_state(game_state[0])
        dist_dict, _ = dijkstra(g.g, 0)

        dist = np.zeros_like(game_state[0])
        for key, value in dist_dict.items():
            dist[key] = value


def dijkstra_update(game_states):
    g = build_graph_from_state(game_states[0][0])
    for i in range(1, len(game_states)):
        g.update(game_states[i][0], game_states[i - 1][0])
        dist_dict, _ = dijkstra(g.g, 0)

        dist = np.zeros_like(game_states[i][0])
        for key, value in dist_dict.items():
            dist[key] = value


@pytest.mark.benchmark(group="dijkstra")
def test_dijkstra_naive_speed(benchmark):
    """
    Benchmark the time of dijsktra
    """
    game_states, _ = game_states_from_file()
    benchmark(dijkstra_naive, game_states=game_states)
    assert True


@pytest.mark.benchmark(group="dijkstra")
def test_dijkstra_update_speed(benchmark):
    """
    Benchmark the time of dijsktra
    """
    game_states, _ = game_states_from_file()
    benchmark(dijkstra_update, game_states=game_states)
    assert True
