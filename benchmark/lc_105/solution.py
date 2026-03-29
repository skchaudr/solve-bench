from typing import List, Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not preorder:
            return None
            
        root = TreeNode(preorder[0])
        stack = [root]
        inorder_idx = 0
        
        for i in range(1, len(preorder)):
            node = stack[-1]
            if node.val != inorder[inorder_idx]:
                node.left = TreeNode(preorder[i])
                stack.append(node.left)
            else:
                while stack and stack[-1].val == inorder[inorder_idx]:
                    node = stack.pop()
                    inorder_idx += 1
                node.right = TreeNode(preorder[i])
                stack.append(node.right)
                
        return root
