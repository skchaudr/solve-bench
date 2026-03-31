import json
import time
import tracemalloc
import os
from solution import Solution

def run():
    with open("dataset.json", "r") as f:
        data = json.load(f)
        
    results = {
        "problem_id": "lc_1311",
        "title": "Get Watched Videos by Your Friends",
        "topic": "Graph",
        "benchmarks": [],
        "empirical_time_complexity": "O(N log N)",
        "empirical_space_complexity": "O(N)",
        "notes": "Time is bounded by BFS traversal O(V+E) and sorting video frequencies which is at most O(V log V). Space is O(V+E) for graph traversal."
    }
    
    sol = Solution()
    
    for n_str in ["100", "1000", "10000", "100000"]:
        if n_str not in data:
            continue
        kwargs = data[n_str]
        watchedVideos = kwargs["watchedVideos"]
        friends = kwargs["friends"]
        id_val = kwargs["id"]
        level = kwargs["level"]
        n = kwargs["n"]
        
        sol.watchedVideosByFriends(watchedVideos, friends, id_val, level)
        
        runs = 3
        times = []
        peaks = []
        
        for _ in range(runs):
            tracemalloc.start()
            start = time.perf_counter()
            sol.watchedVideosByFriends(watchedVideos, friends, id_val, level)
            end = time.perf_counter()
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            times.append(end - start)
            peaks.append(peak)
            
        avg_time_ms = (sum(times) / runs) * 1000
        peak_memory_kb = max(peaks) / 1024
        
        results["benchmarks"].append({
            "n": n,
            "avg_time_ms": round(avg_time_ms, 3),
            "peak_memory_kb": round(peak_memory_kb, 3)
        })
        
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run()
