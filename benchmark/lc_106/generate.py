import json
import random
import os
import sys

# To generate a valid inorder and postorder array, we generate a tree first
class TreeNode:
    def __init__(self, val=0):
        self.val = val
        self.left = None
        self.right = None

def generate_random_tree(n):
    if n == 0:
        return None
    
    # Pre-allocate values (unique)
    values = random.sample(range(-n * 10, n * 10), n)
    
    root = TreeNode(values[0])
    nodes = [root]
    
    # We build it level by level to avoid deep recursion which would fail later anyway,
    # but the solution is iterative so it can handle it. For generation, a reasonably balanced 
    # tree or slightly skewed is fine.
    
    for i in range(1, n):
        parent = random.choice(nodes)
        new_node = TreeNode(values[i])
        
        # Determine if left or right
        if not parent.left and not parent.right:
            if random.random() < 0.5:
                parent.left = new_node
            else:
                parent.right = new_node
            nodes.append(new_node)
        elif not parent.left:
            parent.left = new_node
            nodes.append(new_node)
        elif not parent.right:
            parent.right = new_node
            nodes.append(new_node)
        else:
            # We picked a full node, try again - but wait, to make it O(N) we can just 
            # keep an active list
            pass
            
    # Better approach to avoid rejection sampling:
    return root

def generate_tree_fast(n):
    if n == 0:
        return None
    values = random.sample(range(-n * 10, n * 10), n)
    root = TreeNode(values[0])
    active = [root]
    
    for i in range(1, n):
        parent_idx = random.randint(0, len(active) - 1)
        parent = active[parent_idx]
        new_node = TreeNode(values[i])
        
        if not parent.left and not parent.right:
            if random.random() < 0.5:
                parent.left = new_node
            else:
                parent.right = new_node
        elif not parent.left:
            parent.left = new_node
            active.pop(parent_idx) # Node is full
        elif not parent.right:
            parent.right = new_node
            active.pop(parent_idx) # Node is full
            
        active.append(new_node)
        
    return root

def get_traversals(root):
    inorder = []
    postorder = []
    
    def traverse(node):
        if not node:
            return
        stack = []
        curr = node
        # Inorder iterative
        while stack or curr:
            if curr:
                stack.append(curr)
                curr = curr.left
            else:
                curr = stack.pop()
                inorder.append(curr.val)
                curr = curr.right
                
        # Postorder iterative
        stack = [node]
        while stack:
            curr = stack.pop()
            postorder.append(curr.val)
            if curr.left:
                stack.append(curr.left)
            if curr.right:
                stack.append(curr.right)
        postorder.reverse()
        
    traverse(root)
    return inorder, postorder

def generate_test_cases():
    scales = [100, 1000, 10000, 100000]
    os.makedirs("benchmark/lc_106", exist_ok=True)
    
    for n in scales:
        root = generate_tree_fast(n)
        inorder, postorder = get_traversals(root)
        
        with open(f"benchmark/lc_106/data_{n}.json", "w") as f:
            json.dump({"n": n, "inorder": inorder, "postorder": postorder}, f)

if __name__ == "__main__":
    generate_test_cases()
