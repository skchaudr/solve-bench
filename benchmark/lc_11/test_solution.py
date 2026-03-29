import unittest
from solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example1(self):
        self.assertEqual(self.sol.maxArea([1,8,6,2,5,4,8,3,7]), 49)

    def test_example2(self):
        self.assertEqual(self.sol.maxArea([1,1]), 1)

if __name__ == '__main__':
    unittest.main()
