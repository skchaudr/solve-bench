import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_1498.solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(self.sol.numSubseq([3,5,6,7], 9), 4)

    def test_example_2(self):
        self.assertEqual(self.sol.numSubseq([3,3,6,8], 10), 6)

    def test_example_3(self):
        self.assertEqual(self.sol.numSubseq([2,3,3,4,6,7], 12), 61)

if __name__ == '__main__':
    unittest.main()
