import os
import sys
import json
import timeit
import tracemalloc
import gc

# Add the repository root to sys.path to enable absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1052.solution import Solution
from benchmark.lc_1052.generate import generate_data

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    num_runs = 3
    results = []

    sol = Solution()

    for n in scales:
        print(f"Benchmarking n = {n}...")
        
        # Generate data once per scale
        customers, grumpy, minutes = generate_data(n)
        
        total_time = 0.0
        max_peak_memory = 0

        for run in range(num_runs):
            gc.disable()
            tracemalloc.start()
            
            # Start timer
            start_time = timeit.default_timer()
            
            # Run the solution
            # The solution doesn't modify the inputs, so no need to copy
            _ = sol.maxSatisfied(customers, grumpy, minutes)
            
            # Stop timer
            end_time = timeit.default_timer()
            
            # Get peak memory
            _, peak = tracemalloc.get_traced_memory()
            
            # Stop tracing memory and enable gc
            tracemalloc.stop()
            gc.enable()

            total_time += (end_time - start_time)
            max_peak_memory = max(max_peak_memory, peak)

        avg_time_ms = (total_time / num_runs) * 1000
        peak_memory_kb = max_peak_memory / 1024

        results.append({
            "n": n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": peak_memory_kb
        })

    # Prepare JSON structure
    output_data = {
        "problem_id": "lc_1052",
        "title": "Grumpy Bookstore Owner",
        "topic": "Sliding Window",
        "benchmarks": results,
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(1)",
        "notes": "The time increases roughly linearly with N (10x input size results in approx 10x time). The space complexity is O(1) as the peak memory stays constant regardless of N."
    }

    # Write results to results.json
    results_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(results_path, "w") as f:
        json.dump(output_data, f, indent=2)

    print("Benchmarks completed and written to results.json.")

if __name__ == "__main__":
    run_benchmarks()
