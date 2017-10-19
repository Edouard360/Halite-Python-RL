"""Testing the speed of building different game states"""
import numpy as np
import pytest

from public.state.state import State2, State1
from tests.util import game_states_from_file


def build_game_state(game_states, state):
    for game_state in game_states:
        for (y, x), k in np.ndenumerate(game_state[0]):
            if k == 1:
                state.get_local(game_state, x, y)


@pytest.mark.benchmark(group="state")
def test_state1_scope1(benchmark):
    """
    Benchmark the time of dijsktra
    """
    game_states, _ = game_states_from_file()
    benchmark(build_game_state, game_states=game_states, state=State1(scope=1))
    assert True


@pytest.mark.benchmark(group="state")
def test_state1_scope2(benchmark):
    """
    Benchmark the time of dijsktra
    """
    game_states, _ = game_states_from_file()
    benchmark(build_game_state, game_states=game_states, state=State1(scope=2))
    assert True


@pytest.mark.benchmark(group="state")
def test_state1_scope3(benchmark):
    """
    Benchmark the time of dijsktra
    """
    game_states, _ = game_states_from_file()
    benchmark(build_game_state, game_states=game_states, state=State1(scope=3))
    assert True


@pytest.mark.benchmark(group="state")
def test_state2_scope2(benchmark):
    """
    Benchmark the time of dijsktra
    """
    game_states, _ = game_states_from_file()
    benchmark(build_game_state, game_states=game_states, state=State2(scope=2))
    assert True


@pytest.mark.benchmark(group="state")
def test_state2_scope3(benchmark):
    """
    Benchmark the time of dijsktra
    """
    game_states, _ = game_states_from_file()
    benchmark(build_game_state, game_states=game_states, state=State2(scope=3))
    assert True


@pytest.mark.benchmark(group="state")
def test_state2_scope4(benchmark):
    """
    Benchmark the time of dijsktra
    """
    game_states, _ = game_states_from_file()
    benchmark(build_game_state, game_states=game_states, state=State2(scope=4))
    assert True
