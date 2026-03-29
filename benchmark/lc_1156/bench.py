import sys
import os
import timeit
import tracemalloc
import json

# Add repository root to sys.path to resolve imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1156.solution import Solution
from benchmark.lc_1156.generate import generate_data

def run_benchmark():
    sizes = [100, 1000, 10000, 100000]
    runs = 3
    results = []

    sol = Solution()

    for n in sizes:
        print(f"Benchmarking n={n}...")
        test_str = generate_data(n)
        
        # Warmup and test correctness
        _ = sol.maxRepOpt1(test_str)
        
        total_time = 0
        peak_mem = 0
        
        import gc
        
        for _ in range(runs):
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            sol.maxRepOpt1(test_str)
            elapsed = timeit.default_timer() - start_time
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += elapsed
            peak_mem = max(peak_mem, peak)
            
        avg_time_ms = (total_time / runs) * 1000
        peak_memory_kb = peak_mem / 1024
        
        results.append({
            "n": n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": peak_memory_kb
        })
        print(f"n={n}: {avg_time_ms:.3f} ms, {peak_memory_kb:.2f} KB")

    return results

if __name__ == "__main__":
    benchmarks = run_benchmark()
    
    # Write initial results template to results.json
    results_path = os.path.join(os.path.dirname(__file__), "results.json")
    
    if os.path.exists(results_path):
        with open(results_path, "r") as f:
            data = json.load(f)
    else:
        data = {
            "problem_id": "lc_1156",
            "title": "Swap For Longest Repeated Character Substring",
            "topic": "Sliding Window",
            "empirical_time_complexity": "O(?)",
            "empirical_space_complexity": "O(?)",
            "notes": "reasoning based on timing ratios"
        }
        
    data["benchmarks"] = benchmarks
    
    with open(results_path, "w") as f:
        json.dump(data, f, indent=2)
    print("Results written to results.json")
