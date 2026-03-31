class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def sortedListToBST(self, head: 'ListNode') -> 'TreeNode':
        # To avoid deep recursion, we will first extract the values to an array
        # and then build the BST iteratively or with safe stack-based approach
        # The prompt says: "When benchmarking binary tree algorithms up to massive scales (e.g., N=100,000) in Python, prioritize iterative stack-based solutions over recursive ones."
        
        if not head:
            return None
            
        vals = []
        curr = head
        while curr:
            vals.append(curr.val)
            curr = curr.next
            
        n = len(vals)
        # We can simulate the recursive build using a stack
        # Elements in stack: (left_idx, right_idx, parent_node, is_left_child)
        
        mid = n // 2
        root = TreeNode(vals[mid])
        
        stack = [(0, mid - 1, root, True), (mid + 1, n - 1, root, False)]
        
        while stack:
            l, r, parent, is_left = stack.pop()
            if l > r:
                continue
                
            m = l + (r - l) // 2
            node = TreeNode(vals[m])
            
            if is_left:
                parent.left = node
            else:
                parent.right = node
                
            stack.append((l, m - 1, node, True))
            stack.append((m + 1, r, node, False))
            
        return root
