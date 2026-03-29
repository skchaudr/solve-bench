import sys
import os
import gc
import timeit
import tracemalloc

# Configure sys.path to allow absolute imports from repository root
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1016.solution import Solution
from benchmark.lc_1016.generate import generate_data

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    results = []

    for n in scales:
        print(f"Generating data for N={n}...")
        s, target_n = generate_data(n)
        
        sol = Solution()

        runs = 3
        total_time = 0.0
        peak_memory = 0

        for _ in range(runs):
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            
            # Call the solution
            _ = sol.queryString(s, target_n)
            
            end_time = timeit.default_timer()
            
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += (end_time - start_time)
            peak_memory = max(peak_memory, peak)
            
        avg_time_ms = (total_time / runs) * 1000
        peak_memory_kb = peak_memory / 1024
        
        print(f"N={n} -> avg_time_ms: {avg_time_ms:.4f}, peak_memory_kb: {peak_memory_kb:.2f}")
        
        results.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 4),
            "peak_memory_kb": round(peak_memory_kb, 2)
        })

    print("Benchmarks complete.")
    for res in results:
        print(res)
        
    import json
    results_path = os.path.join(os.path.dirname(__file__), 'results.json')
    if os.path.exists(results_path):
        with open(results_path, 'r') as f:
            data = json.load(f)
        data['benchmarks'] = results
        with open(results_path, 'w') as f:
            json.dump(data, f, indent=2)
            f.write('\n')

if __name__ == "__main__":
    run_benchmarks()
