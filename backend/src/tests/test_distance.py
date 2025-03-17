import unittest
from ..utils.distance import calculate_distance


class TestDistance(unittest.TestCase):
    def test_calculate_distance(self):
        self.assertAlmostEqual(calculate_distance((0, 0), (3, 4)), 5.0)
        self.assertAlmostEqual(calculate_distance((1, 1), (4, 5)), 5.0)
        self.assertAlmostEqual(calculate_distance((-1, -1), (-4, -5)), 5.0)


if __name__ == '__main__':
    unittest.main()
