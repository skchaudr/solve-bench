import os
import json
import uuid
import duckdb
import argparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.console import Console
from rich.table import Table

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser("~/.config/solve-bench/sa-key.json")

DB_FILE = "solve-bench.db"
GCP_PROJECT = "gen-lang-client-0824562549"
GCP_REGION = "us-central1"

SOLVER_SYSTEM = """You are an expert competitive programming solver. Solve the given problem and return ONLY a raw JSON object.

REQUIRED JSON KEYS (all mandatory):
- "solution_code": string — complete Python 3 solution using standard LeetCode class format
- "reasoning": string — 2-4 sentence explanation of your algorithm and time/space complexity
- "time_complexity": string — e.g. "O(N)", "O(N log N)", "O(N^2)"
- "space_complexity": string — e.g. "O(1)", "O(N)"
- "language": string — always "python"

SOLUTION FORMAT RULES:
- solution_code MUST use the standard LeetCode class format: class Solution with a method that takes self as first argument
- Import statements go BEFORE the class definition
- No driver code, no stdin parsing, no if __name__ == "__main__" blocks

VALID solution_code EXAMPLE:
"from typing import List\\nclass Solution:\\n    def twoSum(self, nums: List[int], target: int) -> List[int]:\\n        seen = {}\\n        for i, n in enumerate(nums):\\n            if target - n in seen:\\n                return [seen[target - n], i]\\n            seen[n] = i"

CRITICAL OUTPUT RULES — VIOLATIONS WILL BREAK THE PARSER:
- Your ENTIRE response must be a single JSON object starting with { and ending with }
- NEVER use markdown code fences (no ```, no ```json, no ```python)
- NEVER add any text before or after the JSON object
- NEVER add comments inside the JSON

---

PROBLEM:
{problem}"""

console = Console()


def strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        end = -1 if lines[-1].strip() == "```" else len(lines)
        text = "\n".join(lines[1:end])
    return text.strip()


def parse_response(text: str) -> dict:
    return json.loads(strip_fences(text))


def get_problem(problem_id: str) -> dict:
    with duckdb.connect(DB_FILE) as conn:
        row = conn.execute(
            "SELECT id, title, prompt FROM problems WHERE id = ?", (problem_id,)
        ).fetchone()
    if not row:
        raise ValueError(f"Problem '{problem_id}' not found.")
    return {"id": row[0], "title": row[1], "prompt": row[2]}


def call_gemini(prompt: str) -> dict:
    from google import genai
    from google.genai import types

    client = genai.Client(vertexai=True, project=GCP_PROJECT, location="global")
    response = client.models.generate_content(
        model="gemini-3.1-pro-preview",
        contents=SOLVER_SYSTEM.replace("{problem}", prompt),
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            max_output_tokens=8192,
        ),
    )
    return parse_response(response.text)


def call_claude(prompt: str) -> dict:
    import anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY not set.")
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8192,
        messages=[{"role": "user", "content": SOLVER_SYSTEM.replace("{problem}", prompt)}],
    )
    return parse_response(message.content[0].text)


def call_gpt(prompt: str) -> dict:
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not set.")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[{"role": "user", "content": SOLVER_SYSTEM.replace("{problem}", prompt)}],
        max_tokens=8192,
    )
    return parse_response(response.choices[0].message.content)


MODELS = {
    "gemini": call_gemini,    # gemini-3.1-pro-preview (Vertex AI)
    "claude": call_claude,    # claude-sonnet-4-6 (Vertex AI / Anthropic)
    "gpt-4o": call_gpt,       # placeholder — swap for any Model Garden model
}

DEFAULT_MODELS = ["gemini", "claude"]


def insert_run(problem_id: str, model: str, result: dict, error: str | None = None) -> str:
    run_id = f"run_{uuid.uuid4().hex[:8]}"
    with duckdb.connect(DB_FILE) as conn:
        conn.execute(
            """
            INSERT INTO runs
              (id, problem_id, model, solution_code, reasoning,
               time_complexity, space_complexity, passed_tests, run_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                problem_id,
                model,
                result.get("solution_code", "") if not error else "",
                error if error else result.get("reasoning", ""),
                result.get("time_complexity", "") if not error else "ERROR",
                result.get("space_complexity", "") if not error else "ERROR",
                None,
                datetime.now(),
            ),
        )
    return run_id


def solve(problem_id: str, models: list[str]):
    problem = get_problem(problem_id)
    console.print(f"\n[bold]Problem:[/bold] {problem['title']} ([cyan]{problem_id}[/cyan])")
    console.print(f"[bold]Models:[/bold]  {', '.join(models)}\n")

    results = {}

    def run_model(name):
        fn = MODELS[name]
        try:
            data = fn(problem["prompt"])
            run_id = insert_run(problem_id, name, data)
            results[name] = (run_id, data.get("time_complexity", "?"), None)
        except Exception as e:
            err = str(e)
            run_id = insert_run(problem_id, name, {}, error=err)
            results[name] = (run_id, "ERROR", err)

    with ThreadPoolExecutor(max_workers=len(models)) as pool:
        futures = {pool.submit(run_model, m): m for m in models}
        for f in as_completed(futures):
            f.result()

    table = Table(title="Run Summary", show_header=True, header_style="bold magenta")
    table.add_column("Model", style="cyan", width=12)
    table.add_column("Run ID", style="dim", width=16)
    table.add_column("Time Complexity", width=18)
    table.add_column("Status")

    for model in models:
        run_id, tc, err = results.get(model, ("—", "—", "missing"))
        status = "[red]FAILED[/red]" if err else "[green]OK[/green]"
        table.add_row(model, run_id, tc, status)

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="solve-bench: Run all models on a problem")
    parser.add_argument("--problem_id", required=True, help="e.g. lc_200")
    parser.add_argument(
        "--models",
        nargs="+",
        choices=list(MODELS.keys()),
        default=DEFAULT_MODELS,
    )
    args = parser.parse_args()
    solve(args.problem_id, args.models)


if __name__ == "__main__":
    main()
