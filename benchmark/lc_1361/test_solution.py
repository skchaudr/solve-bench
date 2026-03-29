import unittest
from benchmark.lc_1361.solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example1(self):
        self.assertTrue(self.sol.validateBinaryTreeNodes(4, [1,-1,3,-1], [2,-1,-1,-1]))

    def test_example2(self):
        self.assertFalse(self.sol.validateBinaryTreeNodes(4, [1,-1,3,-1], [2,3,-1,-1]))

    def test_example3(self):
        self.assertFalse(self.sol.validateBinaryTreeNodes(2, [1,0], [-1,-1]))

    def test_single_node(self):
        self.assertTrue(self.sol.validateBinaryTreeNodes(1, [-1], [-1]))

    def test_disconnected(self):
        self.assertFalse(self.sol.validateBinaryTreeNodes(4, [1,-1,-1,-1], [2,-1,-1,-1]))

if __name__ == '__main__':
    unittest.main()
