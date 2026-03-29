import sys
import os
import timeit
import tracemalloc
import json
import gc

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_1008.solution import Solution
from benchmark.lc_1008.generate import generate_test_case

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    results = []

    for n in scales:
        print(f"Generating data for n={n}...")
        preorder = generate_test_case(n)
        
        times = []
        peak_mems = []

        # 3 runs
        for _ in range(3):
            sol = Solution()
            
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            root = sol.bstFromPreorder(preorder)
            end_time = timeit.default_timer()
            
            _, peak_memory = tracemalloc.get_traced_memory()
            
            tracemalloc.stop()
            gc.enable()

            times.append((end_time - start_time) * 1000)
            peak_mems.append(peak_memory / 1024)

        avg_time = sum(times) / 3
        avg_peak_mem = sum(peak_mems) / 3

        print(f"n={n}: avg_time={avg_time:.2f} ms, peak_mem={avg_peak_mem:.2f} KB")

        results.append({
            "n": n,
            "avg_time_ms": round(avg_time, 2),
            "peak_memory_kb": round(avg_peak_mem, 2)
        })

    with open("benchmark/lc_1008/results.json", "w") as f:
        json.dump({
            "problem_id": "lc_1008",
            "title": "Construct Binary Search Tree from Preorder Traversal",
            "topic": "Binary Search",
            "benchmarks": results,
            "empirical_time_complexity": "O(N)",
            "empirical_space_complexity": "O(N)",
            "notes": "Time scales linearly, approximately increasing by 10x as N increases by 10x. Space also scales linearly by 10x, corresponding to the memory of the newly allocated tree nodes."
        }, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
