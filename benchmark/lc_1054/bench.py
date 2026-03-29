import os
import sys
import timeit
import tracemalloc
import gc
import json

# Add repository root to sys.path to resolve module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1054.solution import Solution
from benchmark.lc_1054.generate import generate_data

def run_benchmarks():
    sizes = [100, 1000, 10000, 100000]
    results = []
    
    for n in sizes:
        # Generate data once per scale
        barcodes = generate_data(n)
        
        # We need 3 runs
        runs = 3
        total_time = 0.0
        peak_mem = 0
        
        for _ in range(runs):
            # Pass a copy of the data since solution rearranges in-place implicitly
            data_copy = barcodes.copy()
            sol = Solution()
            
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            sol.rearrangeBarcodes(data_copy)
            end_time = timeit.default_timer()
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += (end_time - start_time)
            peak_mem = max(peak_mem, peak)
            
        avg_time_ms = (total_time / runs) * 1000
        peak_memory_kb = peak_mem / 1024.0
        
        results.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })
        
        print(f"n={n}: {avg_time_ms:.3f} ms, {peak_memory_kb:.3f} KB")
        
    # Write to results.json
    results_path = os.path.join(os.path.dirname(__file__), "results.json")
    
    # Read existing results if it exists, otherwise initialize empty
    try:
        with open(results_path, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {
            "problem_id": "lc_1054",
            "title": "Distant Barcodes",
            "topic": "Heap",
            "benchmarks": [],
            "empirical_time_complexity": "O(?)",
            "empirical_space_complexity": "O(?)",
            "notes": ""
        }
        
    data["benchmarks"] = results
    
    with open(results_path, "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
