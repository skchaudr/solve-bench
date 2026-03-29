import os
import sys
import json
import timeit
import tracemalloc
import gc

# Add the repo root to sys.path to allow imports like `from benchmark.lc_1268.solution import Solution`
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1268.solution import Solution
from benchmark.lc_1268.generate import generate_data

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    runs = 3
    results = []

    for n in scales:
        print(f"Benchmarking n={n}...")
        
        products, searchWord = generate_data(n)
        
        total_time = 0.0
        peak_mem = 0
        
        for _ in range(runs):
            sol = Solution()
            
            # Use a copy of products for each run since the solution sorts them in-place
            test_products = list(products)
            
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            sol.suggestedProducts(test_products, searchWord)
            end_time = timeit.default_timer()
            
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += (end_time - start_time)
            peak_mem = max(peak_mem, peak)
            
        avg_time_ms = (total_time / runs) * 1000
        peak_mem_kb = peak_mem / 1024
        
        results.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_mem_kb, 3)
        })
        print(f"  n={n} -> {avg_time_ms:.3f} ms, {peak_mem_kb:.3f} KB")

    # Load results.json if it exists and update the benchmarks array
    results_path = os.path.join(os.path.dirname(__file__), "results.json")
    if os.path.exists(results_path):
        with open(results_path, 'r') as f:
            data = json.load(f)
            
        data['benchmarks'] = results
        
        with open(results_path, 'w') as f:
            json.dump(data, f, indent=2)
    else:
        print("Warning: results.json not found, skipping update.")

if __name__ == "__main__":
    run_benchmarks()
