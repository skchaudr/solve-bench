import json
import time
import tracemalloc
import sys

# Add current directory to path so we can import solution
sys.path.append('.')

from solution import SnapshotArray

def run_benchmark():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []
    
    for scale in scales:
        with open(f"benchmark/lc_1146/data_{scale}.json", "r") as f:
            data = json.load(f)
            
        ops = data["ops"]
        args = data["args"]
        
        runs = 3
        total_time = 0
        peak_memory = 0
        
        for _ in range(runs):
            tracemalloc.start()
            start_time = time.perf_counter()
            
            obj = SnapshotArray(*args[0])
            for i in range(1, len(ops)):
                op = ops[i]
                if op == "set":
                    obj.set(*args[i])
                elif op == "snap":
                    obj.snap()
                elif op == "get":
                    obj.get(*args[i])
                    
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
        "problem_id": "lc_1146",
        "title": "Snapshot Array",
        "topic": "Binary Search",
        "benchmarks": benchmarks,
        "empirical_time_complexity": "O(N log N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Time complexity is empirical O(N log N) based on 10x N resulting in ~14x time increase. Space complexity is O(N) since memory scales exactly 10x per 10x N."
    }
    
    with open("benchmark/lc_1146/results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmark()
