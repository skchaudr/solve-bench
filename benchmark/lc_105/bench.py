import timeit
import tracemalloc
import gc
import json
import os
import sys

# To ensure the solution can be imported and executed successfully
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from solution import Solution

def run_benchmarks():
    data_file = "benchmark/lc_105/data.json"
    with open(data_file, "r") as f:
        data = json.load(f)

    results = {
        "problem_id": "lc_105",
        "benchmarks": [],
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(N)"
    }
    
    solution = Solution()
    scales = sorted(int(k) for k in data.keys())

    for n in scales:
        preorder = data[str(n)]["preorder"]
        inorder = data[str(n)]["inorder"]
        
        # Warmup and test correctness implicitly
        _ = solution.buildTree(preorder, inorder)

        # Time
        # To avoid data corruption and ensure fair timing, use the global preorder and inorder vars.
        # But this function is read-only on the lists so it shouldn't mutate.
        timer = timeit.Timer(
            stmt="solution.buildTree(preorder, inorder)",
            globals={
                "solution": solution,
                "preorder": preorder,
                "inorder": inorder
            }
        )
        
        runs = 3
        times = []
        for _ in range(runs):
            gc.collect()
            times.append(timer.timeit(number=1))
        
        avg_time_ms = (sum(times) / runs) * 1000.0

        # Memory
        gc.collect()
        tracemalloc.start()
        _ = solution.buildTree(preorder, inorder)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        peak_memory_kb = peak / 1024.0

        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })
        
        print(f"n={n}: time={avg_time_ms:.3f}ms, memory={peak_memory_kb:.3f}KB")

    with open("benchmark/lc_105/results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
