import unittest
from benchmark.lc_1415.solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_examples(self):
        self.assertEqual(self.sol.getHappyString(1, 3), "c")
        self.assertEqual(self.sol.getHappyString(1, 4), "")
        self.assertEqual(self.sol.getHappyString(3, 9), "cab")
        
    def test_more(self):
        self.assertEqual(self.sol.getHappyString(2, 7), "")
        self.assertEqual(self.sol.getHappyString(10, 100), "abacbabacb")

if __name__ == "__main__":
    unittest.main()
