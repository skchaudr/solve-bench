import json
import os
import sys
import timeit
import tracemalloc
import gc

# Add the repository root to sys.path to allow imports from benchmark directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_1094.solution import Solution

def run_benchmarks():
    dataset_path = os.path.join(os.path.dirname(__file__), "dataset.json")
    with open(dataset_path, "r") as f:
        data = json.load(f)

    results_path = os.path.join(os.path.dirname(__file__), "results.json")
    with open(results_path, "r") as f:
        results = json.load(f)

    solution = Solution()
    benchmarks = []

    for n_str in ["100", "1000", "10000", "100000"]:
        if n_str not in data:
            continue
            
        trips = data[n_str]["trips"]
        capacity = data[n_str]["capacity"]
        n = int(n_str)
        
        times = []
        peak_memories = []

        for _ in range(3):
            # Clean up memory
            gc.collect()
            
            # Copy trips for the current run, as the solution mutates (sorts) the list in-place
            trips_copy = [trip[:] for trip in trips]
            
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            _ = solution.carPooling(trips_copy, capacity)
            end_time = timeit.default_timer()
            
            current_mem, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            times.append((end_time - start_time) * 1000) # Convert to ms
            peak_memories.append(peak_mem / 1024) # Convert to kb
            
        avg_time = sum(times) / len(times)
        avg_memory = sum(peak_memories) / len(peak_memories)
        
        benchmarks.append({
            "n": n,
            "avg_time_ms": round(avg_time, 3),
            "peak_memory_kb": round(avg_memory, 2)
        })

    results["benchmarks"] = benchmarks
    
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
