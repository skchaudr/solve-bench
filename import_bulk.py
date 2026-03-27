import json
import duckdb
from datetime import datetime

DB_FILE = "solve-bench.db"
PROBLEMS_FILE = "leetcode-problems/merged_problems.json"

TARGET_MEDIUM_TOPICS = {
    "Dynamic Programming", "Graph", "Tree", "Binary Search",
    "Sliding Window", "Two Pointers", "Backtracking", "Heap (Priority Queue)",
}


def build_prompt(p: dict) -> str:
    parts = [p["description"].strip()]

    if p.get("examples"):
        parts.append("\nExamples:")
        for ex in p["examples"]:
            parts.append(ex["example_text"].strip())

    if p.get("constraints"):
        parts.append("\nConstraints:")
        for c in p["constraints"]:
            parts.append(f"- {c}")

    return "\n".join(parts)


def should_include(p: dict) -> bool:
    diff = p["difficulty"].lower()
    if diff == "hard":
        return True
    if diff == "medium":
        return bool(TARGET_MEDIUM_TOPICS & set(p.get("topics", [])))
    return False


def main():
    with open(PROBLEMS_FILE) as f:
        problems = json.load(f)["questions"]

    filtered = [p for p in problems if should_include(p)]
    print(f"Filtered: {len(filtered)} problems ({sum(1 for p in filtered if p['difficulty']=='Hard')} hard, "
          f"{sum(1 for p in filtered if p['difficulty']=='Medium')} medium)")

    rows = []
    for p in filtered:
        rows.append((
            f"lc_{p['frontend_id']}",
            "LeetCode",
            p["title"],
            p["difficulty"].lower(),
            ", ".join(p.get("topics", [])),
            build_prompt(p),
            datetime.now(),
        ))

    with duckdb.connect(DB_FILE) as conn:
        # DuckDB doesn't support INSERT OR IGNORE; use a temp table + anti-join
        conn.execute("""
            CREATE TEMP TABLE _import (
                id VARCHAR, source VARCHAR, title VARCHAR, difficulty VARCHAR,
                tags VARCHAR, prompt TEXT, created_at TIMESTAMP
            )
        """)
        conn.executemany("INSERT INTO _import VALUES (?, ?, ?, ?, ?, ?, ?)", rows)
        before = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
        conn.execute("""
            INSERT INTO problems
            SELECT i.* FROM _import i
            LEFT JOIN problems p ON p.id = i.id
            WHERE p.id IS NULL
        """)
        after = conn.execute("SELECT COUNT(*) FROM problems").fetchone()[0]
        inserted = after - before

    print(f"✅ Inserted {inserted} new problems into '{DB_FILE}' (skipped {len(rows) - inserted} duplicates)")


if __name__ == "__main__":
    main()
