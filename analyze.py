import os
import json
import duckdb
import argparse

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser("~/.config/solve-bench/sa-key.json")

DB_FILE = "solve-bench.db"
GCP_PROJECT = "gen-lang-client-0824562549"
GCP_REGION = "us-central1"

ANALYZER_SYSTEM = """You are a code complexity analyzer. Given a Python solution, return ONLY valid JSON with no markdown, no backticks, no explanation outside the JSON. Use \\n for newlines in any code references.

Format: {"time_complexity": "O(...)", "space_complexity": "O(...)", "explanation": "<A single sentence that justifies both the time and space complexity>"}

Python Solution:

def sum_array(arr):
    total = 0
    for x in arr:
        total += x
    return total

JSON Output:
{
  "time_complexity": "O(n)",
  "space_complexity": "O(1)",
  "explanation": "The time complexity is O(n) because it iterates through the array once, and space complexity is O(1) as it uses a constant amount of extra space."
}

Python Solution:
{code}

JSON Output:"""

console = Console()


def strip_fences(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        end = -1 if lines[-1].strip() == "```" else len(lines)
        text = "\n".join(lines[1:end])
    return text.strip()


def call_gemini_analyzer(code: str) -> dict:
    import vertexai
    from vertexai.generative_models import GenerativeModel, GenerationConfig

    vertexai.init(project=GCP_PROJECT, location=GCP_REGION)
    model = GenerativeModel("gemini-2.5-pro")
    response = model.generate_content(
        ANALYZER_SYSTEM.format(code=strip_fences(code)),
        generation_config=GenerationConfig(
            response_mime_type="application/json",
            max_output_tokens=1024,
        ),
    )
    return json.loads(strip_fences(response.text))


def get_pending_runs(run_id: str | None) -> list[tuple]:
    with duckdb.connect(DB_FILE) as conn:
        if run_id:
            rows = conn.execute(
                "SELECT id, solution_code FROM runs WHERE id = ?", (run_id,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, solution_code FROM runs WHERE time_complexity IS NULL AND solution_code != ''"
            ).fetchall()
    return rows


def update_run(run_id: str, time_c: str, space_c: str, explanation: str):
    with duckdb.connect(DB_FILE) as conn:
        conn.execute(
            """
            UPDATE runs
            SET time_complexity = ?, space_complexity = ?, reasoning = reasoning || '\n\n[Analyzer] ' || ?
            WHERE id = ?
            """,
            (time_c, space_c, explanation, run_id),
        )


def main():
    parser = argparse.ArgumentParser(description="solve-bench: Analyze complexity of stored runs")
    parser.add_argument("--run_id", help="Analyze a single run by ID")
    args = parser.parse_args()

    runs = get_pending_runs(args.run_id)
    if not runs:
        console.print("[yellow]No runs to analyze.[/yellow]")
        return

    console.print(f"Analyzing [bold]{len(runs)}[/bold] run(s)...\n")

    ok = err = 0
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Analyzing...", total=len(runs))

        for run_id, solution_code in runs:
            progress.update(task, description=f"[cyan]{run_id}[/cyan]")
            try:
                result = call_gemini_analyzer(solution_code)
                update_run(
                    run_id,
                    result.get("time_complexity", "?"),
                    result.get("space_complexity", "?"),
                    result.get("explanation", ""),
                )
                ok += 1
            except Exception as e:
                console.print(f"  [red]✗ {run_id}:[/red] {e}")
                err += 1
            progress.advance(task)

    console.print(f"\n[green]✅ {ok} analyzed[/green]  [red]✗ {err} failed[/red]")


if __name__ == "__main__":
    main()
