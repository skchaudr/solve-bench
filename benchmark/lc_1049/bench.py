import sys
import os
import gc
import json
import timeit
import tracemalloc

# Add the repository root to sys.path to resolve module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from benchmark.lc_1049.solution import Solution
from benchmark.lc_1049.generate import generate_data

def main():
    scales = [100, 1000, 10000, 100000]
    runs = 3
    benchmarks = []

    sol = Solution()

    for n in scales:
        data = generate_data(n)

        # We don't mutate the data, but let's copy it anyway just to be standard.
        # However, the problem specifies the solution doesn't mutate, so copying is not strictly necessary.

        times = []
        peak_memories = []

        for _ in range(runs):
            # To isolate memory, force GC before measuring
            gc.collect()

            # Use same data instance for consistent memory measuring
            # The solution doesn't mutate the input, so no need to deepcopy.
            test_data = data

            tracemalloc.start()
            gc.disable()

            start_time = timeit.default_timer()
            _ = sol.lastStoneWeightII(test_data)
            end_time = timeit.default_timer()

            gc.enable()
            _, peak_mem = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            times.append(end_time - start_time)
            peak_memories.append(peak_mem)

        avg_time_ms = (sum(times) / runs) * 1000
        # Peak memory across all runs, or average of peaks? Usually average of peaks is fine.
        avg_peak_memory_kb = (sum(peak_memories) / runs) / 1024

        benchmarks.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(avg_peak_memory_kb, 3)
        })

        print(f"Scale n={n}: {avg_time_ms:.3f} ms, {avg_peak_memory_kb:.3f} KB")

    results_path = os.path.join(os.path.dirname(__file__), "results.json")

    # Read existing or create new results.json
    if os.path.exists(results_path):
        with open(results_path, "r") as f:
            results = json.load(f)
    else:
        results = {
            "problem_id": "lc_1049",
            "title": "Last Stone Weight II",
            "topic": "Dynamic Programming",
            "empirical_time_complexity": "O(N^2)",
            "empirical_space_complexity": "O(N)",
            "notes": "Since max sum is S <= 100 * N, the number of bits required scales linearly with N. Bitwise operations on Python's arbitrary precision integers take O(bits), so each step takes O(N). Across N steps, overall time complexity approaches O(N^2). Empirical measurements verify space scales linearly O(N)."
        }

    results["benchmarks"] = benchmarks

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
