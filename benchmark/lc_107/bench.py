import json
import timeit
import tracemalloc
import os
import sys

sys.path.append(os.path.dirname(__file__))
from solution import Solution, TreeNode

def construct_tree(values):
    if not values:
        return None
    root = TreeNode(values[0])
    queue = [root]
    i = 1
    while queue and i < len(values):
        node = queue.pop(0)
        
        if i < len(values):
            node.left = TreeNode(values[i])
            queue.append(node.left)
            i += 1
            
        if i < len(values):
            node.right = TreeNode(values[i])
            queue.append(node.right)
            i += 1
    return root

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    results = []
    
    sol = Solution()
    
    for n in scales:
        with open(f"benchmark/lc_107/data_{n}.json", "r") as f:
            data = json.load(f)
            values = data["values"]
        
        root = construct_tree(values)
        
        # Benchmarking Time
        timer = timeit.Timer(lambda: sol.levelOrderBottom(root))
        number, time_taken = timer.autorange()
        avg_time_ms = (time_taken / number) * 1000
        
        # Benchmarking Space
        tracemalloc.start()
        sol.levelOrderBottom(root)
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        peak_memory_kb = peak_memory / 1024
        
        results.append({
            "n": n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": peak_memory_kb
        })
        print(f"n={n}: {avg_time_ms:.4f} ms, {peak_memory_kb:.2f} KB")

    out_json = {
        "problem_id": "lc_107",
        "title": "Binary Tree Level Order Traversal II",
        "topic": "Tree",
        "benchmarks": results,
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Time and space grow linearly. The algorithm visits each node once and builds the result using O(N) auxiliary space."
    }
    
    with open("benchmark/lc_107/results.json", "w") as f:
        json.dump(out_json, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
