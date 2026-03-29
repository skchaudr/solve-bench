from typing import Optional

class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def sortList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
            
        # Get length
        length = 0
        curr = head
        while curr:
            length += 1
            curr = curr.next
            
        dummy = ListNode(0)
        dummy.next = head
        
        step = 1
        while step < length:
            curr = dummy.next
            tail = dummy
            while curr:
                left = curr
                right = self.split(left, step)
                curr = self.split(right, step)
                tail = self.merge(left, right, tail)
            step *= 2
            
        return dummy.next

    def split(self, head: Optional[ListNode], step: int) -> Optional[ListNode]:
        if not head:
            return None
        
        for i in range(1, step):
            if not head.next:
                break
            head = head.next
            
        right = head.next
        head.next = None
        return right
        
    def merge(self, left: Optional[ListNode], right: Optional[ListNode], tail: ListNode) -> ListNode:
        curr = tail
        while left and right:
            if left.val < right.val:
                curr.next = left
                left = left.next
            else:
                curr.next = right
                right = right.next
            curr = curr.next
            
        if left:
            curr.next = left
        elif right:
            curr.next = right
            
        while curr.next:
            curr = curr.next
            
        return curr
