import unittest
from solution import Solution

class TestSolution(unittest.TestCase):
    def test_example_1(self):
        s = Solution()
        self.assertEqual(s.maxSumTwoNoOverlap([0,6,5,2,2,5,1,9,4], 1, 2), 20)
        
    def test_example_2(self):
        s = Solution()
        self.assertEqual(s.maxSumTwoNoOverlap([3,8,1,3,2,1,8,9,0], 3, 2), 29)
        
    def test_example_3(self):
        s = Solution()
        self.assertEqual(s.maxSumTwoNoOverlap([2,1,5,6,0,9,5,0,3,8], 4, 3), 31)

if __name__ == '__main__':
    unittest.main()
