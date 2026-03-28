import sys
import os
import timeit
import tracemalloc
import json

# Add current directory to path so we can import local modules
sys.path.append(os.path.dirname(__file__))

from solution import Solution
from generate import generate

def run_benchmarks():
    # Constraints say length is 1 to 16. So we can use 4, 8, 12, 16.
    # At n=16, worst case partitions is 2^15 = 32768, which is completely fine
    # for timing.
    sizes = [4, 8, 12, 16]
    results = []

    sol = Solution()

    for n in sizes:
        s = generate(n)

        # Warmup and timeit
        # Copy is not really needed since string is immutable and output is generated fresh
        timer = timeit.Timer(lambda: sol.partition(s))

        # We can dynamically adjust runs based on size.
        # For n=16, maybe we only want a few runs.
        number_of_runs = max(1, 1000 // (2 ** (n // 4)))

        try:
            # 3 runs avg
            times = timer.repeat(repeat=3, number=number_of_runs)
            avg_time = sum(times) / 3.0
            avg_time_ms = (avg_time / number_of_runs) * 1000
        except Exception as e:
            print(f"Error timing for n={n}: {e}")
            avg_time_ms = 0.0

        # Memory profiling
        tracemalloc.start()
        try:
            # Not using a copy since it's an immutable string
            sol.partition(s)
            _, peak_mem = tracemalloc.get_traced_memory()
            peak_memory_kb = peak_mem / 1024
        except Exception as e:
            print(f"Error measuring memory for n={n}: {e}")
            peak_memory_kb = 0.0
        finally:
            tracemalloc.stop()

        results.append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 1)
        })

        print(f"n={n}: {avg_time_ms:.3f} ms, {peak_memory_kb:.1f} KB")

    output = {
        "problem_id": "lc_131",
        "title": "Palindrome Partitioning",
        "topic": "Backtracking",
        "benchmarks": results,
        "empirical_time_complexity": "O(N * 2^N)",
        "empirical_space_complexity": "O(N * 2^N)",
        "notes": "Backtracking explores all 2^(N-1) partitions in the worst case ('a' * N). Copying partitions takes O(N) time each, leading to O(N * 2^N) time and space complexity."
    }

    with open(os.path.join(os.path.dirname(__file__), 'results.json'), 'w') as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
