import json
import os
import sys
import timeit
import tracemalloc
import gc

# Add repository root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_17.solution import Solution

def run_benchmarks():
    with open(os.path.join(os.path.dirname(__file__), "test_cases.json"), "r") as f:
        datasets = json.load(f)

    results = []
    
    for data in datasets:
        n = data["n"]
        real_n = data["real_n"]
        digits = data["digits"]
        
        sol = Solution()
        
        times = []
        peak_mems = []
        
        for _ in range(3):
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            _res = sol.letterCombinations(digits)
            end_time = timeit.default_timer()
            
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            times.append(end_time - start_time)
            peak_mems.append(peak_mem)
            
        avg_time_ms = (sum(times) / 3) * 1000
        avg_mem_kb = (sum(peak_mems) / 3) / 1024
        
        results.append({
            "n": n,
            "real_n": real_n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": avg_mem_kb
        })
        
        print(f"n={n} (real_n={real_n}): {avg_time_ms:.2f} ms | {avg_mem_kb:.2f} KB")

    res_json = {
        "problem_id": "lc_17",
        "title": "Letter Combinations of a Phone Number",
        "topic": "Backtracking",
        "benchmarks": [
            {"n": r["n"], "avg_time_ms": round(r["avg_time_ms"], 3), "peak_memory_kb": round(r["peak_memory_kb"], 3)} for r in results
        ],
        "empirical_time_complexity": "O(?)",
        "empirical_space_complexity": "O(?)",
        "notes": "real_n scales: " + str([r["real_n"] for r in results])
    }
    
    with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
        json.dump(res_json, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
