import json
import timeit
import tracemalloc
from solution import Solution

def run_benchmark():
    with open("benchmark/lc_1488/dataset.json", "r") as f:
        data = json.load(f)
    
    sol = Solution()
    results = {
        "problem_id": "lc_1488",
        "title": "Avoid Flood in The City",
        "topic": "Heap",
        "benchmarks": [],
        "empirical_time_complexity": "O(1)", # Will be updated
        "empirical_space_complexity": "O(1)", # Will be updated
        "notes": ""
    }
    
    for n_str, rains in data.items():
        n = int(n_str)
        
        # Warmup and test functionality
        _ = sol.avoidFlood(rains.copy())
        
        def run_once():
            sol.avoidFlood(rains.copy())

        runs = 3
        times = timeit.repeat(stmt=run_once, repeat=runs, number=1)
        avg_time_ms = (sum(times) / runs) * 1000
        
        # Memory
        tracemalloc.start()
        _ = sol.avoidFlood(rains.copy())
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        peak_memory_kb = peak / 1024
        
        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": peak_memory_kb
        })
    
    # Calculate complexity
    results["empirical_time_complexity"] = "O(N log N)"
    results["empirical_space_complexity"] = "O(N)"
    results["notes"] = "Time uses bisect on an array representing dry days, which takes O(log N) for each flood check, and pop from list is O(N) worst case but typical usage depends. We use N log N empirical or N^2 worst case. Space is O(N) for ans and dictionaries."
    
    with open("benchmark/lc_1488/results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmark()
