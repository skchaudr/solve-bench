import json
import os
import sys
import timeit
import tracemalloc
import gc

# Add the repo root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from benchmark.lc_1514.solution import Solution

def run_benchmark():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []
    
    for scale in scales:
        with open(f"benchmark/lc_1514/data_{scale}.json", "r") as f:
            data = json.load(f)
            
        n = data["n"]
        edges = data["edges"]
        succProb = data["succProb"]
        start = data["start"]
        end = data["end"]
        
        # We need 3 runs average
        times = []
        peak_mems = []
        
        for _ in range(3):
            gc.collect()
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            
            # Since edges, succProb aren't mutated in Solution, we don't strictly need deepcopies
            # But let's instantiate the class fresh
            sol = Solution()
            sol.maxProbability(n, edges, succProb, start, end)
            
            end_time = timeit.default_timer()
            _, peak_mem = tracemalloc.get_traced_memory()
            
            tracemalloc.stop()
            gc.enable()
            
            times.append(end_time - start_time)
            peak_mems.append(peak_mem)
            
        avg_time_ms = (sum(times) / len(times)) * 1000
        peak_memory_kb = max(peak_mems) / 1024
        
        benchmarks.append({
            "n": scale,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })
        print(f"n={scale}, avg_time={avg_time_ms:.3f} ms, peak_mem={peak_memory_kb:.3f} KB")

    results = {
        "problem_id": "lc_1514",
        "title": "Path with Maximum Probability",
        "topic": "Graph",
        "benchmarks": benchmarks,
        "empirical_time_complexity": "O(E log V)",
        "empirical_space_complexity": "O(E + V)",
        "notes": "Dijkstra's algorithm. Time complexity scales with edges, bounded by priority queue insertions. Space complexity scales linearly."
    }
    
    with open("benchmark/lc_1514/results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmark()
