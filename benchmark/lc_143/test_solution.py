import unittest
import sys
import os

# Ensure the repository root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from benchmark.lc_143.solution import Solution, ListNode

class TestReorderList(unittest.TestCase):
    def list_to_array(self, head):
        res = []
        curr = head
        while curr:
            res.append(curr.val)
            curr = curr.next
        return res

    def array_to_list(self, arr):
        if not arr: return None
        head = ListNode(arr[0])
        curr = head
        for val in arr[1:]:
            curr.next = ListNode(val)
            curr = curr.next
        return head

    def test_example_1(self):
        head = self.array_to_list([1, 2, 3, 4])
        Solution().reorderList(head)
        self.assertEqual(self.list_to_array(head), [1, 4, 2, 3])

    def test_example_2(self):
        head = self.array_to_list([1, 2, 3, 4, 5])
        Solution().reorderList(head)
        self.assertEqual(self.list_to_array(head), [1, 5, 2, 4, 3])

    def test_empty_list(self):
        head = None
        Solution().reorderList(head)
        self.assertEqual(self.list_to_array(head), [])

    def test_single_element(self):
        head = self.array_to_list([1])
        Solution().reorderList(head)
        self.assertEqual(self.list_to_array(head), [1])

if __name__ == '__main__':
    unittest.main()
