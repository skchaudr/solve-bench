import json
import os
import sys
import timeit
import tracemalloc
import gc

# Add the repo root to sys.path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1498.solution import Solution

def run_benchmark():
    scales = [100, 1000, 10000, 100000]
    results = []
    
    script_dir = os.path.dirname(__file__)
    
    for n in scales:
        data_file = os.path.join(script_dir, f"data_{n}.json")
        with open(data_file, "r") as f:
            data = json.load(f)
            
        nums = data["nums"]
        target = data["target"]
        
        runs = 3
        times = []
        peak_memories = []
        
        for _ in range(runs):
            # We copy nums because the solution mutates it (sorts it)
            nums_copy = nums.copy()
            
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            
            # Execute the solution
            Solution().numSubseq(nums_copy, target)
            
            elapsed_time = timeit.default_timer() - start_time
            
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            times.append(elapsed_time)
            peak_memories.append(peak_mem)
            
        avg_time_ms = (sum(times) / runs) * 1000.0
        # Peak memory in KB
        peak_memory_kb = max(peak_memories) / 1024.0
        
        results.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })
        
        print(f"n={n}: avg_time_ms={avg_time_ms:.3f}, peak_memory_kb={peak_memory_kb:.3f}")
        
    # Write initial results to results.json
    results_file = os.path.join(script_dir, "results.json")
    
    # Check if results.json exists and read it, to update only the benchmarks field
    if os.path.exists(results_file):
        with open(results_file, "r") as f:
            output_data = json.load(f)
    else:
        output_data = {
            "problem_id": "lc_1498",
            "title": "Number of Subsequences That Satisfy the Given Sum Condition",
            "topic": "Two Pointers",
            "benchmarks": [],
            "empirical_time_complexity": "O(?)",
            "empirical_space_complexity": "O(?)",
            "notes": ""
        }
        
    output_data["benchmarks"] = results
    
    with open(results_file, "w") as f:
        json.dump(output_data, f, indent=2)

if __name__ == "__main__":
    run_benchmark()
