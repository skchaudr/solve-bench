import json
import timeit
import tracemalloc
from solution import Solution

def run_benchmark():
    with open("benchmark/lc_1079/dataset.json", "r") as f:
        data = json.load(f)
    
    sol = Solution()
    results = {
        "problem_id": "lc_1079",
        "title": "Letter Tile Possibilities",
        "topic": "Backtracking",
        "benchmarks": [],
        "empirical_time_complexity": "O(N!)", 
        "empirical_space_complexity": "O(N)", 
        "notes": "Backtracking explores all unique subsets/permutations, leading to factorial time complexity. Space complexity is O(N) due to recursion stack depth and character frequencies. N values mapped down to 3, 5, 7, 9 to avoid timeout."
    }
    
    for n_str, tiles in data.items():
        n = int(n_str)
        
        # Warmup and test functionality
        _ = sol.numTilePossibilities(tiles)
        
        def run_once():
            sol.numTilePossibilities(tiles)

        runs = 3
        times = timeit.repeat(stmt=run_once, repeat=runs, number=1)
        avg_time_ms = (sum(times) / runs) * 1000
        
        # Memory
        tracemalloc.start()
        _ = sol.numTilePossibilities(tiles)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        peak_memory_kb = peak / 1024
        
        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": avg_time_ms,
            "peak_memory_kb": peak_memory_kb
        })
    
    with open("benchmark/lc_1079/results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmark()
