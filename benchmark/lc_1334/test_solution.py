import unittest
from solution import Solution

class TestSolution(unittest.TestCase):
    def test_example_1(self):
        n = 4
        edges = [[0,1,3],[1,2,1],[1,3,4],[2,3,1]]
        distanceThreshold = 4
        self.assertEqual(Solution().findTheCity(n, edges, distanceThreshold), 3)

    def test_example_2(self):
        n = 5
        edges = [[0,1,2],[0,4,8],[1,2,3],[1,4,2],[2,3,1],[3,4,1]]
        distanceThreshold = 2
        self.assertEqual(Solution().findTheCity(n, edges, distanceThreshold), 0)

if __name__ == '__main__':
    unittest.main()
