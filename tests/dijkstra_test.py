"""
Tests the dijkstra function
"""
import unittest

import numpy as np
from public.util.dijkstra import build_graph_from_state, dijkstra


class TestDijkstra(unittest.TestCase):
    """
    Tests the dijkstra algorithm
    """

    def test_dijkstra(self):
        """
        Test the dijkstra algorithm
        """
        state = np.array([[0, 0, 0, 0, 1, 1],
                          [0, 1, 1, 1, 1, 1],
                          [0, 1, 1, 1, 1, 1],
                          [0, 1, 1, 1, 1, 1],
                          [0, 1, 1, 1, 1, 1],
                          [0, 0, 0, 1, 1, 1]])

        print(state)
        g = build_graph_from_state(state)
        dist_dict, _ = dijkstra(g.g, 0)

        dist = np.zeros_like(state)
        for key, value in dist_dict.items():
            dist[key] = value
        print(dist)


if __name__ == '__main__':
    unittest.main()
