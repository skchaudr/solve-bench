from benchmark.lc_148.solution import Solution, ListNode

def to_list(head):
    res = []
    while head:
        res.append(head.val)
        head = head.next
    return res

def to_linked_list(arr):
    dummy = ListNode(0)
    curr = dummy
    for val in arr:
        curr.next = ListNode(val)
        curr = curr.next
    return dummy.next

sol = Solution()
print(to_list(sol.sortList(to_linked_list([4, 2, 1, 3]))))
print(to_list(sol.sortList(to_linked_list([-1, 5, 3, 4, 0]))))
print(to_list(sol.sortList(to_linked_list([]))))
