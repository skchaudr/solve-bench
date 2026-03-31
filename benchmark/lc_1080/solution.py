class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def sufficientSubset(self, root: 'TreeNode', limit: int) -> 'TreeNode':
        if not root:
            return None
        
        # Iterative post-order traversal to avoid deep recursion
        # stack stores: (node, parent, is_left_child, path_sum_so_far)
        # We need a way to process leaves and then propagate info up.
        # However, modifying the tree structure while doing an iterative post-order traversal
        # is a bit tricky. We can do it by maintaining the path sum downwards, and then
        # maintaining the max path sum from leaves upwards.
        
        # We will use an iterative post-order traversal.
        stack = [(root, 0)] # node, current sum
        
        # We need to know when we are visiting a node for the second time (post-order).
        # Alternatively, since we can change tree nodes, we can use a recursive approach 
        # but with sys.setrecursionlimit increased in bench.py.
        # Wait, the prompt memory says: 
        # "When benchmarking binary tree algorithms up to massive scales (e.g., N=100,000) in Python, prioritize iterative stack-based solutions over recursive ones. Deep recursion on highly skewed trees causes severe performance degradation and RecursionError..."
        
        # Let's implement an iterative DFS for sufficientSubset.
        # We can map each node to its max path sum from root to leaf passing through it.
        # Actually, a node is deleted if ALL paths through it have sum < limit.
        # Equivalently, a node is kept if at least ONE path through it has sum >= limit.
        # So we can calculate the maximum root-to-leaf path sum for each subtree.
        
        # Let's do a post-order traversal using a stack.
        # We'll push nodes, and a flag indicating if they've been visited.
        stack = [(root, False, 0)] # (node, visited, path_sum_before_node)
        
        # We need to store the max path sum that can be formed from the subtree.
        max_leaf_sum = {}
        
        # Dummy node to handle the root easily
        dummy = TreeNode(0)
        dummy.left = root
        
        # Parent mapping to delete nodes
        parent_map = {root: (dummy, True)} # True if left child
        
        while stack:
            node, visited, path_sum = stack.pop()
            
            if visited:
                # Post-order: children have been processed
                is_leaf = not node.left and not node.right
                if is_leaf:
                    max_leaf_sum[node] = path_sum + node.val
                else:
                    max_sum = float('-inf')
                    if node.left:
                        max_sum = max(max_sum, max_leaf_sum[node.left])
                    if node.right:
                        max_sum = max(max_sum, max_leaf_sum[node.right])
                    max_leaf_sum[node] = max_sum
                
                # Check if this node is insufficient
                if max_leaf_sum[node] < limit:
                    # delete node
                    parent, is_left = parent_map[node]
                    if is_left:
                        parent.left = None
                    else:
                        parent.right = None
            else:
                # Pre-order: push back as visited, then push children
                stack.append((node, True, path_sum))
                curr_sum = path_sum + node.val
                if node.right:
                    parent_map[node.right] = (node, False)
                    stack.append((node.right, False, curr_sum))
                if node.left:
                    parent_map[node.left] = (node, True)
                    stack.append((node.left, False, curr_sum))
                    
        return dummy.left
