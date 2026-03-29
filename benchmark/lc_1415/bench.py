import os
import sys
import time
import json
import tracemalloc

# Add the repository root to sys.path to resolve module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
sys.set_int_max_str_digits(200000)

from benchmark.lc_1415.solution import Solution

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    results = []
    
    # Make sure we don't carry over data memory overhead
    for n in scales:
        with open(f"benchmark/lc_1415/data_{n}.json", "r") as f:
            data = json.load(f)
            # Read k as string and convert back to int to maintain large integer representation
            k = int(data["k"])
        
        sol = Solution()
        
        # Warm-up run
        _ = sol.getHappyString(n, k)
        
        runs = 3
        total_time = 0
        peak_memory = 0
        
        for _ in range(runs):
            import gc
            gc.disable()
            tracemalloc.start()
            
            start_time = time.perf_counter()
            _ = sol.getHappyString(n, k)
            end_time = time.perf_counter()
            
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += (end_time - start_time)
            peak_memory = max(peak_memory, peak)
        
        avg_time_ms = (total_time / runs) * 1000
        peak_memory_kb = peak_memory / 1024
        
        results.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 2),
            "peak_memory_kb": round(peak_memory_kb, 2)
        })
        print(f"n={n}: {avg_time_ms:.2f} ms, {peak_memory_kb:.2f} KB")

    out_file = "benchmark/lc_1415/results.json"
    if os.path.exists(out_file):
        with open(out_file, "r") as f:
            full_results = json.load(f)
    else:
        full_results = {
            "problem_id": "lc_1415",
            "title": "The k-th Lexicographical String of All Happy Strings of Length n",
            "topic": "Backtracking",
            "benchmarks": [],
            "empirical_time_complexity": "O(N)",
            "empirical_space_complexity": "O(N)",
            "notes": "Time and space scale linearly with n because we construct a string of length n bit by bit. Even with Python's large integer conversions, `bin()` format processes all bits linearly, and memory is proportional to the resulting string length."
        }
        
    full_results["benchmarks"] = results
    
    with open(out_file, "w") as f:
        json.dump(full_results, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
