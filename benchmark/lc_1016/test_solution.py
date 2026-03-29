import unittest
from benchmark.lc_1016.solution import Solution

class TestSolution(unittest.TestCase):
    def test_examples(self):
        sol = Solution()
        self.assertTrue(sol.queryString("0110", 3))
        self.assertFalse(sol.queryString("0110", 4))
        self.assertTrue(sol.queryString("1111000101", 5)) # 1, 10, 11, 100, 101 all in s
        
    def test_edge(self):
        sol = Solution()
        self.assertTrue(sol.queryString("1", 1))
        self.assertFalse(sol.queryString("0", 1))
        self.assertFalse(sol.queryString("10", 3))

if __name__ == '__main__':
    unittest.main()
