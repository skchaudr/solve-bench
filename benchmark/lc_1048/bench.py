import os
import json
import timeit
import tracemalloc
import gc
from typing import List
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_1048.solution import Solution

def run_benchmark(n: int) -> dict:
    file_path = f"benchmark/lc_1048/data_{n}.json"
    with open(file_path, 'r') as f:
        data = json.load(f)

    solution = Solution()
    
    # Pre-run to warmup and check if it runs
    try:
        solution.longestStrChain(data[:])
    except Exception as e:
        print(f"Error during execution for n={n}: {e}")
        return {
            "n": n,
            "avg_time_ms": 0.0,
            "peak_memory_kb": 0.0
        }

    times = []
    peak_memories = []

    # 3 runs average
    runs = 3
    for _ in range(runs):
        data_copy = data[:]
        
        gc.disable()
        tracemalloc.start()
        
        start_time = timeit.default_timer()
        solution.longestStrChain(data_copy)
        end_time = timeit.default_timer()
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        gc.enable()
        gc.collect()

        times.append((end_time - start_time) * 1000)
        peak_memories.append(peak / 1024)

    avg_time = sum(times) / runs
    avg_memory = sum(peak_memories) / runs

    return {
        "n": n,
        "avg_time_ms": round(avg_time, 4),
        "peak_memory_kb": round(avg_memory, 4)
    }

def main():
    sizes = [100, 1000, 10000, 100000]
    benchmarks = []

    for n in sizes:
        print(f"Benchmarking for n={n}...")
        result = run_benchmark(n)
        benchmarks.append(result)
        print(f"n={n}: Time: {result['avg_time_ms']} ms, Memory: {result['peak_memory_kb']} KB")

    results_path = "benchmark/lc_1048/results.json"
    
    # Ensure file exists or create boilerplate
    if not os.path.exists(results_path):
        initial_results = {
            "problem_id": "lc_1048",
            "title": "Longest String Chain",
            "topic": "Two Pointers",
            "benchmarks": [],
            "empirical_time_complexity": "O(?)",
            "empirical_space_complexity": "O(?)",
            "notes": "reasoning based on timing ratios"
        }
    else:
        with open(results_path, 'r') as f:
            initial_results = json.load(f)
            
    initial_results["benchmarks"] = benchmarks
    
    with open(results_path, 'w') as f:
        json.dump(initial_results, f, indent=2)
        
    print("Benchmark complete. Results written to results.json.")

if __name__ == "__main__":
    main()
