class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def bstToGst(self, root: 'TreeNode') -> 'TreeNode':
        if not root:
            return None
            
        # We need a reverse in-order traversal (Right, Node, Left)
        # We'll use an iterative approach to prevent deep recursion issues
        # and to keep space complexity manageable.
        
        stack = []
        curr = root
        current_sum = 0
        
        while stack or curr:
            if curr:
                stack.append(curr)
                curr = curr.right
            else:
                curr = stack.pop()
                current_sum += curr.val
                curr.val = current_sum
                curr = curr.left
                
        return root
