import unittest
from benchmark.lc_142.solution import Solution, ListNode

def build_linked_list(arr, pos):
    if not arr:
        return None
    head = ListNode(arr[0])
    curr = head
    cycle_node = None
    if pos == 0:
        cycle_node = head
        
    for i in range(1, len(arr)):
        curr.next = ListNode(arr[i])
        curr = curr.next
        if i == pos:
            cycle_node = curr
            
    if cycle_node:
        curr.next = cycle_node
        
    return head

class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_1(self):
        head = build_linked_list([3, 2, 0, -4], 1)
        res = self.sol.detectCycle(head)
        self.assertIsNotNone(res)
        self.assertEqual(res.val, 2)
        
    def test_example_2(self):
        head = build_linked_list([1, 2], 0)
        res = self.sol.detectCycle(head)
        self.assertIsNotNone(res)
        self.assertEqual(res.val, 1)

    def test_example_3(self):
        head = build_linked_list([1], -1)
        res = self.sol.detectCycle(head)
        self.assertIsNone(res)

if __name__ == "__main__":
    unittest.main()
