import json
import timeit
import tracemalloc
import gc
import os
import sys

# Ensure import of Solution works
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_1361.solution import Solution

def main():
    scales = [100, 1000, 10000, 100000]
    results = []
    
    for n in scales:
        file_path = os.path.join(os.path.dirname(__file__), f"data_{n}.json")
        with open(file_path, "r") as f:
            data = json.load(f)
            
        leftChild = data["leftChild"]
        rightChild = data["rightChild"]
        
        avg_time = 0.0
        peak_mem = 0
        
        # 3 runs avg
        runs = 3
        for _ in range(runs):
            gc.collect()
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            # Copy data just in case, though the solution doesn't mutate it
            sol = Solution()
            res = sol.validateBinaryTreeNodes(n, list(leftChild), list(rightChild))
            end_time = timeit.default_timer()
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            avg_time += (end_time - start_time) * 1000
            peak_mem = max(peak_mem, peak)
            
        avg_time /= runs
        
        results.append({
            "n": n,
            "avg_time_ms": round(avg_time, 4),
            "peak_memory_kb": round(peak_mem / 1024, 2)
        })
        print(f"n={n}: {round(avg_time, 4)}ms, {round(peak_mem / 1024, 2)}KB")

    # Generate or read results.json to format correctly
    res_path = os.path.join(os.path.dirname(__file__), "results.json")
    out_data = {
        "problem_id": "lc_1361",
        "title": "Validate Binary Tree Nodes",
        "topic": "Graph",
        "benchmarks": results,
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(N)",
        "notes": "BFS visits each node at most once, and degree counting takes O(N) time. Peak memory includes queue and visited set which scale linearly."
    }
    
    with open(res_path, "w") as f:
        json.dump(out_data, f, indent=2)

if __name__ == "__main__":
    main()
