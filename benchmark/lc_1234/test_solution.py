import unittest
from solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_examples(self):
        self.assertEqual(self.sol.balancedString("QWER"), 0)
        self.assertEqual(self.sol.balancedString("QQWE"), 1)
        self.assertEqual(self.sol.balancedString("QQQW"), 2)
        self.assertEqual(self.sol.balancedString("QQQQ"), 3)

if __name__ == '__main__':
    unittest.main()
