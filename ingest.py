import duckdb
import argparse
import sys
import uuid
from datetime import datetime

DB_FILE = "solve-bench.db"

def init_db():
    """Creates the three core tables if they don't exist."""
    with duckdb.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS problems (
                id VARCHAR PRIMARY KEY,
                source VARCHAR,
                title VARCHAR,
                difficulty VARCHAR,
                tags VARCHAR,
                prompt TEXT,
                created_at TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS runs (
                id VARCHAR PRIMARY KEY,
                problem_id VARCHAR,
                model VARCHAR,
                solution_code TEXT,
                reasoning TEXT,
                time_complexity VARCHAR,
                space_complexity VARCHAR,
                passed_tests BOOLEAN,
                run_at TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS annotations (
                id VARCHAR PRIMARY KEY,
                run_id VARCHAR,
                your_verdict VARCHAR,
                notes TEXT,
                reviewed_at TIMESTAMP
            );
        """)
    print(f"✅ Schema initialized successfully in '{DB_FILE}'")

def add_problem(source, title, difficulty, tags):
    """Reads the prompt from stdin and inserts the problem into DuckDB."""
    print("Paste the problem description (Press Ctrl+D when finished):")
    prompt = sys.stdin.read().strip()

    if not prompt:
        print("❌ Error: Problem description cannot be empty.")
        sys.exit(1)

    problem_id = f"prob_{uuid.uuid4().hex[:8]}"
    created_at = datetime.now()

    with duckdb.connect(DB_FILE) as conn:
        conn.execute("""
            INSERT INTO problems (id, source, title, difficulty, tags, prompt, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (problem_id, source, title, difficulty, tags, prompt, created_at))

    print(f"\n✅ Problem '{title}' ingested successfully! (ID: {problem_id})")

def main():
    parser = argparse.ArgumentParser(description="solve-bench: Ingest layer")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init", help="Initialize the DuckDB database and schema")

    add_parser = subparsers.add_parser("add", help="Add a new problem")
    add_parser.add_argument("--source", required=True, help="e.g., LeetCode, Codeforces, HR")
    add_parser.add_argument("--title", required=True, help="Name of the problem")
    add_parser.add_argument("--difficulty", choices=["easy", "medium", "hard"], required=True)
    add_parser.add_argument("--tags", default="", help="Comma-separated tags (e.g., 'graph,dp')")

    args = parser.parse_args()

    if args.command == "init":
        init_db()
    elif args.command == "add":
        add_problem(args.source, args.title, args.difficulty, args.tags)

if __name__ == "__main__":
    main()
