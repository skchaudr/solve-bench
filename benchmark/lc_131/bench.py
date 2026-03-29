import json
import os
import sys
import time
import tracemalloc
import gc

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_131.solution import Solution

def bench():
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset.json")
    with open(dataset_path, "r") as f:
        dataset = json.load(f)

    results = []
    
    for data in dataset:
        n = data["n"]
        s_val = data["s"]
        
        times = []
        peaks = []
        
        for _ in range(3):
            sol = Solution()
            
            gc.collect()
            gc.disable()
            tracemalloc.start()
            
            t0 = time.time()
            res = sol.partition(s_val)
            t1 = time.time()
            
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            times.append((t1 - t0) * 1000)
            peaks.append(peak / 1024)
            
        avg_time = sum(times) / len(times)
        avg_peak = sum(peaks) / len(peaks)
        
        results.append({
            "n": n,
            "avg_time_ms": round(avg_time, 2),
            "peak_memory_kb": round(avg_peak, 2)
        })
        print(f"n={n} (length={len(s_val)}): time={avg_time:.2f}ms, mem={avg_peak:.2f}KB")
        
    out_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(out_path, "w") as f:
        json.dump({
            "problem_id": "lc_131",
            "title": "Palindrome Partitioning",
            "topic": "Backtracking",
            "benchmarks": results,
            "empirical_time_complexity": "O(N * 2^N)",
            "empirical_space_complexity": "O(N * 2^N)",
            "notes": "Time and space complexities are driven by the 2^(N-1) possible partitions, with each taking O(N) space. Mapped inputs N=100, 1000, 10000, 100000 to lengths 12, 14, 16, 18."
        }, f, indent=2)

if __name__ == "__main__":
    bench()
