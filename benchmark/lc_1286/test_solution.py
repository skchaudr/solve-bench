import unittest
from benchmark.lc_1286.solution import CombinationIterator

class TestCombinationIterator(unittest.TestCase):
    def test_example(self):
        itr = CombinationIterator("abc", 2)
        self.assertEqual(itr.next(), "ab")
        self.assertTrue(itr.hasNext())
        self.assertEqual(itr.next(), "ac")
        self.assertTrue(itr.hasNext())
        self.assertEqual(itr.next(), "bc")
        self.assertFalse(itr.hasNext())

if __name__ == '__main__':
    unittest.main()
