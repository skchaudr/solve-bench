import unittest
from benchmark.lc_1471.solution import Solution

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.solution = Solution()

    def test_example_1(self):
        arr = [1, 2, 3, 4, 5]
        k = 2
        # Center is 3. Strongest are 5, 1
        expected_candidates = [[5, 1], [1, 5]]
        result = self.solution.getStrongest(arr, k)
        self.assertIn(result, expected_candidates)

    def test_example_2(self):
        arr = [1, 1, 3, 5, 5]
        k = 2
        # Center is 3. Strongest are 5, 5
        expected = [5, 5]
        result = self.solution.getStrongest(arr, k)
        self.assertEqual(result, expected)

    def test_example_3(self):
        arr = [6, 7, 11, 7, 6, 8]
        k = 5
        # Center is 7. Strongest are 11, 8, 6, 6, 7
        # Note: 6 and 6 can be in either order depending on the sort algorithm stability, 
        # but the problem states return in any arbitrary order.
        expected = [11, 8, 6, 6, 7]
        result = self.solution.getStrongest(arr, k)
        
        # Since the problem allows arbitrary order, we can check if the multisets match
        self.assertEqual(sorted(result), sorted(expected))
        
    def test_all_elements(self):
        arr = [6, -3, 7, 2, 11]
        k = 5
        result = self.solution.getStrongest(arr, k)
        self.assertEqual(len(result), 5)
        self.assertEqual(sorted(result), sorted([6, -3, 7, 2, 11]))

if __name__ == '__main__':
    unittest.main()
