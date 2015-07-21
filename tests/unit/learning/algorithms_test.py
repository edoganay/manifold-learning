import numpy as np
from unittest import TestCase
from numpy import testing

from manifold.learning import algorithms


class ENearestNeighborsTest(TestCase):
    def test_basic(self):
        e = 4
        m = {
            0: {1: 5, 2: 40, 3: 4},
            1: {2: 41, 3: 1},
            2: {3: 2},
        }

        expected = {
            0: {3: 4},
            1: {3: 1},
            2: {3: 2},
        }

        actual = algorithms \
            .ENearestNeighbors(distance_matrix=m, alpha=e) \
            .run()

        self.assertDictEqual(expected, actual)


class KNearestNeighborsTest(TestCase):
    def test_basic(self):
        m = {
            0: {1: 50, 2: 10, 3: 20},
            1: {2: 4, 3: 2},
            2: {3: 2},
        }

        k = 2

        expected = {
            0: {2: 10, 3: 20},
            1: {2: 4, 3: 2},
        }

        actual = algorithms \
            .KNearestNeighbors(distance_matrix=m, alpha=k) \
            .run()

        self.assertDictEqual(expected, actual)


class AllPairsDijkstraTest(TestCase):
    def test_basic(self):
        m = {
            0: {1: 50, 2: 10, 3: 20},
            1: {2: 4, 3: 2},
            2: {3: 2},
        }

        expected = {
            0: {0:  0, 1: 14, 2: 10, 3: 12},
            1: {0: 14, 1:  0, 2:  4, 3:  2},
            2: {0: 10, 1:  4, 2:  0, 3:  2},
            3: {0: 12, 1:  2, 2:  2, 3:  0},
        }

        actual = algorithms.AllPairsDijkstra(m).run()

        self.assertDictEqual(expected, actual)


class FloydWarshallTest(TestCase):
    def test_digraph(self):
        # https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm
        distance = {
            0: {1: 50, 2: 10, 3: 20},
            1: {2: 4, 3: 2},
            2: {3: 2},
        }

        expected = {
            0: {0:  0, 1: 14, 2: 10, 3: 12},
            1: {0: 14, 1:  0, 2:  4, 3:  2},
            2: {0: 10, 1:  4, 2:  0, 3:  2},
            3: {0: 12, 1:  2, 2:  2, 3:  0},
        }

        f = algorithms.FloydWarshall(distance)
        actual = f.run()

        self.assertDictEqual(expected, actual)


class MDSTest(TestCase):
    def test_wickelmaier(self):
        proximity_matrix = {
            0: {0:   0, 1: 93, 2:  82, 3: 133},
            1: {0:  93, 1:  0, 2:  52, 3:  60},
            2: {0:  82, 1: 52, 2:   0, 3: 111},
            3: {0: 133, 1: 60, 2: 111, 3:   0},
        }

        expected = [
            [-62.831, 32.97448],
            [18.403, -12.02697],
            [-24.960, -39.71091],
            [69.388, 18.76340],
        ]

        i = algorithms.MDS(proximity_matrix, to_dimension=2)

        actual = i.run()

        testing.assert_array_almost_equal(actual, expected, decimal=3)