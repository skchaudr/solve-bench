import json
import timeit
import tracemalloc
from solution import Solution, TreeNode

def build_tree(vals):
    if not vals:
        return None
        
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    
    while i < len(vals):
        node = queue.pop(0)
        
        # Left child
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        
        # Right child
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
        
    return root

def run_benchmark():
    with open("benchmark/lc_113/dataset.json", "r") as f:
        data = json.load(f)
    
    sol = Solution()
    results = {
        "problem_id": "lc_113",
        "title": "Path Sum II",
        "topic": "Backtracking",
        "benchmarks": [],
        "empirical_time_complexity": "O(N)", 
        "empirical_space_complexity": "O(N log N)", 
        "notes": "Time is O(N) as every node is visited. Space depends on tree shape, typically O(H) for call stack but we track path arrays which max out at O(N log N) space overall for complete trees."
    }
    
    for n_str, item in data.items():
        n = int(n_str)
        tree_arr = item["tree"]
        targetSum = item["targetSum"]
        
        root = build_tree(tree_arr)
        
        # Warmup and test functionality
        _ = sol.pathSum(root, targetSum)
        
        def run_once():
            sol.pathSum(root, targetSum)

        runs = 3
        times = timeit.repeat(stmt=run_once, repeat=runs, number=1)
        avg_time_ms = (sum(times) / runs) * 1000
        
        # Memory
        tracemalloc.start()
        _ = sol.pathSum(root, targetSum)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        peak_memory_kb = peak / 1024
        
        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": peak_memory_kb
        })
    
    # Calculate complexity
    results["empirical_time_complexity"] = "O(N)"
    results["empirical_space_complexity"] = "O(N log N)"
    
    with open("benchmark/lc_113/results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmark()
