from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        res = []
        
        # Iterative DFS using a stack to avoid recursion depth limits for large N
        if not root:
            return res
            
        stack = [(root, root.val, [root.val])]
        
        while stack:
            node, curr_sum, path = stack.pop()
            
            if not node.left and not node.right and curr_sum == targetSum:
                res.append(path)
                
            if node.right:
                stack.append((node.right, curr_sum + node.right.val, path + [node.right.val]))
            if node.left:
                stack.append((node.left, curr_sum + node.left.val, path + [node.left.val]))
                
        return res
