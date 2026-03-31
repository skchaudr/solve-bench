"""
compare.py — Run models on a benchmarked problem and compare against Jules' baseline.

Flow:
  1. Fetch model solutions via solve.py (writes to runs table)
  2. For each model: swap solution into benchmark/lc_XXXX/solution.py, run bench.py
  3. Restore original solution.py
  4. Display side-by-side timing + complexity table vs Jules baseline

Usage:
  python compare.py --problem_id lc_15
  python compare.py --problem_id lc_15 --models claude gemini gpt-4o
  python compare.py --problem_id lc_15 --skip-solve   # use runs already in DB
"""
import os
import sys
import json
import shutil
import subprocess
import argparse
import duckdb

from rich.console import Console
from rich.table import Table
from rich import box

DB_FILE = "solve-bench.db"
console = Console()

SCALES = [100, 1000, 10000, 100000]


def load_jules_results(problem_id: str) -> dict | None:
    path = f"benchmark/{problem_id}/results.json"
    if not os.path.exists(path):
        return None
    with open(path) as f:
        return json.load(f)


def get_latest_runs(problem_id: str, models: list[str]) -> dict[str, dict]:
    """Fetch most recent run per model from DB."""
    runs = {}
    with duckdb.connect(DB_FILE) as conn:
        for model in models:
            row = conn.execute(
                """SELECT id, solution_code, reasoning, time_complexity, space_complexity
                   FROM runs
                   WHERE problem_id = ? AND model = ? AND solution_code != '' AND solution_code != 'ERROR'
                   ORDER BY run_at DESC LIMIT 1""",
                (problem_id, model)
            ).fetchone()
            if row:
                runs[model] = {
                    "run_id": row[0],
                    "solution_code": row[1],
                    "reasoning": row[2],
                    "time_complexity": row[3],
                    "space_complexity": row[4],
                }
    return runs


