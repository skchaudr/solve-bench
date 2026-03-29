import sys
import os
import timeit
import tracemalloc
import gc
import json

# Add repository root to sys.path to resolve module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1248.solution import Solution
from benchmark.lc_1248.generate import generate_data

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    results = []
    
    solution = Solution()
    
    for n in scales:
        nums, k = generate_data(n)
        
        # Benchmark Time (3 runs avg)
        runs = 3
        times = []
        for _ in range(runs):
            # Pass a copy to avoid side-effects if solution mutates,
            # though this solution does not mutate.
            nums_copy = nums.copy()
            
            gc.disable()
            start = timeit.default_timer()
            solution.numberOfSubarrays(nums_copy, k)
            end = timeit.default_timer()
            gc.enable()
            times.append(end - start)
            
        avg_time_ms = (sum(times) / runs) * 1000
        
        # Benchmark Memory
        peak_memory_kb = 0
        for _ in range(runs):
            nums_copy = nums.copy()
            gc.disable()
            tracemalloc.start()
            solution.numberOfSubarrays(nums_copy, k)
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            peak_memory_kb = max(peak_memory_kb, peak / 1024.0)
            
        print(f"Scale n={n}: avg_time={avg_time_ms:.4f}ms, peak_mem={peak_memory_kb:.2f}KB")
        
        results.append({
            "n": n,
            "avg_time_ms": float(f"{avg_time_ms:.4f}"),
            "peak_memory_kb": float(f"{peak_memory_kb:.2f}")
        })
        
    return results

if __name__ == "__main__":
    results = run_benchmarks()
    
    # Check if results.json exists and load it to update
    json_path = os.path.join(os.path.dirname(__file__), "results.json")
    
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
    else:
        data = {
            "problem_id": "lc_1248",
            "title": "Count Number of Nice Subarrays",
            "topic": "Sliding Window",
            "empirical_time_complexity": "O(?)",
            "empirical_space_complexity": "O(?)",
            "notes": "reasoning based on timing ratios"
        }
        
    data["benchmarks"] = results
    
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Results saved to {json_path}")
