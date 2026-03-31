import json
import timeit
import tracemalloc
import gc
from solution import Solution, ListNode

def build_linked_list(arr):
    if not arr:
        return None
    head = ListNode(arr[0])
    curr = head
    for val in arr[1:]:
        curr.next = ListNode(val)
        curr = curr.next
    return head

def main():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []
    
    sol = Solution()
    
    for n in scales:
        with open(f"data_{n}.json", "r") as f:
            data = json.load(f)
        
        arr = data["arr"]
        
        # Build LL outside benchmark
        head = build_linked_list(arr)
        
        # Time complexity
        gc.collect()
        
        def run_algo():
            sol.sortedListToBST(head)

        times = timeit.repeat(run_algo, number=1, repeat=3)
        avg_time = sum(times) / 3 * 1000 # to ms
        
        # Space complexity
        gc.collect()
        tracemalloc.start()
        sol.sortedListToBST(head)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        peak_kb = peak / 1024
        
        benchmarks.append({
            "n": n,
            "avg_time_ms": round(avg_time, 3),
            "peak_memory_kb": round(peak_kb, 3)
        })
        
    output = {
        "problem_id": "lc_109",
        "title": "Convert Sorted List to Binary Search Tree",
        "topic": "Binary Search",
        "benchmarks": benchmarks,
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Time scales linearly with N because we iterate the list to extract values, and then iteratively construct the BST visiting each node once. Space complexity is O(N) due to the intermediate array of values and the stack during construction."
    }
    
    with open("results.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
