import json
import random
import os
import sys

# To support large deep trees in generation if necessary
sys.setrecursionlimit(200000)

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def generate_random_tree(n: int) -> TreeNode:
    if n == 0:
        return None
    
    # We want unique values, so we can use numbers from 1 to n
    vals = list(range(1, n + 1))
    random.shuffle(vals)
    
    nodes = [TreeNode(val) for val in vals]
    root = nodes[0]
    
    # Randomly attach remaining nodes to create a random binary tree
    # To keep the depth somewhat reasonable (though we don't strictly care as long as it's N nodes),
    # we can randomly attach each node to a randomly chosen previously attached node.
    # Actually, a purely random tree might be very deep.
    # To avoid stack overflow during traversal later if we did recursive generation/traversal,
    # we just generate iteratively.
    available = [root]
    
    for i in range(1, n):
        parent_idx = random.randint(0, len(available) - 1)
        parent = available[parent_idx]
        
        node = nodes[i]
        
        # 0: left, 1: right
        if not parent.left and not parent.right:
            if random.choice([True, False]):
                parent.left = node
            else:
                parent.right = node
            available.append(node)
        elif not parent.left:
            parent.left = node
            available.append(node)
            available.pop(parent_idx) # parent is full now
        else: # not parent.right
            parent.right = node
            available.append(node)
            available.pop(parent_idx) # parent is full now
            
    return root

def get_traversals(root: TreeNode):
    preorder = []
    inorder = []
    
    # iterative traversals to avoid stack overflow on deep random trees
    # Preorder
    if root:
        stack = [root]
        while stack:
            node = stack.pop()
            preorder.append(node.val)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
                
    # Inorder
    curr = root
    stack = []
    while stack or curr:
        if curr:
            stack.append(curr)
            curr = curr.left
        else:
            curr = stack.pop()
            inorder.append(curr.val)
            curr = curr.right
            
    return preorder, inorder

def generate_data():
    scales = [100, 1000, 10000, 100000]
    data = {}
    
    for n in scales:
        root = generate_random_tree(n)
        preorder, inorder = get_traversals(root)
        data[str(n)] = {
            "preorder": preorder,
            "inorder": inorder
        }
        
    os.makedirs(os.path.dirname(os.path.abspath(__file__)), exist_ok=True)
    with open("benchmark/lc_105/data.json", "w") as f:
        json.dump(data, f)

if __name__ == "__main__":
    generate_data()
