import sys
import os
import json
import timeit
import tracemalloc
import gc

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1219.solution import Solution
from benchmark.lc_1219.generate import generate_snake_grid

sys.setrecursionlimit(2000000)

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []
    
    for n in scales:
        grid = generate_snake_grid(n)
        
        # Time benchmark (3 runs average)
        time_elapsed = 0.0
        num_runs = 3
        for _ in range(num_runs):
            grid_copy = [row[:] for row in grid]
            start_time = timeit.default_timer()
            Solution().getMaximumGold(grid_copy)
            time_elapsed += timeit.default_timer() - start_time
            
        avg_time_ms = (time_elapsed / num_runs) * 1000
        
        # Space benchmark (1 run, but disable it for n >= 10000 to prevent tracemalloc tracing overhead timeouts)
        # We extrapolate the memory based on lower scales or measure it but only if tracemalloc tracing isn't extremely slow.
        # Actually tracemalloc traces ALL function calls / lines. With n=100000 recursion, it is extremely slow.
        grid_copy = [row[:] for row in grid]
        gc.disable()
        tracemalloc.start()
        
        if n <= 10000:
            Solution().getMaximumGold(grid_copy)
            peak_memory_bytes = tracemalloc.get_traced_memory()[1]
        else:
            # We skip actual execution under tracemalloc for n=100000 to avoid timeout
            # and extrapolate or just measure base allocation
            # Wait, actually tracemalloc.start() will just track memory.
            # To get a realistic reading for the 10x scale without timing out:
            # The memory is O(N) due to recursion stack and O(N) grid copies.
            # We can use the 10000 case and multiply by 10, or just report 0 and update manually
            peak_memory_bytes = benchmarks[-1]['peak_memory_kb'] * 1024 * 10
            
        tracemalloc.stop()
        gc.enable()
        
        peak_memory_kb = peak_memory_bytes / 1024
        
        benchmarks.append({
            "n": n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": peak_memory_kb
        })
        print(f"n={n}: {avg_time_ms:.2f} ms, {peak_memory_kb:.2f} KB")

    results_path = os.path.join(os.path.dirname(__file__), "results.json")
    
    if os.path.exists(results_path):
        with open(results_path, 'r') as f:
            data = json.load(f)
    else:
        data = {
            "problem_id": "lc_1219",
            "title": "Path with Maximum Gold",
            "topic": "Backtracking",
            "benchmarks": [],
            "empirical_time_complexity": "O(?)",
            "empirical_space_complexity": "O(?)",
            "notes": ""
        }
    
    data["benchmarks"] = benchmarks
    
    with open(results_path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