def run_bench_with_solution(problem_id: str, solution_code: str, timeout: int = 120) -> dict | None:
    """
    Temporarily swap solution.py, run bench.py, capture results.json, restore original.
    Returns parsed results dict or None on failure.
    """
    solution_path = f"benchmark/{problem_id}/solution.py"
    bench_path = f"benchmark/{problem_id}/bench.py"
    results_path = f"benchmark/{problem_id}/results.json"
    backup_path = f"benchmark/{problem_id}/solution.py.bak"

    # Back up original
    shutil.copy2(solution_path, backup_path)

    try:
        # Wrap in Solution class if model returned a bare function
        if "class Solution" not in solution_code:
            indented = "\n".join("    " + line for line in solution_code.splitlines())
            solution_code = f"class Solution:\n{indented}\n"

        # Write model solution
        with open(solution_path, "w") as f:
            f.write(solution_code)

        # Back up Jules results before bench.py overwrites them
        with open(results_path) as f:
            original_results = json.load(f)

        # Run bench.py from repo root using venv python
        venv_python = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".venv", "bin", "python")
        result = subprocess.run(
            [venv_python, bench_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

        if result.returncode != 0:
            console.print(f"[red]bench.py failed:[/red] {result.stderr[:300]}")
            return None

        # Read model results
        with open(results_path) as f:
            model_results = json.load(f)

        return model_results

    except subprocess.TimeoutExpired:
        console.print(f"[yellow]bench.py timed out after {timeout}s[/yellow]")
        return None
    except Exception as e:
        console.print(f"[red]Error running bench:[/red] {e}")
        return None
    finally:
        # Always restore original solution and results
        shutil.copy2(backup_path, solution_path)
        os.remove(backup_path)
        with open(results_path, "w") as f:
            json.dump(original_results, f, indent=2)


def fmt_time(ms: float) -> str:
    if ms < 1:
        return f"{ms*1000:.1f}µs"
    if ms < 1000:
        return f"{ms:.1f}ms"
    return f"{ms/1000:.2f}s"


def fmt_ratio(model_ms: float, jules_ms: float) -> str:
    if jules_ms == 0:
        return "—"
    ratio = model_ms / jules_ms
    if ratio < 0.8:
        return f"[green]{ratio:.1f}x faster[/green]"
    if ratio > 1.25:
        return f"[red]{ratio:.1f}x slower[/red]"
    return f"[dim]{ratio:.1f}x[/dim]"


def display_comparison(problem_id: str, jules: dict, model_results: dict[str, dict | None], model_complexities: dict[str, dict]):
    title = jules.get("title", problem_id)
    topic = jules.get("topic", "")
    console.print(f"\n[bold cyan]{title}[/bold cyan] ([dim]{problem_id} · {topic}[/dim])\n")

    # Complexity summary table
    comp_table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    comp_table.add_column("Model", style="cyan", min_width=10)
    comp_table.add_column("Time Complexity")
    comp_table.add_column("Space Complexity")
    comp_table.add_column("Source")

    comp_table.add_row(
        "Jules",
        jules.get("empirical_time_complexity", "?"),
        jules.get("empirical_space_complexity", "?"),
        "empirical",
    )
    for model, r in model_results.items():
        tc = model_complexities.get(model, {}).get("time_complexity", "?")
        sc = model_complexities.get(model, {}).get("space_complexity", "?")
        comp_table.add_row(model, tc, sc, "self-reported")

    console.print(comp_table)

    # Timing table
    jules_benchmarks = {b["n"]: b for b in jules.get("benchmarks", [])}

    timing_table = Table(box=box.SIMPLE, show_header=True, header_style="bold")
    timing_table.add_column("n", style="dim")
    timing_table.add_column("Jules (baseline)", style="yellow")
    for model in model_results:
        timing_table.add_column(model, style="cyan")

    for n in SCALES:
        jules_b = jules_benchmarks.get(n, {})
        jules_ms = jules_b.get("avg_time_ms", 0)
        row = [str(n), fmt_time(jules_ms)]

        for model, mr in model_results.items():
            if mr is None:
                row.append("[red]FAILED[/red]")
                continue
            model_benchmarks = {b["n"]: b for b in mr.get("benchmarks", [])}
            mb = model_benchmarks.get(n, {})
            model_ms = mb.get("avg_time_ms")
            if model_ms is None:
                row.append("—")
            else:
                row.append(f"{fmt_time(model_ms)} {fmt_ratio(model_ms, jules_ms)}")

        timing_table.add_row(*row)

    console.print(timing_table)

    # Notes
    console.print(f"[dim]Jules notes:[/dim] {jules.get('notes', '')}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--problem_id", required=True)
    parser.add_argument("--models", nargs="+", default=["claude", "gemini"])
    parser.add_argument("--skip-solve", action="store_true", help="Use runs already in DB, don't call models")
    parser.add_argument("--timeout", type=int, default=120, help="Bench timeout per model in seconds")
    args = parser.parse_args()

    problem_id = args.problem_id

    # Check benchmark exists
    jules_results = load_jules_results(problem_id)
    if not jules_results:
        console.print(f"[red]No Jules benchmark found for {problem_id}.[/red] Run Jules dispatch first.")
        sys.exit(1)

    # Step 1: Get model solutions
    if not args.skip_solve:
        console.print(f"[bold]Solving {problem_id} with models: {', '.join(args.models)}...[/bold]")
        import solve
        solve.solve(problem_id, args.models)
    else:
        console.print(f"[dim]--skip-solve: using existing runs from DB[/dim]")

    # Step 2: Fetch runs from DB
    runs = get_latest_runs(problem_id, args.models)
    if not runs:
        console.print(f"[red]No runs found in DB for {problem_id}.[/red]")
        sys.exit(1)

    # Step 3: Run bench.py with each model's solution
    model_bench_results = {}
    model_complexities = {}
    for model, run in runs.items():
        console.print(f"\n[bold]Benchmarking {model} solution...[/bold]")
        model_complexities[model] = {
            "time_complexity": run["time_complexity"],
            "space_complexity": run["space_complexity"],
        }
        bench_result = run_bench_with_solution(problem_id, run["solution_code"], timeout=args.timeout)
        model_bench_results[model] = bench_result

    # Step 4: Display
    display_comparison(problem_id, jules_results, model_bench_results, model_complexities)


if __name__ == "__main__":
    main()
