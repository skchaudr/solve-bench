import unittest
from benchmark.lc_1014.solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.maxScoreSightseeingPair([8, 1, 5, 2, 6]), 11)

    def test_example_2(self):
        self.assertEqual(self.sol.maxScoreSightseeingPair([1, 2]), 2)
        
    def test_minimum_constraints(self):
        self.assertEqual(self.sol.maxScoreSightseeingPair([1, 1]), 1)
        
    def test_decreasing_values(self):
        self.assertEqual(self.sol.maxScoreSightseeingPair([10, 8, 6, 4, 2]), 17) # 10 + 8 - 1 = 17

    def test_increasing_values(self):
        self.assertEqual(self.sol.maxScoreSightseeingPair([2, 4, 6, 8, 10]), 17) # 8 + 10 - 1 = 17

if __name__ == '__main__':
    unittest.main()
