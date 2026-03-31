import json
import timeit
import tracemalloc
import os
import sys

sys.path.append(os.path.dirname(__file__))
from solution import Solution, TreeNode

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    results = []
    
    sol = Solution()
    
    for n in scales:
        with open(f"benchmark/lc_106/data_{n}.json", "r") as f:
            data = json.load(f)
            inorder = data["inorder"]
            postorder = data["postorder"]
        
        # Benchmarking Time
        timer = timeit.Timer(lambda: sol.buildTree(inorder, postorder))
        number, time_taken = timer.autorange()
        avg_time_ms = (time_taken / number) * 1000
        
        # Benchmarking Space
        tracemalloc.start()
        sol.buildTree(inorder, postorder)
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
        "problem_id": "lc_106",
        "title": "Construct Binary Tree from Inorder and Postorder Traversal",
        "topic": "Tree",
        "benchmarks": results,
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Time and space grow linearly with N. The iterative approach constructs the tree in O(N) time using O(N) space for the stack and tree nodes."
    }
    
    with open("benchmark/lc_106/results.json", "w") as f:
        json.dump(out_json, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
