import unittest
from benchmark.lc_1593.solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_examples(self):
        self.assertEqual(self.sol.maxUniqueSplit("ababccc"), 5)
        self.assertEqual(self.sol.maxUniqueSplit("aba"), 2)
        self.assertEqual(self.sol.maxUniqueSplit("aa"), 1)

if __name__ == '__main__':
    unittest.main()
