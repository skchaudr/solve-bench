import json
import timeit
import tracemalloc
import os
import sys
import gc

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_1297.solution import Solution

def run_benchmarks():
    data_path = os.path.join(os.path.dirname(__file__), "data.json")
    with open(data_path, "r") as f:
        data = json.load(f)
        
    results = []
    
    for n_str, params in data.items():
        n = int(n_str)
        s = params["s"]
        maxLetters = params["maxLetters"]
        minSize = params["minSize"]
        maxSize = params["maxSize"]
        
        runs = 3
        total_time = 0
        peak_memory = 0
        
        sol = Solution()
        
        for _ in range(runs):
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            sol.maxFreq(s, maxLetters, minSize, maxSize)
            end_time = timeit.default_timer()
            
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += (end_time - start_time)
            peak_memory = max(peak_memory, peak)
            
        avg_time_ms = (total_time / runs) * 1000
        peak_memory_kb = peak_memory / 1024
        
        results.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })
        
        print(f"n={n}: {avg_time_ms:.3f} ms, {peak_memory_kb:.3f} KB")
        
    results_path = os.path.join(os.path.dirname(__file__), "results.json")
    
    # Try reading existing
    existing_data = {
        "problem_id": "lc_1297",
        "title": "Maximum Number of Occurrences of a Substring",
        "topic": "Sliding Window",
        "benchmarks": [],
        "empirical_time_complexity": "O(?)",
        "empirical_space_complexity": "O(?)",
        "notes": ""
    }
    
    if os.path.exists(results_path):
        with open(results_path, "r") as f:
            try:
                existing_data = json.load(f)
            except:
                pass
                
    existing_data["benchmarks"] = results
    
    with open(results_path, "w") as f:
        json.dump(existing_data, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
