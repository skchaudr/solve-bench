import unittest
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_1039.solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        values = [1, 2, 3]
        self.assertEqual(self.sol.minScoreTriangulation(values), 6)

    def test_example_2(self):
        values = [3, 7, 4, 5]
        self.assertEqual(self.sol.minScoreTriangulation(values), 144)

    def test_example_3(self):
        values = [1, 3, 1, 4, 1, 5]
        self.assertEqual(self.sol.minScoreTriangulation(values), 13)

if __name__ == "__main__":
    unittest.main()
