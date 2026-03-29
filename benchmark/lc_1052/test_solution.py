import unittest
from solution import Solution

class TestSolution(unittest.TestCase):
    def test_example_1(self):
        customers = [1,0,1,2,1,1,7,5]
        grumpy = [0,1,0,1,0,1,0,1]
        minutes = 3
        sol = Solution()
        self.assertEqual(sol.maxSatisfied(customers, grumpy, minutes), 16)

    def test_example_2(self):
        customers = [1]
        grumpy = [0]
        minutes = 1
        sol = Solution()
        self.assertEqual(sol.maxSatisfied(customers, grumpy, minutes), 1)

if __name__ == '__main__':
    unittest.main()
