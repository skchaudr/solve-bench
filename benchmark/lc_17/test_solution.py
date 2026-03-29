import unittest
from typing import List
from benchmark.lc_17.solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        self.assertEqual(
            set(self.sol.letterCombinations("23")),
            {"ad","ae","af","bd","be","bf","cd","ce","cf"}
        )

    def test_example_2(self):
        self.assertEqual(
            self.sol.letterCombinations(""),
            []
        )

    def test_example_3(self):
        self.assertEqual(
            set(self.sol.letterCombinations("2")),
            {"a","b","c"}
        )

if __name__ == '__main__':
    unittest.main()
