"""
Dispatches Jules tasks as GitHub issues to skchaudr/AI-sparring-coding-problems.
Each issue = one topic batch of ~10 problems.

Jules will:
1. Write a clean Python solution for each problem
2. Write pytest test cases from the problem description + examples
3. Run all tests and record pass/fail
4. Output results as JSON at results/<topic>_results.json

Usage:
  python dispatch_jules.py --dry-run        # preview issues
  python dispatch_jules.py                  # create issues via gh CLI
  python dispatch_jules.py --topics "Tree"  # single topic
"""
import subprocess
import argparse
import duckdb

DB_FILE = "solve-bench.db"
REPO = "skchaudr/AI-sparring-coding-problems"

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


def build_issue(topic: str, problems: list[dict]) -> str:
    problem_sections = ""
    for p in problems:
        problem_sections += f"""
<details>
<summary><strong>{p['id']} — {p['title']}</strong> ({p['tags']})</summary>

```
{p['prompt'][:1200]}
```
</details>
"""

    ids = ", ".join(p["id"] for p in problems)

    return f"""## [Jules Task] {topic} — Solve, Test & Validate

### Context
This is part of the `solve-bench` project — a benchmark comparing how AI models solve algorithmic problems.

### Your job for each problem below:
1. **Write a clean Python 3 solution** in `problems/leetcode/medium/{topic.lower().replace(' ', '-')}/<problem_id>/solution.py`
2. **Write pytest test cases** in `problems/leetcode/medium/{topic.lower().replace(' ', '-')}/<problem_id>/test_solution.py` — derive test cases from the examples and constraints in the problem description
3. **Run the tests** and confirm they pass against your solution
4. **Output a results JSON** at `results/{topic.lower().replace(' ', '_')}_results.json` in this format:

```json
{{
  "topic": "{topic}",
  "results": [
    {{
      "problem_id": "lc_XXX",
      "title": "Problem Title",
      "solved": true,
      "test_count": 5,
      "notes": "optional notes on approach or edge cases"
    }}
  ]
}}
```

### Problems ({len(problems)} total)
`{ids}`

---

{problem_sections}
"""


def create_issue(title: str, body: str, dry_run: bool):
    if dry_run:
        print(f"\n{'='*60}")
        print(f"TITLE: {title}")
        print(f"BODY: {len(body)} chars")
        print(body[:300] + "...\n")
        return True

    result = subprocess.run(
        ["jules", "new", "--repo", REPO, f"{title}\n\n{body}"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✅ {title}\n   {result.stdout.strip()}")
        return True
    else:
        print(f"❌ {title}\n   {result.stderr.strip()}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--topics", nargs="+", choices=list(TOPIC_FILTERS.keys()),
                        default=list(TOPIC_FILTERS.keys()))
    args = parser.parse_args()

    with duckdb.connect(DB_FILE) as conn:
        total = 0
        for topic in args.topics:
            problems = get_problems(conn, TOPIC_FILTERS[topic])
            if not problems:
                print(f"⚠️  No problems for {topic}")
                continue
            title = f"[Jules] {topic} — Solve & Test ({len(problems)} problems)"
            body = build_issue(topic, problems)
            ok = create_issue(title, body, args.dry_run)
            if ok:
                total += 1
                print(f"{'DRY' if args.dry_run else 'SENT'}: {topic} ({len(problems)} problems)")

    print(f"\n{'Would dispatch' if args.dry_run else 'Dispatched'} {total} Jules tasks")


if __name__ == "__main__":
    main()
