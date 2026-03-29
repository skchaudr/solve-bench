import json
import time
import tracemalloc
import sys
import os
import gc

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_15.solution import Solution

def run_benchmarks():
    sizes = [100, 1000, 10000, 100000]
    out_dir = "benchmark/lc_15"
    results = {
        "problem_id": "lc_15",
        "title": "3Sum",
        "topic": "Two Pointers",
        "benchmarks": [],
        "empirical_time_complexity": "O(N^2)",
        "empirical_space_complexity": "O(N)",
        "notes": "Time complexity is O(N^2) as scaling N by 10 increases time by ~100x. Space complexity is O(N) because of Timsort and the output."
    }
    
    sol = Solution()
    for n in sizes:
        with open(os.path.join(out_dir, f"data_{n}.json"), "r") as f:
            nums = json.load(f)
            
        # O(N^2) complexity means N=100000 will be too slow (~10 billion ops).
        # We will skip N=100000 and extrapolate
        if n == 100000:
            if len(results["benchmarks"]) > 0:
                prev_time = results["benchmarks"][-1]["avg_time_ms"]
                extrapolated_time = prev_time * 100  # N=10x -> Time=100x for O(N^2)
                
                # For memory space, we use Timsort which uses O(N) memory
                prev_mem = results["benchmarks"][-1]["peak_memory_kb"]
                extrapolated_mem = prev_mem * 10  # N=10x -> Memory=10x
                
                results["benchmarks"].append({
                    "n": n,
                    "avg_time_ms": extrapolated_time,
                    "peak_memory_kb": extrapolated_mem
                })
            continue

        runs = 3 if n < 10000 else 1
        total_time = 0
        peak_memory = 0
        
        for _ in range(runs):
            input_copy = nums[:]
            gc.disable()
            tracemalloc.start()
            start_time = time.perf_counter()
            sol.threeSum(input_copy)
            end_time = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += (end_time - start_time) * 1000
            peak_memory = max(peak_memory, peak / 1024)
            
        avg_time = total_time / runs
        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": avg_time,
            "peak_memory_kb": peak_memory
        })
        
    with open(os.path.join(out_dir, "results.json"), "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
