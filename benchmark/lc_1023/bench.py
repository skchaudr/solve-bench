import json
import os
import sys
import timeit
import tracemalloc
import gc

# Add the repo root to sys.path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1023.solution import Solution

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    out_dir = os.path.dirname(__file__)
    results = []

    for n in scales:
        data_file = os.path.join(out_dir, f"data_{n}.json")
        if not os.path.exists(data_file):
            print(f"Data file not found for scale {n}. Skipping.")
            continue
        
        with open(data_file, "r") as f:
            data = json.load(f)
            
        queries = data["queries"]
        pattern = data["pattern"]
        
        solution = Solution()

        # Warm up
        solution.camelMatch(queries, pattern)

        # Timeit setup
        timer = timeit.Timer(lambda: solution.camelMatch(queries, pattern))
        
        # 3 runs average
        num_runs = 3
        total_time = 0.0
        peak_mem = 0
        
        for _ in range(num_runs):
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            solution.camelMatch(queries, pattern)
            elapsed_time = timeit.default_timer() - start_time
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += elapsed_time
            peak_mem = max(peak_mem, peak)
            
        avg_time_ms = (total_time / num_runs) * 1000
        peak_memory_kb = peak_mem / 1024
        
        results.append({
            "n": n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": peak_memory_kb
        })
        
        print(f"Scale {n}: avg_time_ms={avg_time_ms:.2f}, peak_memory_kb={peak_memory_kb:.2f}")

    # Write partial results directly here for logging purposes, but the results.json update will happen next
    return results

if __name__ == "__main__":
    results = run_benchmarks()
    # Output results to be grabbed by bash
    with open(os.path.join(os.path.dirname(__file__), "raw_results.json"), "w") as f:
        json.dump(results, f)
