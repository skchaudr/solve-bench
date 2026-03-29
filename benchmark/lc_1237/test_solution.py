import unittest
from solution import Solution, CustomFunction

class TestCustomFunction(CustomFunction):
    def __init__(self, func_id):
        self.func_id = func_id
    def f(self, x, y):
        if self.func_id == 1:
            return x + y
        elif self.func_id == 2:
            return x * y

class TestSolution(unittest.TestCase):
    def test_example1(self):
        s = Solution()
        f = TestCustomFunction(1)
        self.assertEqual(sorted(s.findSolution(f, 5)), sorted([[1,4],[2,3],[3,2],[4,1]]))

    def test_example2(self):
        s = Solution()
        f = TestCustomFunction(2)
        self.assertEqual(sorted(s.findSolution(f, 5)), sorted([[1,5],[5,1]]))

if __name__ == '__main__':
    unittest.main()
