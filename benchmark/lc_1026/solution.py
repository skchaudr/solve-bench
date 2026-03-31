class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def maxAncestorDiff(self, root: 'TreeNode') -> int:
        if not root:
            return 0
        
        stack = [(root, root.val, root.val)]
        max_diff = 0
        
        while stack:
            node, cur_max, cur_min = stack.pop()
            
            diff1 = abs(cur_max - node.val)
            diff2 = abs(cur_min - node.val)
            if diff1 > max_diff:
                max_diff = diff1
            if diff2 > max_diff:
                max_diff = diff2
            
            if node.val > cur_max:
                cur_max = node.val
            if node.val < cur_min:
                cur_min = node.val
            
            if node.left:
                stack.append((node.left, cur_max, cur_min))
            if node.right:
                stack.append((node.right, cur_max, cur_min))
                
        return max_diff
