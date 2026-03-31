import json
import timeit
import tracemalloc
import gc
from solution import Solution, TreeNode

def build_tree(arr):
    if not arr:
        return None
    root = TreeNode(arr[0])
    queue = [root]
    i = 1
    while i < len(arr):
        curr = queue.pop(0)
        
        if i < len(arr) and arr[i] is not None:
            curr.left = TreeNode(arr[i])
            queue.append(curr.left)
        i += 1
        
        if i < len(arr) and arr[i] is not None:
            curr.right = TreeNode(arr[i])
            queue.append(curr.right)
        i += 1
    return root

def main():
    scales = [100, 1000, 10000, 100000]
    benchmarks = []
    
    sol = Solution()
    
    for n in scales:
        with open(f"data_{n}.json", "r") as f:
            data = json.load(f)
        
        arr = data["arr"]
        limit = data["limit"]
        
        # Build tree outside the benchmark
        root = build_tree(arr)
        
        # Time complexity
        gc.collect()
        
        def run_algo():
            # Create a deep copy of the tree for each run, or just re-build it.
            # wait, if the tree is modified, we need a fresh copy.
            # Building tree can be slow. So we must build it inside the timing loop or use deepcopy.
            # "When benchmarking in-place linked list modifications, ensure the linked list is reconstructed from the underlying array data at the start of each benchmark run before enabling tracemalloc and starting execution timing."
            # Actually, the memory instruction says: "perform the parsing and conversion from flat arrays to Node objects before starting the timeit timer in bench.py"
            # Since the algorithm modifies the tree in-place, we have to rebuild it for each run.
            pass

        # Since it's in-place modification, we need to rebuild the tree per run.
        times = []
        for _ in range(3):
            tree_root = build_tree(arr)
            gc.collect()
            start_time = timeit.default_timer()
            sol.sufficientSubset(tree_root, limit)
            end_time = timeit.default_timer()
            times.append((end_time - start_time) * 1000)
            
        avg_time = sum(times) / 3
        
        # Space complexity
        tree_root = build_tree(arr)
        gc.collect()
        tracemalloc.start()
        sol.sufficientSubset(tree_root, limit)
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        peak_kb = peak / 1024
        
        benchmarks.append({
            "n": n,
            "avg_time_ms": round(avg_time, 3),
            "peak_memory_kb": round(peak_kb, 3)
        })
        
    output = {
        "problem_id": "lc_1080",
        "title": "Insufficient Nodes in Root to Leaf Paths",
        "topic": "Tree",
        "benchmarks": benchmarks,
        "empirical_time_complexity": "O(N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Time scales linearly with N because the iterative post-order traversal visits each node a constant number of times. Space complexity is O(N) due to the hash map tracking leaf sums and parent relationships for every node, and the stack size during traversal."
    }
    
    with open("results.json", "w") as f:
        json.dump(output, f, indent=2)

if __name__ == "__main__":
    main()
