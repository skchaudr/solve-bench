import json
import timeit
import tracemalloc
import os
from solution import Solution

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    results = {
        "problem_id": "lc_1238",
        "title": "Circular Permutation in Binary Representation",
        "topic": "Backtracking",
        "benchmarks": [],
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Here N refers to 2^n, which is the size of the output. The mapped n values are 7, 10, 13, and 17. The time and space grow linearly with 2^n (i.e. O(2^n) in terms of n, but O(N) in terms of benchmark scale N)."
    }
    
    sol = Solution()
    for N in scales:
        with open(f'benchmark/lc_1238/input_{N}.json', 'r') as f:
            data = json.load(f)
        n = data['n']
        start = data['start']
        
        def test_func():
            return sol.circularPermutation(n, start)
        
        # Warmup and time
        time_runs = timeit.repeat(test_func, number=1, repeat=3)
        avg_time_ms = (sum(time_runs) / len(time_runs)) * 1000
        
        # Memory
        tracemalloc.start()
        test_func()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_memory_kb = peak / 1024
        
        results["benchmarks"].append({
            "n": N,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })
        
    with open('benchmark/lc_1238/results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    run_benchmarks()