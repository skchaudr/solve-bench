"""
Jules batch dispatcher — dispatches in verified batches of 15.
After each batch: confirms all sessions appear in jules remote list before continuing.
Skips problems already dispatched (checks existing sessions by problem ID).

Usage:
  python dispatch_jules_batched.py --dry-run
  python dispatch_jules_batched.py
  python dispatch_jules_batched.py --batch-size 15 --delay 2
"""
import subprocess
import argparse
import duckdb
import time
import re

DB_FILE = "solve-bench.db"
REPO = "skchaudr/solve-bench"
BATCH_SIZE = 15
DELAY = 2  # seconds between dispatches

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


def get_jules_sessions() -> dict[str, list[str]]:
    """Return {'Completed': [...ids], 'Progress': [...ids], ...} for solve-bench sessions."""
    result = subprocess.run(
        ["jules", "remote", "list", "--session"],
        capture_output=True, text=True
    )
    sessions: dict[str, list[str]] = {"Completed": [], "Progress": [], "other": []}
    for line in result.stdout.splitlines():
        if "solve-bench" not in line:
            continue
        match_id = re.search(r"\[Benchmark\]\s+(lc_\d+)", line)
        if not match_id:
            continue
        pid = match_id.group(1)
        if "Progress" in line:
            sessions["Progress"].append(pid)
        elif "Completed" in line:
            sessions["Completed"].append(pid)
        else:
            sessions["other"].append(pid)
    return sessions


def get_already_dispatched() -> set[str]:
    """All problem IDs that have any Jules session (regardless of status)."""
    sessions = get_jules_sessions()
    return set(sessions["Completed"] + sessions["Progress"] + sessions["other"])


def get_available_slots(max_concurrent: int = 15) -> int:
    """How many new tasks can be dispatched right now."""
    in_progress = len(get_jules_sessions()["Progress"])
    return max(0, max_concurrent - in_progress)


def wait_for_slots(needed: int, max_concurrent: int = 15, poll_interval: int = 30) -> int:
    """Block until at least `needed` slots are free. Returns actual available slots."""
    while True:
        slots = get_available_slots(max_concurrent)
        if slots >= needed:
            return slots
        in_progress = max_concurrent - slots
        print(f"  ⏳ {in_progress} tasks In Progress, {slots} slots free (need {needed}) — checking again in {poll_interval}s...", flush=True)
        time.sleep(poll_interval)


def get_all_problems(conn) -> list[dict]:
    problems = []
    seen = set()
    for topic, condition in TOPIC_FILTERS.items():
        rows = conn.execute(
            f"SELECT id, title, tags, prompt FROM problems "
            f"WHERE difficulty='medium' AND {condition} ORDER BY id LIMIT 10"
        ).fetchall()
        for pid, title, tags, prompt in rows:
            if pid not in seen:
                seen.add(pid)
                problems.append({
                    "id": pid, "title": title,
                    "tags": tags, "prompt": prompt,
                    "topic": topic
                })
    return problems


def build_task(p: dict) -> str:
    hint = GENERATOR_HINTS.get(p["topic"], "random inputs appropriate for the problem")
    return f"""## [Jules Benchmark] {p['id']} — {p['title']}

### Goal
Write a solution, generate synthetic stress-test data, benchmark at scale, report empirical complexity curve.

**Topic:** {p['topic']} | **Tags:** {p['tags']}

### Problem
```
{p['prompt'][:1200]}
```

### Tasks
1. `benchmark/{p['id']}/solution.py` — clean Python 3 solution
2. `benchmark/{p['id']}/generate.py` — synthetic inputs at n=100, 1_000, 10_000, 100_000
   - Input type: {hint}
3. `benchmark/{p['id']}/bench.py` — timeit + tracemalloc at each scale (3 runs avg)
4. `benchmark/{p['id']}/results.json`:
```json
{{
  "problem_id": "{p['id']}",
  "title": "{p['title']}",
  "topic": "{p['topic']}",
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
5. Fit the complexity curve from timing ratios and fill in empirical_time/space_complexity.
"""


def dispatch_one(p: dict, dry_run: bool) -> bool:
    title = f"[Benchmark] {p['id']} — {p['title']} ({p['topic']})"
    body = build_task(p)
    if dry_run:
        print(f"  DRY: {p['id']} — {p['title'][:40]}")
        return True
    result = subprocess.run(
        ["jules", "new", "--repo", REPO, f"{title}\n\n{body}"],
        capture_output=True, text=True
    )
    return result.returncode == 0


def verify_batch(expected_ids: list[str], timeout: int = 30) -> tuple[set, set]:
    """Wait up to timeout seconds for all expected IDs to appear in jules list."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        found = get_already_dispatched()
        confirmed = {pid for pid in expected_ids if pid in found}
        missing = {pid for pid in expected_ids if pid not in found}
        if not missing:
            return confirmed, missing
        time.sleep(3)
    found = get_already_dispatched()
    confirmed = {pid for pid in expected_ids if pid in found}
    missing = {pid for pid in expected_ids if pid not in found}
    return confirmed, missing


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--batch-size", type=int, default=BATCH_SIZE)
    parser.add_argument("--delay", type=float, default=DELAY)
    args = parser.parse_args()

    already_done = get_already_dispatched()
    print(f"Already dispatched: {len(already_done)} problems")

    with duckdb.connect(DB_FILE) as conn:
        all_problems = get_all_problems(conn)

    remaining = [p for p in all_problems if p["id"] not in already_done]
    print(f"Remaining to dispatch: {len(remaining)}")
    print(f"Batch size: {args.batch_size} | Delay: {args.delay}s\n")

    total_dispatched = 0
    total_confirmed = 0

    batch_num = 0
    i = 0
    while i < len(remaining):
        # Wait until we have at least 1 free slot
        if not args.dry_run:
            slots = wait_for_slots(1, poll_interval=30)
        else:
            slots = args.batch_size

        # Only dispatch as many as we have slots for, capped at batch_size
        take = min(args.batch_size, slots, len(remaining) - i)
        batch = remaining[i:i + take]
        batch_num += 1
        print(f"── Batch {batch_num} ({len(batch)} problems, {slots} slots free) ──")

        sent = []
        for p in batch:
            ok = dispatch_one(p, args.dry_run)
            if ok:
                sent.append(p["id"])
                print(f"  ✅ {p['id']} — {p['title'][:40]}", flush=True)
            else:
                print(f"  ❌ {p['id']} — dispatch failed", flush=True)
            time.sleep(args.delay)

        total_dispatched += len(sent)
        i += take

        if args.dry_run:
            print(f"  [dry run — skipping verification]\n")
            continue

        # Verify all sent tasks actually registered
        print(f"  Verifying {len(sent)} tasks registered with Jules...", flush=True)
        confirmed, missing = verify_batch(sent)
        total_confirmed += len(confirmed)

        if missing:
            print(f"  ⚠️  {len(missing)} tasks dropped: {', '.join(sorted(missing))}")
            print(f"  ✅ {len(confirmed)}/{len(sent)} confirmed\n")
            # Put dropped ones back in remaining so we retry
            dropped_problems = [p for p in batch if p["id"] in missing]
            remaining = remaining[:i] + dropped_problems + remaining[i:]
        else:
            print(f"  ✅ All {len(confirmed)} confirmed\n")

    print(f"\nTotal dispatched: {total_dispatched}")
    if not args.dry_run:
        print(f"Total confirmed:  {total_confirmed}")


if __name__ == "__main__":
    main()
