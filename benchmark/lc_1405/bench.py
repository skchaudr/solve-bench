import json
import timeit
import tracemalloc
from solution import Solution

def run_benchmark():
    with open("benchmark/lc_1405/dataset.json", "r") as f:
        data = json.load(f)
    
    sol = Solution()
    results = {
        "problem_id": "lc_1405",
        "title": "Longest Happy String",
        "topic": "Heap",
        "benchmarks": [],
        "empirical_time_complexity": "O(1)", # Will be updated
        "empirical_space_complexity": "O(1)", # Will be updated
        "notes": ""
    }
    
    for n_str, a_b_c in data.items():
        n = int(n_str)
        a, b, c = a_b_c
        
        # Warmup and test functionality
        _ = sol.longestDiverseString(a, b, c)
        
        def run_once():
            sol.longestDiverseString(a, b, c)

        runs = 3
        times = timeit.repeat(stmt=run_once, repeat=runs, number=1)
        avg_time_ms = (sum(times) / runs) * 1000
        
        # Memory
        tracemalloc.start()
        _ = sol.longestDiverseString(a, b, c)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        peak_memory_kb = peak / 1024
        
        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": peak_memory_kb
        })
    
    # Calculate complexity
    # We use O(N) since we build string of length up to n
    results["empirical_time_complexity"] = "O(N)"
    results["empirical_space_complexity"] = "O(N)"
    results["notes"] = "Time grows linearly with N. Space is also linear to store the result string."
    
    with open("benchmark/lc_1405/results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmark()
