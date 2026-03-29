import sys
import os
import timeit
import tracemalloc
import gc
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1031.solution import Solution
from benchmark.lc_1031.generate import generate_data

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    runs = 3
    results = []

    for n in scales:
        nums, firstLen, secondLen = generate_data(n)
        
        times = []
        peak_memories = []
        
        for _ in range(runs):
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            
            s = Solution()
            s.maxSumTwoNoOverlap(nums, firstLen, secondLen)
            
            end_time = timeit.default_timer()
            _, peak = tracemalloc.get_traced_memory()
            
            tracemalloc.stop()
            gc.enable()
            
            times.append(end_time - start_time)
            peak_memories.append(peak)
            
        avg_time = sum(times) / runs
        avg_peak_memory = sum(peak_memories) / runs
        
        results.append({
            "n": n,
            "avg_time_ms": avg_time * 1000,
            "peak_memory_kb": avg_peak_memory / 1024
        })
        
    return results

if __name__ == "__main__":
    results = run_benchmarks()
    
    # Write initial results to results.json
    results_file = os.path.join(os.path.dirname(__file__), "results.json")
    
    # Keep the expected format
    output_data = {
        "problem_id": "lc_1031",
        "title": "Maximum Sum of Two Non-Overlapping Subarrays",
        "topic": "Sliding Window",
        "benchmarks": results,
        "empirical_time_complexity": "O(?)",
        "empirical_space_complexity": "O(?)",
        "notes": "reasoning based on timing ratios"
    }
    
    # If the file exists, we could just update the benchmarks array to keep metadata
    if os.path.exists(results_file):
        with open(results_file, "r") as f:
            existing_data = json.load(f)
            existing_data["benchmarks"] = results
            output_data = existing_data
            
    with open(results_file, "w") as f:
        json.dump(output_data, f, indent=2)
