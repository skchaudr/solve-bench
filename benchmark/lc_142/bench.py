import os
import sys
import json
import timeit
import tracemalloc
import gc

# Add the repository root to sys.path to resolve module imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_142.solution import Solution, ListNode

def build_linked_list(arr, pos):
    if not arr:
        return None
    head = ListNode(arr[0])
    curr = head
    cycle_node = None
    if pos == 0:
        cycle_node = head
        
    for i in range(1, len(arr)):
        curr.next = ListNode(arr[i])
        curr = curr.next
        if i == pos:
            cycle_node = curr
            
    if cycle_node:
        curr.next = cycle_node
        
    return head

def run_benchmarks():
    data_file = os.path.join(os.path.dirname(__file__), "data.json")
    with open(data_file, "r") as f:
        data = json.load(f)
        
    results = {
        "problem_id": "lc_142",
        "title": "Linked List Cycle II",
        "topic": "Two Pointers",
        "benchmarks": [],
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(1)",
        "notes": "Both time and space complexity follow expected logic for Two Pointers."
    }
    
    solution = Solution()
    scales = [100, 1000, 10000, 100000]
    
    for n in scales:
        n_str = str(n)
        if n_str not in data:
            continue
            
        arr = data[n_str]["arr"]
        pos = data[n_str]["pos"]
        
        # Build the linked list
        head = build_linked_list(arr, pos)
        
        runs = 3
        total_time = 0
        peak_memory_bytes = 0
        
        for _ in range(runs):
            gc.disable()
            tracemalloc.start()
            
            start_time = timeit.default_timer()
            solution.detectCycle(head)
            end_time = timeit.default_timer()
            
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += (end_time - start_time)
            peak_memory_bytes = max(peak_memory_bytes, peak)
            
        avg_time_ms = (total_time / runs) * 1000
        peak_memory_kb = peak_memory_bytes / 1024
        
        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 4),
            "peak_memory_kb": round(peak_memory_kb, 4)
        })
        
    # Infer complexity based on results
    benchmarks = results["benchmarks"]
    if len(benchmarks) >= 2:
        # N goes up by 10x each step. 
        # For O(N) time, time goes up by ~10x.
        # For O(1) space, memory goes up by ~1x (constant).
        ratio_time = benchmarks[-1]["avg_time_ms"] / (benchmarks[-2]["avg_time_ms"] or 1e-9)
        
        if ratio_time > 50:
            results["empirical_time_complexity"] = "O(N^2)"
        elif ratio_time > 5:
            results["empirical_time_complexity"] = "O(N)"
        else:
            results["empirical_time_complexity"] = "O(log N) or O(1)"
            
        mem_ratio = benchmarks[-1]["peak_memory_kb"] / (benchmarks[-2]["peak_memory_kb"] or 1e-9)
        if mem_ratio > 5:
            results["empirical_space_complexity"] = "O(N)"
        else:
            results["empirical_space_complexity"] = "O(1)"
            
        results["notes"] = f"Empirical scaling ratio for time: {ratio_time:.2f}x for 10x N. Space scales by: {mem_ratio:.2f}x for 10x N."
        
    results_file = os.path.join(os.path.dirname(__file__), "results.json")
    with open(results_file, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_benchmarks()
