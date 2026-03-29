import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1027.solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_examples(self):
        self.assertEqual(self.sol.longestArithSeqLength([3,6,9,12]), 4)
        self.assertEqual(self.sol.longestArithSeqLength([9,4,7,2,10]), 3)
        self.assertEqual(self.sol.longestArithSeqLength([20,1,15,3,10,5,8]), 4)
        
    def test_edge_cases(self):
        self.assertEqual(self.sol.longestArithSeqLength([1,1,1,1,1]), 5)
        self.assertEqual(self.sol.longestArithSeqLength([5,5]), 2)
        
    def test_zero_diff(self):
        self.assertEqual(self.sol.longestArithSeqLength([5, 5, 5, 5, 5]), 5)
        
if __name__ == '__main__':
    unittest.main()
