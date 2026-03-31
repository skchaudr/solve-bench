import json
import timeit
import tracemalloc
import os
from solution import Solution

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    results = {
        "problem_id": "lc_1105",
        "title": "Filling Bookcase Shelves",
        "topic": "Dynamic Programming",
        "benchmarks": [],
        "empirical_time_complexity": "O(N * W)",
        "empirical_space_complexity": "O(N)",
        "notes": "DP array takes O(N) space. Inner loop runs up to the max number of books that fit on a shelf. With bounded shelfWidth, time complexity empirically scales linearly with N."
    }
    
    sol = Solution()
    for N in scales:
        with open(f'benchmark/lc_1105/input_{N}.json', 'r') as f:
            data = json.load(f)
        books = data['books']
        shelfWidth = data['shelfWidth']
        
        def test_func():
            return sol.minHeightShelves(books, shelfWidth)
        
        time_runs = timeit.repeat(test_func, number=1, repeat=3)
        avg_time_ms = (sum(time_runs) / len(time_runs)) * 1000
        
        tracemalloc.start()
        test_func()
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        peak_memory_kb = peak / 1024
        
        results["benchmarks"].append({
            "n": N,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })
        
    with open('benchmark/lc_1105/results.json', 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    run_benchmarks()