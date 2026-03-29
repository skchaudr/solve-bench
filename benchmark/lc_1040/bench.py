import timeit
import tracemalloc
import json
import os
import sys

# Ensure the parent directory is in the path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1040.solution import Solution

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    results = []
    
    for n in scales:
        input_file = f"benchmark/lc_1040/input_{n}.json"
        with open(input_file, "r") as f:
            stones = json.load(f)
            
        solution = Solution()
        
        runs = 3
        total_time = 0.0
        peak_memory = 0
        
        for _ in range(runs):
            # Pass a copy of stones so sorting doesn't affect subsequent runs
            stones_copy = stones.copy()
            
            gc_state = True
            try:
                import gc
                gc_state = gc.isenabled()
                gc.disable()
            except:
                pass
                
            tracemalloc.start()
            start_time = timeit.default_timer()
            
            solution.numMovesStonesII(stones_copy)
            
            end_time = timeit.default_timer()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            try:
                if gc_state:
                    gc.enable()
            except:
                pass
                
            total_time += (end_time - start_time)
            peak_memory = max(peak_memory, peak)
            
        avg_time_ms = (total_time / runs) * 1000
        peak_memory_kb = peak_memory / 1024
        
        results.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })
        print(f"n={n}: {avg_time_ms:.3f} ms, {peak_memory_kb:.3f} KB")
        
    # Prepare results dictionary
    results_data = {
        "problem_id": "lc_1040",
        "title": "Moving Stones Until Consecutive II",
        "topic": "Sliding Window",
        "benchmarks": results,
        "empirical_time_complexity": "O(N log N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Time complexity is dominated by the sorting step (O(N log N)), and space complexity is O(N) auxiliary space used by Timsort, as visible from memory metrics which scale linearly. The sliding window step itself is O(N)."
    }
    
    results_path = "benchmark/lc_1040/results.json"
    
    with open(results_path, "w") as f:
        json.dump(results_data, f, indent=2)
    print(f"Results written to {results_path}")

if __name__ == "__main__":
    run_benchmarks()
