from typing import Optional, List

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def buildTree(self, inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
        # Using iterative approach to avoid recursion limit for n=100000
        if not inorder or not postorder:
            return None
            
        root = TreeNode(postorder[-1])
        stack = [root]
        inorder_index = len(inorder) - 1
        
        for i in range(len(postorder) - 2, -1, -1):
            postorder_val = postorder[i]
            node = stack[-1]
            if node.val != inorder[inorder_index]:
                node.right = TreeNode(postorder_val)
                stack.append(node.right)
            else:
                while stack and stack[-1].val == inorder[inorder_index]:
                    node = stack.pop()
                    inorder_index -= 1
                node.left = TreeNode(postorder_val)
                stack.append(node.left)
                
        return root
