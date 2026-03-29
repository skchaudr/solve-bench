import unittest
from solution import Solution

class TestSolution(unittest.TestCase):
    def test_basic(self):
        s = Solution()
        b1 = [1,1,1,2,2,2]
        res1 = s.rearrangeBarcodes(b1)
        self.assertEqual(sorted(res1), sorted(b1))
        for i in range(len(res1) - 1):
            self.assertNotEqual(res1[i], res1[i+1])
            
        b2 = [1,1,1,1,2,2,3,3]
        res2 = s.rearrangeBarcodes(b2)
        self.assertEqual(sorted(res2), sorted(b2))
        for i in range(len(res2) - 1):
            self.assertNotEqual(res2[i], res2[i+1])

if __name__ == '__main__':
    unittest.main()
