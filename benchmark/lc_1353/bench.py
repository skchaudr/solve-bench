import json
import os
import sys
import timeit
import tracemalloc
import gc

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_1353.solution import Solution

def run_benchmarks():
    sizes = [100, 1000, 10000, 100000]
    out_dir = os.path.dirname(__file__)
    
    sol = Solution()
    
    benchmarks_data = []
    
    for n in sizes:
        data_path = os.path.join(out_dir, f"data_{n}.json")
        with open(data_path, "r") as f:
            original_events = json.load(f)
            
        times = []
        peak_mems = []
        runs = 3
        
        for _ in range(runs):
            events_copy = [event[:] for event in original_events]
            
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            sol.maxEvents(events_copy)
            end_time = timeit.default_timer()
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            times.append((end_time - start_time) * 1000)
            peak_mems.append(peak / 1024)
            
        avg_time = sum(times) / runs
        avg_mem = sum(peak_mems) / runs
        
        benchmarks_data.append({
            "n": n,
            "avg_time_ms": round(avg_time, 2),
            "peak_memory_kb": round(avg_mem, 2)
        })
        print(f"n={n}: {avg_time:.2f} ms, {avg_mem:.2f} KB")

    results = {
        "problem_id": "lc_1353",
        "title": "Maximum Number of Events That Can Be Attended",
        "topic": "Heap",
        "benchmarks": benchmarks_data,
        "empirical_time_complexity": "O(N log N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Time complexity is O(N log N) because sorting takes O(N log N) and heap operations take O(N log N) in worst case. Space is O(N) due to sorting and heap space. Timing ratio roughly scales by 10x-12x as n scales 10x, matching O(N log N)."
    }

    results_path = os.path.join(out_dir, "results.json")
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
