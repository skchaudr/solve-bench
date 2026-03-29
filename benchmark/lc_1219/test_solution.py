import unittest
from solution import Solution

class TestSolution(unittest.TestCase):
    def test_example_1(self):
        grid = [[0,6,0],[5,8,7],[0,9,0]]
        self.assertEqual(Solution().getMaximumGold(grid), 24)

    def test_example_2(self):
        grid = [[1,0,7],[2,0,6],[3,4,5],[0,3,0],[9,0,20]]
        self.assertEqual(Solution().getMaximumGold(grid), 28)

if __name__ == "__main__":
    unittest.main()
