import time
import tracemalloc
import gc
import json
import os
import sys

# Append the repository root to sys.path to resolve module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1466.solution import Solution
from benchmark.lc_1466.generate import generate_random_tree

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []
    
    sol = Solution()
    
    for n in scales:
        print(f"Benchmarking n={n}...")
        
        # We need to average over 3 runs
        total_time = 0.0
        max_peak_memory = 0
        
        for _ in range(3):
            # Generate data fresh per iteration to avoid any potential side effects
            connections = generate_random_tree(n)
            
            gc.disable()
            tracemalloc.start()
            
            start_time = time.perf_counter()
            sol.minReorder(n, connections)
            end_time = time.perf_counter()
            
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += (end_time - start_time)
            max_peak_memory = max(max_peak_memory, peak)
            
        avg_time_ms = (total_time / 3) * 1000
        peak_memory_kb = max_peak_memory / 1024
        
        benchmarks.append({
            "n": n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": peak_memory_kb
        })
        print(f"  Avg Time: {avg_time_ms:.2f} ms")
        print(f"  Peak Memory: {peak_memory_kb:.2f} KB")

    results = {
        "problem_id": "lc_1466",
        "title": "Reorder Routes to Make All Paths Lead to the City Zero",
        "topic": "Graph",
        "benchmarks": benchmarks,
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Both time and space complexity scale linearly with N (O(N) since edges = N - 1) because the algorithm traverses all edges once via BFS, and stores the graph as an adjacency list."
    }
    
    # Write to results.json
    results_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"Results written to {results_path}")

if __name__ == "__main__":
    run_benchmarks()
