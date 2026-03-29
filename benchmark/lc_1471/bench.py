import json
import os
import sys
import timeit
import tracemalloc
import gc

# Add the repository root to sys.path to enable absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1471.solution import Solution

def benchmark():
    scales = [100, 1000, 10000, 100000]
    data_dir = os.path.dirname(os.path.abspath(__file__))
    
    results = {
        "problem_id": "lc_1471",
        "title": "The k Strongest Values in an Array",
        "topic": "Two Pointers",
        "benchmarks": [],
        "empirical_time_complexity": "O(?)",
        "empirical_space_complexity": "O(?)",
        "notes": ""
    }
    
    solution = Solution()
    
    for n in scales:
        file_path = os.path.join(data_dir, f"data_{n}.json")
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        arr = data["arr"]
        k = data["k"]
        
        # Time benchmarking
        # Setup for timeit
        setup_code = "from __main__ import Solution\nsolution = Solution()\n"
        # Since solution modifies arr in place (sorting it), we need to copy it for each run
        stmt_code = f"temp_arr = {arr}.copy(); solution.getStrongest(temp_arr, {k})"
        
        # Run 3 times, average time in milliseconds
        times = timeit.repeat(stmt=stmt_code, setup=setup_code, repeat=3, number=1)
        avg_time_ms = (sum(times) / len(times)) * 1000
        
        # Memory benchmarking
        # We also need to copy arr before calling getStrongest, but we should measure memory usage
        # including the copy since sorting in Python inherently uses O(N) memory
        # Tracemalloc might capture Timsort memory usage when sorting
        peak_mem_kb_list = []
        for _ in range(3):
            gc.disable()
            temp_arr = arr.copy()
            tracemalloc.start()
            
            solution.getStrongest(temp_arr, k)
            
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            peak_mem_kb_list.append(peak_mem / 1024)
            
        avg_peak_mem_kb = sum(peak_mem_kb_list) / len(peak_mem_kb_list)
        
        print(f"n={n}: avg_time={avg_time_ms:.4f} ms, peak_mem={avg_peak_mem_kb:.2f} KB")
        
        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": avg_peak_mem_kb
        })
        
    results_path = os.path.join(data_dir, "results.json")
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    benchmark()
