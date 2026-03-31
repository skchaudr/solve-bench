import json
import time
import tracemalloc
import os
from solution import Solution

def run():
    with open("dataset.json", "r") as f:
        data = json.load(f)
        
    results = {
        "problem_id": "lc_1319",
        "title": "Number of Operations to Make Network Connected",
        "topic": "Graph",
        "benchmarks": [],
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Union-Find operations with path compression take nearly constant time \\u03b1(N). Iterating through E edges gives O(E \\u03b1(N)) time. Space is O(N) for parent tracking."
    }
    
    sol = Solution()
    
    for n_str in ["100", "1000", "10000", "100000"]:
        if n_str not in data:
            continue
        kwargs = data[n_str]
        n = kwargs["n"]
        connections = kwargs["connections"]
        
        sol.makeConnected(n, connections)
        
        runs = 3
        times = []
        peaks = []
        
        for _ in range(runs):
            tracemalloc.start()
            start = time.perf_counter()
            sol.makeConnected(n, connections)
            end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            times.append(end - start)
            peaks.append(peak)
            
        avg_time_ms = (sum(times) / runs) * 1000
        peak_memory_kb = max(peaks) / 1024
        
        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })
        
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run()
