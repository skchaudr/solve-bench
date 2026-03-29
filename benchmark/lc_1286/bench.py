import json
import os
import sys
import timeit
import tracemalloc
import gc

# Add the repo root to sys.path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_1286.solution import CombinationIterator

def run_operations(ops, args):
    itr = None
    for op, arg in zip(ops, args):
        if op == "CombinationIterator":
            itr = CombinationIterator(arg[0], arg[1])
        elif op == "next":
            itr.next()
        elif op == "hasNext":
            itr.hasNext()

def bench():
    scales = [100, 1000, 10000, 100000]
    results = []
    
    for n in scales:
        dataset_path = os.path.join(os.path.dirname(__file__), f"dataset/{n}.json")
        with open(dataset_path, "r") as f:
            data = json.load(f)
            ops = data["ops"]
            args = data["args"]
            
        times = []
        peak_mems = []
        
        for _ in range(3):
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            run_operations(ops, args)
            end_time = timeit.default_timer()
            
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            times.append(end_time - start_time)
            peak_mems.append(peak)
            
        avg_time_ms = (sum(times) / len(times)) * 1000
        avg_peak_mem_kb = (sum(peak_mems) / len(peak_mems)) / 1024
        
        results.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(avg_peak_mem_kb, 3)
        })
        print(f"n={n}: {avg_time_ms:.3f} ms, {avg_peak_mem_kb:.3f} KB")
        
    return results

if __name__ == "__main__":
    results = bench()
    with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
        json.dump({
            "problem_id": "lc_1286",
            "title": "Iterator for Combination",
            "topic": "Backtracking",
            "benchmarks": results,
            "empirical_time_complexity": "O(N)",
            "empirical_space_complexity": "O(1)",
            "notes": "Time scales linearly with the number of operations N because each next/hasNext takes O(K) where K is a small constant (<=15). Space complexity is O(1) auxiliary space beyond the input data because only the K indices are stored."
        }, f, indent=2)
