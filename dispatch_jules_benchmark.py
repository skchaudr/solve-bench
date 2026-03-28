"""
Dispatches Jules benchmark tasks — one per problem.
Each task: write solution + generate synthetic data + benchmark at scale + report complexity curve.

Usage:
  python dispatch_jules_benchmark.py --dry-run
  python dispatch_jules_benchmark.py
"""
import subprocess
import argparse
import duckdb
import time

DB_FILE = "solve-bench.db"
REPO = "skchaudr/solve-bench"

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

# Data generator hints per topic so Jules knows what synthetic data looks like
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


def get_problems(conn, condition: str, limit: int = 10) -> list[dict]:
    rows = conn.execute(f"""
        SELECT id, title, difficulty, tags, prompt
        FROM problems
        WHERE difficulty = 'medium' AND {condition}
        ORDER BY id
        LIMIT {limit}
    """).fetchall()
    return [{"id": r[0], "title": r[1], "difficulty": r[2],
             "tags": r[3], "prompt": r[4]} for r in rows]


def build_task(problem: dict, topic: str) -> str:
    generator_hint = GENERATOR_HINTS.get(topic, "random inputs appropriate for the problem")

    return f"""## [Jules Benchmark] {problem['id']} — {problem['title']}

### Goal
Write a solution, generate synthetic stress-test data, benchmark at scale, and report the empirical time and space complexity curve.

### Problem
**Topic:** {topic}
**Tags:** {problem['tags']}

```
{problem['prompt'][:1500]}
```

---

### Your tasks

**1. Write solution**
`benchmark/{problem['id']}/solution.py` — clean Python 3 solution

**2. Write synthetic data generator**
`benchmark/{problem['id']}/generate.py` — generates inputs of size n={"{100, 1_000, 10_000, 100_000}"}
- Input type: {generator_hint}
- Must produce valid inputs for this specific problem
- Generate at least 3 random instances per scale for averaging

**3. Write benchmark harness**
`benchmark/{problem['id']}/bench.py` — runs solution against each scale:
- Use `timeit` to measure wall-clock runtime (average of 3 runs)
- Use `tracemalloc` to measure peak memory usage
- Record results at each n

**4. Output results**
`benchmark/{problem['id']}/results.json`:
```json
{{
  "problem_id": "{problem['id']}",
  "title": "{problem['title']}",
  "topic": "{topic}",
  "benchmarks": [
    {{"n": 100,    "avg_time_ms": 0.12, "peak_memory_kb": 48}},
    {{"n": 1000,   "avg_time_ms": 1.4,  "peak_memory_kb": 312}},
    {{"n": 10000,  "avg_time_ms": 18.2, "peak_memory_kb": 2800}},
    {{"n": 100000, "avg_time_ms": 195,  "peak_memory_kb": 28000}}
  ],
  "empirical_time_complexity": "O(n)",
  "empirical_space_complexity": "O(n)",
  "notes": "runtime doubles with each 10x increase in n, consistent with O(n)"
}}
```

**5. Fit the curve**
Based on the timing ratios between scales, infer the empirical complexity:
- If time scales ~linearly with n → O(n)
- If time scales ~as n log n → O(n log n)
- If time quadruples when n doubles → O(n²)
State your reasoning in the notes field.
"""


def dispatch(title: str, body: str, dry_run: bool) -> bool:
    if dry_run:
        print(f"DRY: {title[:60]}")
        return True

    result = subprocess.run(
        ["jules", "new", "--repo", REPO, f"{title}\n\n{body}"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        session_id = None
        for line in result.stdout.splitlines():
            if "ID:" in line:
                session_id = line.split("ID:")[-1].strip()
        print(f"✅ {title[:55]} → {session_id}")
        return True
    else:
        print(f"❌ {title[:55]}\n   {result.stderr[:100]}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=70,
                        help="Max tasks to dispatch (default 70)")
    args = parser.parse_args()

    dispatched = 0
    with duckdb.connect(DB_FILE) as conn:
        for topic, condition in TOPIC_FILTERS.items():
            if dispatched >= args.limit:
                break
            problems = get_problems(conn, condition)
            for p in problems:
                if dispatched >= args.limit:
                    break
                title = f"[Benchmark] {p['id']} — {p['title']} ({topic})"
                body = build_task(p, topic)
                ok = dispatch(title, body, args.dry_run)
                if ok:
                    dispatched += 1
                    time.sleep(2)

    print(f"\n{'Would dispatch' if args.dry_run else 'Dispatched'} {dispatched} benchmark tasks")


if __name__ == "__main__":
    main()
