import time
import tracemalloc
import gc
import json
import os
import sys

# Append the repository root so absolute imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1239.solution import Solution
from benchmark.lc_1239.generate import generate_data

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    results = []

    for n in scales:
        arr = generate_data(n)
        sol = Solution()

        runs = 3
        total_time = 0.0
        peak_memory = 0

        for _ in range(runs):
            # To ensure the algorithm gets a clean list of inputs and no cached side-effects
            run_arr = arr.copy()
            
            gc.disable()
            tracemalloc.start()
            
            start_time = time.perf_counter()
            sol.maxLength(run_arr)
            end_time = time.perf_counter()
            
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += (end_time - start_time)
            peak_memory = max(peak_memory, peak)
            
        avg_time_ms = (total_time / runs) * 1000
        peak_memory_kb = peak_memory / 1024

        print(f"n={n}: {avg_time_ms:.2f} ms, {peak_memory_kb:.2f} KB")

        results.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })

    # Prepare JSON structure
    json_path = os.path.join(os.path.dirname(__file__), 'results.json')
    
    # Read existing if exists
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            data = json.load(f)
    else:
        data = {
            "problem_id": "lc_1239",
            "title": "Maximum Length of a Concatenated String with Unique Characters",
            "topic": "Backtracking",
            "benchmarks": [],
            "empirical_time_complexity": "O(?)",
            "empirical_space_complexity": "O(?)",
            "notes": "reasoning based on timing ratios"
        }
    
    data["benchmarks"] = results

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)

if __name__ == '__main__':
    run_benchmarks()
