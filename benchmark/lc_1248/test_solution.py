import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1248.solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_examples(self):
        self.assertEqual(self.sol.numberOfSubarrays([1,1,2,1,1], 3), 2)
        self.assertEqual(self.sol.numberOfSubarrays([2,4,6], 1), 0)
        self.assertEqual(self.sol.numberOfSubarrays([2,2,2,1,2,2,1,2,2,2], 2), 16)

if __name__ == "__main__":
    unittest.main()
