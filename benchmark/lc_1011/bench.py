import json
import timeit
import tracemalloc
import gc
from solution import Solution

def run_benchmarks():
    with open("benchmark/lc_1011/data.json", "r") as f:
        data = json.load(f)
        
    results = {
        "problem_id": "lc_1011",
        "benchmarks": [],
        "empirical_time_complexity": "O(N log(sum(W)))",
        "empirical_space_complexity": "O(1)"
    }
    
    sol = Solution()
    
    for bench in data["benchmarks"]:
        n = bench["n"]
        weights = bench["weights"]
        days = bench["days"]
        
        # Time
        timer = timeit.Timer(lambda: sol.shipWithinDays(weights, days))
        runs = 3
        times = timer.repeat(number=1, repeat=runs)
        avg_time_ms = (sum(times) / runs) * 1000
        
        # Memory
        gc.collect()
        tracemalloc.start()
        sol.shipWithinDays(weights, days)
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_memory_kb = peak_memory / 1024.0
        
        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })
        
    with open("benchmark/lc_1011/results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()