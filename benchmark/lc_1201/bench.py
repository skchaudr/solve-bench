import json
import time
import tracemalloc
import sys

# Add current directory to path so we can import solution
sys.path.append('.')

from solution import Solution

def run_benchmark():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []
    
    for scale in scales:
        with open(f"benchmark/lc_1201/data_{scale}.json", "r") as f:
            data = json.load(f)
            
        n = data["n"]
        a = data["a"]
        b = data["b"]
        c = data["c"]
        
        runs = 3
        total_time = 0
        peak_memory = 0
        
        for _ in range(runs):
            
            tracemalloc.start()
            start_time = time.perf_counter()
            
            Solution().nthUglyNumber(n, a, b, c)
                    
            end_time = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            
            total_time += (end_time - start_time)
            peak_memory = max(peak_memory, peak)
            
        avg_time_ms = (total_time / runs) * 1000
        peak_memory_kb = peak_memory / 1024
        
        benchmarks.append({
            "n": scale,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })
        
    results = {
        "problem_id": "lc_1201",
        "title": "Ugly Number III",
        "topic": "Binary Search",
        "benchmarks": benchmarks,
        "empirical_time_complexity": "O(log(MAX_ANS))",
        "empirical_space_complexity": "O(1)",
        "notes": "Time complexity is empirical O(log(MAX_ANS)) which remains constant irrespective of 'N' because binary search boundaries are fixed. Space complexity is O(1)."
    }
    
    with open("benchmark/lc_1201/results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmark()
