import os
import json
import timeit
import tracemalloc
import gc
from solution import Solution

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    results = {
        "problem_id": "lc_11",
        "title": "Container With Most Water",
        "topic": "Two Pointers",
        "benchmarks": [],
        "empirical_time_complexity": "O(?)",
        "empirical_space_complexity": "O(?)",
        "notes": "reasoning based on timing ratios"
    }
    
    sol = Solution()
    
    for n in scales:
        file_path = os.path.join(data_dir, f'input_{n}.json')
        with open(file_path, 'r') as f:
            heights = json.load(f)
            
        times = []
        memories = []
        
        for _ in range(3):
            # We don't need to copy the list if it's not mutated, 
            # and our algorithm doesn't mutate `height`.
            
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            sol.maxArea(heights)
            end_time = timeit.default_timer()
            
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            times.append((end_time - start_time) * 1000)
            memories.append(peak_mem / 1024.0)
            
        avg_time = sum(times) / 3
        avg_mem = sum(memories) / 3
        
        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": round(avg_time, 4),
            "peak_memory_kb": round(avg_mem, 4)
        })
        
    print(json.dumps(results, indent=2))
    
    with open(os.path.join(os.path.dirname(__file__), 'results.json'), 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    run_benchmarks()
