import json
import time
import tracemalloc
import os
from solution import Solution

def run():
    with open("dataset.json", "r") as f:
        data = json.load(f)
        
    results = {
        "problem_id": "lc_1338",
        "title": "Reduce Array Size to The Half",
        "topic": "Heap",
        "benchmarks": [],
        "empirical_time_complexity": "O(N log N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Counting frequencies is O(N) time and O(U) space. Sorting the frequencies is O(U log U), where U is unique elements. Space is O(U) bounded by O(N)."
    }
    
    sol = Solution()
    
    for n_str in ["100", "1000", "10000", "100000"]:
        if n_str not in data:
            continue
        kwargs = data[n_str]
        arr = kwargs["arr"]
        n = kwargs["n"]
        
        sol.minSetSize(arr)
        
        runs = 3
        times = []
        peaks = []
        
        for _ in range(runs):
            tracemalloc.start()
            start = time.perf_counter()
            sol.minSetSize(arr)
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
