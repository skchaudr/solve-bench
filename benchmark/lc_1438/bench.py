import os
import sys
import json
import timeit
import tracemalloc
import gc
from typing import List

# Ensure we can import from benchmark directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1438.solution import Solution
from benchmark.lc_1438.generate import generate_test_case

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []
    
    for n in scales:
        print(f"Benchmarking n = {n}...")
        test_case = generate_test_case(n)
        nums = test_case["nums"]
        limit = test_case["limit"]
        
        avg_time_ms = 0.0
        peak_memory_kb = 0.0
        
        runs = 3
        
        for _ in range(runs):
            # Do NOT copy inside tracemalloc because solution does not modify input
            sol = Solution()
            
            gc.collect()
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            sol.longestSubarray(nums, limit)
            end_time = timeit.default_timer()
            
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            avg_time_ms += (end_time - start_time) * 1000
            peak_memory_kb += peak_mem / 1024
            
        avg_time_ms /= runs
        peak_memory_kb /= runs
        
        benchmarks.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 1)
        })
        
        print(f"Scale {n}: {avg_time_ms:.3f} ms, {peak_memory_kb:.1f} KB")

    results_file = os.path.join(os.path.dirname(__file__), "results.json")
    
    notes = ""
    emp_time = "O(?)"
    emp_space = "O(?)"
    if os.path.exists(results_file):
        with open(results_file, "r") as f:
            try:
                data = json.load(f)
                notes = data.get("notes", "")
                emp_time = data.get("empirical_time_complexity", "O(?)")
                emp_space = data.get("empirical_space_complexity", "O(?)")
            except Exception:
                pass
                
    result_data = {
        "problem_id": "lc_1438",
        "title": "Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit",
        "topic": "Heap",
        "benchmarks": benchmarks,
        "empirical_time_complexity": emp_time,
        "empirical_space_complexity": emp_space,
        "notes": notes
    }
    
    with open(results_file, "w") as f:
        json.dump(result_data, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
