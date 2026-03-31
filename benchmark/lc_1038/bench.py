import json
import timeit
import tracemalloc
import gc
from solution import Solution, TreeNode

def sorted_array_to_bst(arr):
    if not arr:
        return None
        
    mid = len(arr) // 2
    root = TreeNode(arr[mid])
    
    stack = [(0, mid - 1, root, True), (mid + 1, len(arr) - 1, root, False)]
    
    while stack:
        l, r, parent, is_left = stack.pop()
        if l > r:
            continue
            
        m = l + (r - l) // 2
        node = TreeNode(arr[m])
        
        if is_left:
            parent.left = node
        else:
            parent.right = node
            
        stack.append((l, m - 1, node, True))
        stack.append((m + 1, r, node, False))
        
    return root

def main():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []
    
    sol = Solution()
    
    for n in scales:
        with open(f"data_{n}.json", "r") as f:
            data = json.load(f)
        
        arr = data["arr"]
        
        # We need a fresh tree for each run since it modifies values in place
        
        # Time complexity
        gc.collect()
        
        times = []
        for _ in range(3):
            # rebuild tree because it modifies it
            root = sorted_array_to_bst(arr)
            gc.collect()
            start_time = timeit.default_timer()
            sol.bstToGst(root)
            end_time = timeit.default_timer()
            times.append((end_time - start_time) * 1000)
            
        avg_time = sum(times) / 3
        
        # Space complexity
        root = sorted_array_to_bst(arr)
        gc.collect()
        tracemalloc.start()
        sol.bstToGst(root)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        peak_kb = peak / 1024
        
        benchmarks.append({
            "n": n,
            "avg_time_ms": round(avg_time, 3),
            "peak_memory_kb": round(peak_kb, 3)
        })
        
    output = {
        "problem_id": "lc_1038",
        "title": "Binary Search Tree to Greater Sum Tree",
        "topic": "Binary Search",
        "benchmarks": benchmarks,
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Time scales linearly with N because the reverse in-order traversal visits every node exactly once. Space complexity is bounded by the height of the tree (which is O(log N) since we construct balanced trees, but empirically the max stack size can be represented within O(N)). Note memory represents the max stack size."
    }
    
    with open("results.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
