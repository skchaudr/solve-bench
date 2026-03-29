import os
import sys
import json
import timeit
import tracemalloc
import gc

# Add the repository root to sys.path to enable absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from benchmark.lc_148.solution import Solution, ListNode

def build_linked_list(arr):
    dummy = ListNode(0)
    curr = dummy
    for val in arr:
        curr.next = ListNode(val)
        curr = curr.next
    return dummy.next

def run_benchmarks():
    data_path = os.path.join(os.path.dirname(__file__), 'data.json')
    with open(data_path, 'r') as f:
        data = json.load(f)
        
    results_path = os.path.join(os.path.dirname(__file__), 'results.json')
    with open(results_path, 'r') as f:
        results = json.load(f)

    sol = Solution()
    scales = [100, 1000, 10000, 100000]
    runs = 3
    
    for i, n in enumerate(scales):
        arr = data[str(n)]
        
        total_time = 0.0
        peak_mem = 0
        
        for _ in range(runs):
            # Setup list OUTSIDE of timed and memory profiled sections
            head = build_linked_list(arr)
            
            gc.disable()
            tracemalloc.start()
            start_time = timeit.default_timer()
            
            # Run solution
            sol.sortList(head)
            
            end_time = timeit.default_timer()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            gc.enable()
            
            total_time += (end_time - start_time)
            peak_mem = max(peak_mem, peak)
            
        avg_time_ms = (total_time / runs) * 1000
        peak_memory_kb = peak_mem / 1024.0
        
        results['benchmarks'][i]['avg_time_ms'] = round(avg_time_ms, 2)
        results['benchmarks'][i]['peak_memory_kb'] = round(peak_memory_kb, 2)
        print(f"n={n}: {avg_time_ms:.2f} ms, {peak_memory_kb:.2f} KB")
        
    with open(results_path, 'w') as f:
        json.dump(results, f, indent=2)

if __name__ == '__main__':
    run_benchmarks()
