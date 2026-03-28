"""Fire remaining 63 benchmark tasks with rate limit protection."""
import subprocess
import duckdb
import time

DB_FILE = "solve-bench.db"
REPO = "skchaudr/solve-bench"

ALREADY_DONE = {
    "lc_1004", "lc_1016", "lc_1031", "lc_1040",
    "lc_1052", "lc_1156", "lc_1208"
}

TOPIC_FILTERS = {
    "Sliding Window":      "tags LIKE '%Sliding Window%'",
    "Two Pointers":        "tags LIKE '%Two Pointers%'",
    "Binary Search":       "tags LIKE '%Binary Search%'",
    "Tree":                "tags LIKE '%Tree%'",
    "Graph":               "tags LIKE '%Graph%'",
    "Heap":                "tags LIKE '%Heap%'",
    "Backtracking":        "tags LIKE '%Backtracking%'",
    "Dynamic Programming": "tags LIKE '%Dynamic Programming%'",
}

GENERATOR_HINTS = {
    "Sliding Window":      "random integer arrays of length n, values in [1, 10^4]",
    "Two Pointers":        "sorted or unsorted integer arrays of length n, values in [-10^9, 10^9]",
    "Binary Search":       "sorted integer arrays of length n, random target values",
    "Tree":                "random binary trees with n nodes, random values",
    "Graph":               "random directed/undirected graphs with n nodes and ~2n edges",
    "Heap":                "random integer arrays of length n simulating a stream of events",
    "Backtracking":        "strings of length n or grids of size sqrt(n) x sqrt(n)",
    "Dynamic Programming": "integer arrays of length n or n x n grids with random values",
}


def build_task(problem, topic):
    hint = GENERATOR_HINTS.get(topic, "random inputs appropriate for the problem")
    return f"""## [Jules Benchmark] {problem['id']} — {problem['title']}

### Goal
Write a solution, generate synthetic stress-test data, benchmark at scale, report empirical complexity curve.

**Topic:** {topic} | **Tags:** {problem['tags']}

### Problem
```
{problem['prompt'][:1200]}
```

### Tasks
1. `benchmark/{problem['id']}/solution.py` — clean Python 3 solution
2. `benchmark/{problem['id']}/generate.py` — synthetic inputs at n=100, 1_000, 10_000, 100_000
   - Input type: {hint}
3. `benchmark/{problem['id']}/bench.py` — timeit + tracemalloc at each scale (3 runs avg)
4. `benchmark/{problem['id']}/results.json`:
```json
{{
  "problem_id": "{problem['id']}",
  "title": "{problem['title']}",
  "topic": "{topic}",
  "benchmarks": [
    {{"n": 100,    "avg_time_ms": 0.0, "peak_memory_kb": 0}},
    {{"n": 1000,   "avg_time_ms": 0.0, "peak_memory_kb": 0}},
    {{"n": 10000,  "avg_time_ms": 0.0, "peak_memory_kb": 0}},
    {{"n": 100000, "avg_time_ms": 0.0, "peak_memory_kb": 0}}
  ],
  "empirical_time_complexity": "O(?)",
  "empirical_space_complexity": "O(?)",
  "notes": "reasoning based on timing ratios"
}}
```
"""


dispatched = 0
with duckdb.connect(DB_FILE) as conn:
    for topic, condition in TOPIC_FILTERS.items():
        rows = conn.execute(
            f"SELECT id, title, tags, prompt FROM problems "
            f"WHERE difficulty='medium' AND {condition} ORDER BY id LIMIT 10"
        ).fetchall()
        for pid, title, tags, prompt in rows:
            if pid in ALREADY_DONE:
                continue
            p = {"id": pid, "title": title, "tags": tags, "prompt": prompt}
            task_title = f"[Benchmark] {pid} — {title} ({topic})"
            body = build_task(p, topic)
            result = subprocess.run(
                ["jules", "new", "--repo", REPO, f"{task_title}\n\n{body}"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                dispatched += 1
                print(f"✅ [{dispatched:02d}] {pid} — {title[:40]}", flush=True)
            else:
                print(f"❌ {pid} — {result.stderr[:80]}", flush=True)
            time.sleep(2)

print(f"\nDispatched {dispatched} tasks")
