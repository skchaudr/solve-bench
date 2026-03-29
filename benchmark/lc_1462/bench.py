import sys
import os
import json
import timeit
import tracemalloc
import gc

# Append the repository root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1462.solution import Solution
from benchmark.lc_1462.generate import generate_data

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []
    
    sol = Solution()
    
    for n in scales:
        print(f"Benchmarking n={n}...")
        
        numCourses, prerequisites, queries = generate_data(n)
        
        time_runs = []
        mem_runs = []
        
        for _ in range(3):
            gc.collect()
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            
            # Execute
            sol.checkIfPrerequisite(numCourses, prerequisites, queries)
            
            end_time = timeit.default_timer()
            
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            time_runs.append((end_time - start_time) * 1000)
            mem_runs.append(peak_mem / 1024)
            
        avg_time = sum(time_runs) / 3
        avg_mem = sum(mem_runs) / 3
        
        print(f"n={n}: Avg Time={avg_time:.2f}ms, Peak Memory={avg_mem:.2f}KB")
        
        benchmarks.append({
            "n": n,
            "avg_time_ms": round(avg_time, 1),
            "peak_memory_kb": round(avg_mem, 1)
        })
        
    return benchmarks

if __name__ == "__main__":
    benchmarks = run_benchmarks()
    
    output_path = os.path.join(os.path.dirname(__file__), "results.json")
    
    if os.path.exists(output_path):
        with open(output_path, "r") as f:
            data = json.load(f)
    else:
        data = {
            "problem_id": "lc_1462",
            "title": "Course Schedule IV",
            "topic": "Graph",
            "benchmarks": [],
            "empirical_time_complexity": "O(?)",
            "empirical_space_complexity": "O(?)",
            "notes": ""
        }
        
    data["benchmarks"] = benchmarks
    
    with open(output_path, "w") as f:
        json.dump(data, f, indent=2)
        
