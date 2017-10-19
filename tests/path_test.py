"""Test the path_to function"""
import unittest

from public.util.path import path_to

class PathTo(unittest.TestCase):
    """
    Tests the path_to function
    """

    def test_path_to(self):
        """
        Test the path_to function
        """
        self.assertTrue(path_to((0, 0), (0, 4), 5, 5) == (0, -1))
        self.assertTrue(path_to((4, 4), (0, 0), 5, 5) == (1, 1))
        self.assertTrue(path_to((0, 0), (4, 4), 5, 5) == (-1, -1))
        self.assertTrue(path_to((0, 0), (4, 4), 5, 10) == (-1, 4))
        self.assertTrue(path_to((0, 0), (4, 4), 6, 10) == (-2, 4))
        self.assertTrue(path_to((0, 0), (4, 4), 7, 10) == (-3, 4))


if __name__ == '__main__':
    unittest.main()
