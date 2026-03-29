import unittest
from solution import Solution

class TestSolution(unittest.TestCase):
    def test_example1(self):
        s = Solution()
        self.assertEqual(s.longestStrChain(["a","b","ba","bca","bda","bdca"]), 4)

    def test_example2(self):
        s = Solution()
        self.assertEqual(s.longestStrChain(["xbc","pcxbcf","xb","cxbc","pcxbc"]), 5)

    def test_example3(self):
        s = Solution()
        self.assertEqual(s.longestStrChain(["abcd","dbqca"]), 1)

if __name__ == '__main__':
    unittest.main()
