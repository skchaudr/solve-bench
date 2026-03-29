import unittest
from benchmark.lc_1156.solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_cases(self):
        self.assertEqual(self.sol.maxRepOpt1("ababa"), 3)
        self.assertEqual(self.sol.maxRepOpt1("aaabaaa"), 6)
        self.assertEqual(self.sol.maxRepOpt1("aaaaa"), 5)

if __name__ == '__main__':
    unittest.main()
