import os
import json
import timeit
import tracemalloc
import gc
from solution import Solution

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    dir_path = os.path.dirname(os.path.abspath(__file__))
    results_path = os.path.join(dir_path, "results.json")
    
    with open(results_path, "r") as f:
        results = json.load(f)

    benchmarks = []
    sol = Solution()

    for n in scales:
        with open(os.path.join(dir_path, f"data_{n}.txt"), "r") as f:
            s = f.read()
            
        # 3 runs avg for time
        times = []
        for _ in range(3):
            gc.disable()
            start_time = timeit.default_timer()
            sol.balancedString(s)
            end_time = timeit.default_timer()
            gc.enable()
            times.append(end_time - start_time)
            
        avg_time_ms = (sum(times) / len(times)) * 1000

        # Memory peak
        gc.disable()
        tracemalloc.start()
        sol.balancedString(s)
        _, peak_mem_bytes = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        gc.enable()
        
        peak_memory_kb = peak_mem_bytes / 1024
        
        benchmarks.append({
            "n": n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": peak_memory_kb
        })
        
    results["benchmarks"] = benchmarks
    
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
        
if __name__ == "__main__":
    run_benchmarks()
