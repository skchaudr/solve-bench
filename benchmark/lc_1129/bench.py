import json
import time
import tracemalloc
import os
from solution import Solution

def run():
    with open("dataset.json", "r") as f:
        data = json.load(f)
        
    results = {
        "problem_id": "lc_1129",
        "title": "Shortest Path with Alternating Colors",
        "topic": "Graph",
        "benchmarks": [],
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Time and space scale linearly with the number of nodes and edges. Since E is O(N) here, it's O(N) overall."
    }
    
    sol = Solution()
    
    for n_str in ["100", "1000", "10000", "100000"]:
        if n_str not in data:
            continue
        kwargs = data[n_str]
        n = kwargs["n"]
        redEdges = kwargs["redEdges"]
        blueEdges = kwargs["blueEdges"]
        
        # Warmup
        sol.shortestAlternatingPaths(n, redEdges, blueEdges)
        
        runs = 3
        times = []
        peaks = []
        
        for _ in range(runs):
            tracemalloc.start()
            start = time.perf_counter()
            sol.shortestAlternatingPaths(n, redEdges, blueEdges)
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
