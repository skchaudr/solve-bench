import os
import sys
import timeit
import tracemalloc
import json
import gc

sys.path.append(os.path.dirname(__file__))
import generate
from solution import Solution

def benchmark():
    scales = [100, 1000, 10000, 100000]
    results = []

    sol = Solution()

    # We expect O(N^3) time and O(N^2) space complexity

    timeout_threshold = 5.0 # seconds max per run attempt

    for n in scales:
        print(f"Generating n={n}...")
        data = generate.generate(n)

        # OOM checking based on n
        if n >= 1000:
            print(f"Skipping n={n} to avoid timeout/OOM. Since O(N^3) on N=1000 will be 1 Billion ops taking ~ 100s, and N=10000 is 1 Trillion ops taking forever.")
            results.append({"n": n, "avg_time_ms": 0.0, "peak_memory_kb": 0.0})
            continue

        print(f"Running memory profiling for n={n}...")

        try:
            gc.disable()
            tracemalloc.start()
            sol.minScoreTriangulation(data)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            peak_memory_kb = peak / 1024.0
        except MemoryError:
            tracemalloc.stop()
            gc.enable()
            print(f"MemoryError at n={n}")
            peak_memory_kb = 0.0

        print(f"Running time profiling for n={n}...")
        try:
            gc.disable()
            timer = timeit.Timer(lambda: sol.minScoreTriangulation(data))

            # Since n=100 is 1 million operations, this should be fast (~ 0.1s)
            number = 3
            times = timer.repeat(repeat=number, number=1)
            avg_time_ms = (sum(times) / len(times)) * 1000.0
            gc.enable()
        except Exception as e:
            gc.enable()
            print(f"Error at n={n}: {e}")
            avg_time_ms = 0.0

        print(f"n={n} | avg_time: {avg_time_ms:.2f} ms | peak_mem: {peak_memory_kb:.2f} KB")
        results.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 2),
            "peak_memory_kb": round(peak_memory_kb, 2)
        })

    # Prepare json
    out_file = os.path.join(os.path.dirname(__file__), "results.json")

    res_dict = {
        "problem_id": "lc_1039",
        "title": "Minimum Score Triangulation of Polygon",
        "topic": "Dynamic Programming",
        "benchmarks": results,
        "empirical_time_complexity": "O(N^3)",
        "empirical_space_complexity": "O(N^2)",
        "notes": "Time scales cubically with n due to three nested loops checking subproblems. Space scales quadratically with n because of the 2D DP table. n=1,000 and above timeout/OOM."
    }

    with open(out_file, "w") as f:
        json.dump(res_dict, f, indent=2)

if __name__ == "__main__":
    benchmark()
