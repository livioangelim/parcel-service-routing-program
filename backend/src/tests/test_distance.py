import unittest
from distance import DistanceData


class TestDistanceData(unittest.TestCase):

    def setUp(self):
        self.distance_data = DistanceData()
        self.distance_data.address_list = ['A', 'B', 'C']
        self.distance_data.distance_table = [
            [0.0, 1.0, 2.0],
            [1.0, 0.0, 1.5],
            [2.0, 1.5, 0.0]
        ]

    def test_get_distance(self):
        self.assertEqual(self.distance_data.get_distance('A', 'B'), 1.0)
        self.assertEqual(self.distance_data.get_distance('B', 'C'), 1.5)
        self.assertEqual(self.distance_data.get_distance('C', 'A'), 2.0)


if __name__ == '__main__':
    unittest.main()
