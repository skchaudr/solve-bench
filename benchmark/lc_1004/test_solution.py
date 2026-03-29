import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1004.solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example1(self):
        self.assertEqual(self.sol.longestOnes([1,1,1,0,0,0,1,1,1,1,0], 2), 6)

    def test_example2(self):
        self.assertEqual(self.sol.longestOnes([0,0,1,1,0,0,1,1,1,0,1,1,0,0,0,1,1,1,1], 3), 10)

if __name__ == '__main__':
    unittest.main()
