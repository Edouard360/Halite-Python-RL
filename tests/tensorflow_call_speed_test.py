"""Testing the speed of 2 tensorflow alternatives"""
import numpy as np
import pytest

from public.models.agent.Agent import start_agent
from public.models.agent.VanillaAgent import VanillaAgent
from public.state.state import State1
from tests.util import game_states_from_file


def tensorflow_naive(game_states, sess, agent):
    state = State1(scope=1)
    for game_state in game_states:
        for y in range(len(game_state[0])):
            for x in range(len(game_state[0][0])):
                if game_state[0][y][x] == 1:
                    game_state_n = state.get_local_and_normalize(game_state, x, y).reshape(1, -1)
                    sess.run(agent.policy, feed_dict={agent.state_in: game_state_n})


def tensorflow_combined(game_states, sess, agent):
    state = State1(scope=1)
    for game_state in game_states:
        all_game_state_n = np.array([]).reshape(0, state.local_size)
        for y in range(len(game_state[0])):
            for x in range(len(game_state[0][0])):
                if game_state[0][y][x] == 1:
                    game_state_n = state.get_local_and_normalize(game_state, x, y).reshape(1, -1)
                    all_game_state_n = np.concatenate((all_game_state_n, game_state_n), axis=0)
        sess.run(agent.policy, feed_dict={agent.state_in: all_game_state_n})


@pytest.mark.benchmark(group="tf")
def test_tensorflow_naive_speed(benchmark):
    """
    Benchmark the time of dijsktra
    """
    sess, agent = start_agent(VanillaAgent, State1(scope=1))
    game_states, _ = game_states_from_file()
    benchmark(tensorflow_naive, game_states=game_states, sess=sess, agent=agent)
    assert True


@pytest.mark.benchmark(group="tf")
def test_tensorflow_combined_speed(benchmark):
    """
    Benchmark the time of dijsktra
    """
    sess, agent = start_agent(VanillaAgent, State1(scope=1))
    game_states, _ = game_states_from_file()
    benchmark(tensorflow_combined, game_states=game_states, sess=sess, agent=agent)
    assert True
