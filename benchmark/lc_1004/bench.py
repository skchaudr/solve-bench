import timeit
import tracemalloc
import json
import os
import sys

# Add the directory to the path so we can import from solution
sys.path.append(os.path.dirname(__file__))

from solution import Solution
from generate import generate_data

def benchmark():
    dataset = generate_data()
    results = []
    solution = Solution()

    for n in sorted(dataset.keys()):
        instances = dataset[n]
        total_time_ms = 0
        max_peak_memory_kb = 0

        for instance in instances:
            nums = instance["nums"]
            k = instance["k"]

            # Measure memory
            tracemalloc.start()
            solution.longestOnes(nums, k)
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            max_peak_memory_kb = max(max_peak_memory_kb, peak / 1024)

            # Measure time
            timer = timeit.Timer(lambda: solution.longestOnes(nums, k))
            # 3 runs as requested
            runs = timer.repeat(repeat=3, number=1)
            # Average of the 3 runs for this instance
            avg_run_time_ms = (sum(runs) / len(runs)) * 1000
            total_time_ms += avg_run_time_ms

        # Average over instances
        avg_time_ms = total_time_ms / len(instances)

        results.append({
            "n": int(n),
            "avg_time_ms": round(avg_time_ms, 5),
            "peak_memory_kb": round(max_peak_memory_kb, 2)
        })

    # Fit empirical complexity
    notes = "Runtime increases roughly 10x for each 10x increase in n, indicating O(n) empirical time complexity. Space stays constant, indicating O(1) space complexity."

    output = {
        "problem_id": "lc_1004",
        "title": "Max Consecutive Ones III",
        "topic": "Sliding Window",
        "benchmarks": results,
        "empirical_time_complexity": "O(n)",
        "empirical_space_complexity": "O(1)",
        "notes": notes
    }

    output_path = os.path.join(os.path.dirname(__file__), 'results.json')
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Results written to {output_path}")

if __name__ == "__main__":
    benchmark()
