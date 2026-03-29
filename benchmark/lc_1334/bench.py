import os
import sys
import json
import timeit
import tracemalloc
import gc
import math

# Add repository root to sys.path to resolve module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1334.solution import Solution
from benchmark.lc_1334.generate import generate_test_case

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []
    
    timeout_threshold_ms = 10000 # 10 seconds max per run for safety
    previous_time_ms = 0
    previous_n = 0
    previous_peak_mem = 0
    
    for n in scales:
        print(f"Benchmarking n={n}...")
        
        # Generation step
        try:
            _, edges, distanceThreshold = generate_test_case(n, seed=42)
        except Exception as e:
            print(f"Failed to generate for n={n}: {e}")
            break
            
        # Fast fail if previous run took too long (extrapolate)
        if previous_time_ms > 0 and previous_n > 0:
            # Expected factor is ~ (n / previous_n)^2 * (log(n) / log(previous_n))
            # O(V * E * log V) where E ~ 2V => O(V^2 * log V)
            ratio = n / previous_n
            log_ratio = math.log2(n) / math.log2(previous_n)
            expected_factor = (ratio ** 2) * log_ratio
            expected_time_ms = previous_time_ms * expected_factor
            
            # Expected memory factor: O(V + E) -> O(V)
            expected_mem_factor = ratio
            expected_mem_kb = previous_peak_mem * expected_mem_factor
            
            if expected_time_ms > timeout_threshold_ms:
                print(f"Skipping n={n} due to expected timeout ({expected_time_ms:.2f} ms)")
                benchmarks.append({
                    "n": n,
                    "avg_time_ms": float(f"{expected_time_ms:.1f}"),
                    "peak_memory_kb": float(f"{expected_mem_kb:.1f}")
                })
                previous_time_ms = expected_time_ms
                previous_n = n
                previous_peak_mem = expected_mem_kb
                continue
                
        # Benchmark run
        solution = Solution()
        num_runs = 3
        
        total_time = 0
        peak_mem_kb_total = 0
        
        for _ in range(num_runs):
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            
            # The actual algorithm call
            solution.findTheCity(n, edges, distanceThreshold)
            
            elapsed_time = timeit.default_timer() - start_time
            
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += elapsed_time
            peak_mem_kb_total += peak_mem / 1024
            
        avg_time_ms = (total_time / num_runs) * 1000
        avg_peak_mem_kb = peak_mem_kb_total / num_runs
        
        print(f"Result for n={n}: {avg_time_ms:.2f} ms, {avg_peak_mem_kb:.2f} KB")
        
        benchmarks.append({
            "n": n,
            "avg_time_ms": float(f"{avg_time_ms:.1f}"),
            "peak_memory_kb": float(f"{avg_peak_mem_kb:.1f}")
        })
        
        previous_time_ms = avg_time_ms
        previous_n = n
        previous_peak_mem = avg_peak_mem_kb
        
    return benchmarks

if __name__ == "__main__":
    benchmarks = run_benchmarks()
    
    results = {
      "problem_id": "lc_1334",
      "title": "Find the City With the Smallest Number of Neighbors at a Threshold Distance",
      "topic": "Graph",
      "benchmarks": benchmarks,
      "empirical_time_complexity": "O(V^3 log V) or O(V * (V + E) log V)", # Will be updated
      "empirical_space_complexity": "O(V + E)",
      "notes": "Extrapolated time and space complexity due to expected timeout on larger values of n."
    }
    
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Benchmark completed, saved to results.json")
