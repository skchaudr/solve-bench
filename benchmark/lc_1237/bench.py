import sys
import os
import json
import timeit
import tracemalloc
import gc

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1237.solution import Solution
from benchmark.lc_1237.generate import generate_data

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []
    
    for n in scales:
        print(f"Benchmarking n = {n}...")
        
        # Prepare data
        data = generate_data(n)
        customfunction = data["customfunction"]
        z = data["z"]
        
        # Warmup and test instance creation
        sol = Solution()
        
        total_time = 0
        peak_mem = 0
        runs = 3
        
        for _ in range(runs):
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            
            # Execute solution
            res = sol.findSolution(customfunction, z)
            
            end_time = timeit.default_timer()
            
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += (end_time - start_time)
            peak_mem = max(peak_mem, peak)
            
        avg_time_ms = (total_time / runs) * 1000
        peak_mem_kb = peak_mem / 1024
        
        benchmarks.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 4),
            "peak_memory_kb": round(peak_mem_kb, 4)
        })
        
        print(f"  Avg Time: {avg_time_ms:.4f} ms")
        print(f"  Peak Mem: {peak_mem_kb:.4f} KB")

    # Read existing or create base template
    results_path = os.path.join(os.path.dirname(__file__), "results.json")
    results = {
        "problem_id": "lc_1237",
        "title": "Find Positive Integer Solution for a Given Equation",
        "topic": "Two Pointers",
        "benchmarks": benchmarks,
        "empirical_time_complexity": "O(?)",
        "empirical_space_complexity": "O(?)",
        "notes": "reasoning based on timing ratios"
    }

    if os.path.exists(results_path):
        with open(results_path, "r") as f:
            try:
                existing_results = json.load(f)
                existing_results["benchmarks"] = benchmarks
                results = existing_results
            except json.JSONDecodeError:
                pass

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
