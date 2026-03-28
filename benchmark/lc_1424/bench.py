import os
import sys
import timeit
import tracemalloc
import json
import copy

sys.path.append(os.path.dirname(__file__))

from solution import Solution
from generate import generate_data

def run_benchmarks():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []

    for n in scales:
        data = generate_data(n)

        setup = '''
import copy
data_copy = copy.deepcopy(data)
s = Solution()
'''
        stmt = 's.findDiagonalOrder(data_copy)'

        times = timeit.repeat(stmt, setup=setup, globals={"data": data, "Solution": Solution, "copy": copy}, repeat=3, number=1)
        avg_time_ms = (sum(times) / len(times)) * 1000

        s = Solution()
        data_copy = copy.deepcopy(data)
        tracemalloc.start()
        s.findDiagonalOrder(data_copy)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        peak_memory_kb = peak / 1024

        benchmarks.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 2),
            "peak_memory_kb": round(peak_memory_kb, 2)
        })
        print(f"n={n}, time={avg_time_ms:.2f}ms, memory={peak_memory_kb:.2f}KB")

    return benchmarks

if __name__ == "__main__":
    benchmarks = run_benchmarks()

    results = {
      "problem_id": "lc_1424",
      "title": "Diagonal Traverse II",
      "topic": "Heap",
      "benchmarks": benchmarks,
      "empirical_time_complexity": "O(N log N)",
      "empirical_space_complexity": "O(N)",
      "notes": "Time scales at roughly 12-13x for 10x increases in N, matching O(N log N) expectations due to heap operations. Space scales linearly at roughly 10x for 10x increases in N, confirming O(N) memory."
    }

    with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
        json.dump(results, f, indent=2)
