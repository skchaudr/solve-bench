"""
dispatch_packed.py — Dispatch 24 remaining benchmark problems as 6 packed Jules tasks.

Packs 4 problems per task to minimize quota usage (6 tasks vs 24).
Each problem still produces its own benchmark/<id>/ folder with independent files.

Usage:
  python dispatch_packed.py --dry-run
  python dispatch_packed.py
"""
import os
import re
import time
import argparse
import subprocess
import duckdb

DB_FILE = "solve-bench.db"
REPO = "skchaudr/solve-bench"

# 24 problems confirmed missing benchmark folders, grouped by topic affinity
PACKS = [
    ("01", ["lc_102", "lc_103", "lc_106", "lc_107"]),           # Tree
    ("02", ["lc_1026", "lc_1080", "lc_109", "lc_1038"]),        # Tree + Binary Search
    ("03", ["lc_1146", "lc_1170", "lc_1201", "lc_1042"]),       # Binary Search + Graph
    ("04", ["lc_1129", "lc_1311", "lc_1319", "lc_1338"]),       # Graph + Heap
    ("05", ["lc_1405", "lc_1488", "lc_1079", "lc_113"]),        # Heap + Backtracking
    ("06", ["lc_1238", "lc_1024", "lc_1043", "lc_1105"]),       # Backtracking + DP
]

GENERATOR_HINTS = {
    "Tree":                "random binary trees with n nodes, random integer values",
    "Binary Search":       "sorted integer arrays of length n, random target values",
    "Graph":               "random directed/undirected graphs with n nodes and ~2n edges",
    "Heap":                "random integer arrays of length n simulating a stream of events",
    "Backtracking":        "strings of length n or grids of size sqrt(n) x sqrt(n)",
    "Dynamic Programming": "integer arrays of length n or n x n grids with random values",
}


def load_problems(ids: list[str]) -> dict[str, dict]:
    with duckdb.connect(DB_FILE) as conn:
        placeholders = ", ".join("?" for _ in ids)
        rows = conn.execute(
            f"SELECT id, title, tags, prompt FROM problems WHERE id IN ({placeholders})",
            ids
        ).fetchall()
    return {r[0]: {"id": r[0], "title": r[1], "tags": r[2], "prompt": r[3]} for r in rows}


def infer_topic(tags: str) -> str:
    for topic in ["Dynamic Programming", "Backtracking", "Heap", "Graph",
                  "Binary Search", "Tree", "Two Pointers", "Sliding Window"]:
        if topic.lower() in tags.lower():
            return topic
    return "General"


def build_problem_section(p: dict) -> str:
    topic = infer_topic(p["tags"])
    hint = GENERATOR_HINTS.get(topic, "random inputs appropriate for the problem")
    pid = p["id"]
    return f"""---
### Problem: {pid} — {p['title']}
**Topic:** {topic} | **Tags:** {p['tags']}

```
{p['prompt'][:800]}
```

**Required output files for {pid} (each independent, no shared artifacts):**

1. `benchmark/{pid}/solution.py` — clean Python 3 `class Solution` with LeetCode method signature
2. `benchmark/{pid}/generate.py` — generates inputs at n=100, 1_000, 10_000, 100_000
   - Input type: {hint}
3. `benchmark/{pid}/bench.py` — timeit + tracemalloc at each scale (3 runs avg), writes results.json
4. `benchmark/{pid}/results.json`:
```json
{{
  "problem_id": "{pid}",
  "title": "{p['title']}",
  "topic": "{topic}",
  "benchmarks": [
    {{"n": 100,    "avg_time_ms": 0.0, "peak_memory_kb": 0}},
    {{"n": 1000,   "avg_time_ms": 0.0, "peak_memory_kb": 0}},
    {{"n": 10000,  "avg_time_ms": 0.0, "peak_memory_kb": 0}},
    {{"n": 100000, "avg_time_ms": 0.0, "peak_memory_kb": 0}}
  ],
  "empirical_time_complexity": "O(?)",
  "empirical_space_complexity": "O(?)",
  "notes": "reasoning based on timing ratios between consecutive scales"
}}
```
5. Fit the complexity curve from timing ratios (10x N → how much does time grow?) and fill in empirical complexity fields.
"""


def build_packed_task(pack_num: str, problems: list[dict]) -> tuple[str, str]:
    ids_str = " + ".join(p["id"] for p in problems)
    title = f"[Benchmark Pack {pack_num}] {ids_str}"
    body = f"""## Jules Benchmark Pack {pack_num}

### Goal
For each of the {len(problems)} problems below, independently produce:
solution.py, generate.py, bench.py, and results.json with empirical complexity.

Each problem is fully independent. Do not share data or code between them.

"""
    for p in problems:
        body += build_problem_section(p)

    return title, body


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    # Flatten and validate exactly 24 IDs
    all_ids = [pid for _, ids in PACKS for pid in ids]
    assert len(all_ids) == 24, f"Expected 24 IDs, got {len(all_ids)}"
    assert len(set(all_ids)) == 24, "Duplicate IDs in PACKS"

    # Load from DB
    problems = load_problems(all_ids)
    missing_from_db = [pid for pid in all_ids if pid not in problems]
    if missing_from_db:
        print(f"WARNING: {len(missing_from_db)} IDs not found in DB: {missing_from_db}")

    # Check which already have benchmark folders
    existing = {pid for pid in all_ids if os.path.isdir(f"benchmark/{pid}")}
    if existing:
        print(f"Skipping {len(existing)} already benchmarked: {sorted(existing)}")

    print(f"\n{'DRY RUN — ' if args.dry_run else ''}Dispatching {6 - len([p for _, ids in PACKS for p in ids if p in existing])} packs\n")

    dispatched = []
    skipped = []

    for pack_num, ids in PACKS:
        # Filter out already-done problems from this pack
        active = [problems[pid] for pid in ids if pid in problems and pid not in existing]
        already_done = [pid for pid in ids if pid in existing]

        if already_done:
            skipped.extend(already_done)

        if not active:
            print(f"Pack {pack_num}: all {len(ids)} already done — skipping")
            continue

        title, body = build_packed_task(pack_num, active)
        ids_in_pack = [p["id"] for p in active]

        if args.dry_run:
            print(f"Pack {pack_num}: {' + '.join(ids_in_pack)}")
            continue

        result = subprocess.run(
            ["jules", "new", "--repo", REPO, f"{title}\n\n{body}"],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            # Try to extract session ID from output
            session_id = result.stdout.strip().split()[-1] if result.stdout.strip() else "unknown"
            print(f"Pack {pack_num} dispatched — session: {session_id} — problems: {' + '.join(ids_in_pack)}")
            dispatched.extend(ids_in_pack)
        else:
            print(f"Pack {pack_num} FAILED (exit {result.returncode}) — NOT retrying")
            print(f"  stderr: {result.stderr[:200]}")

        time.sleep(3)

    print(f"\nSummary:")
    print(f"  Dispatched: {len(dispatched)} problems across {len([p for _, ids in PACKS for p in [ids] if any(pid not in existing for pid in p)])} packs")
    print(f"  Skipped (already done): {len(skipped)} — {sorted(skipped)}")


if __name__ == "__main__":
    main()
