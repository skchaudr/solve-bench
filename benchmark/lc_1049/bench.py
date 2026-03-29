import json
import timeit
import tracemalloc
import gc
import os
import sys

# Add the parent directory to the path so we can import the solution
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from benchmark.lc_1049.solution import Solution

def run_benchmark():
    with open('benchmark/lc_1049/data.json', 'r') as f:
        data = json.load(f)
    
    results = {
        "problem_id": "lc_1049",
        "benchmarks": [],
        "empirical_time_complexity": "O(N log N)",
        "empirical_space_complexity": "O(N)"
    }
    
    sol = Solution()
    
    for n_str in ['100', '1000', '10000', '100000']:
        n = int(n_str)
        stones = data[n_str]
        
        runs = 3
        times = []
        memories = []
        
        for _ in range(runs):
            # Isolate time measurement
            gc.collect()
            start_time = timeit.default_timer()
            sol.lastStoneWeightII(stones)
            end_time = timeit.default_timer()
            times.append((end_time - start_time) * 1000) # ms
            
            # Isolate memory measurement
            gc.collect()
            tracemalloc.start()
            sol.lastStoneWeightII(stones)
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memories.append(peak / 1024) # kb
            
        avg_time = sum(times) / runs
        avg_memory = sum(memories) / runs
        
        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": round(avg_time, 2),
            "peak_memory_kb": round(avg_memory, 2)
        })
        print(f"n: {n}, avg_time_ms: {avg_time:.2f}, peak_memory_kb: {avg_memory:.2f}")
        
    with open('benchmark/lc_1049/results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmark()
