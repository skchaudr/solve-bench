import uuid
import duckdb
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.syntax import Syntax
from rich.prompt import Prompt, Confirm
from rich import box

DB_FILE = "solve-bench.db"
MODELS = ["gemini", "claude", "gpt-4o"]

console = Console()


# ── Data helpers ──────────────────────────────────────────────────────────────

def list_problems() -> list[tuple]:
    with duckdb.connect(DB_FILE) as conn:
        return conn.execute("""
            SELECT p.id, p.title, p.difficulty, p.tags,
                   COUNT(r.id) AS run_count
            FROM problems p
            LEFT JOIN runs r ON r.problem_id = p.id
            GROUP BY p.id, p.title, p.difficulty, p.tags
            ORDER BY p.difficulty DESC, p.title
        """).fetchall()


def get_runs_for_problem(problem_id: str) -> list[tuple]:
    with duckdb.connect(DB_FILE) as conn:
        return conn.execute("""
            SELECT id, model, solution_code, reasoning,
                   time_complexity, space_complexity, run_at
            FROM runs WHERE problem_id = ?
            ORDER BY model
        """, (problem_id,)).fetchall()


def get_annotations(run_id: str) -> list[tuple]:
    with duckdb.connect(DB_FILE) as conn:
        return conn.execute(
            "SELECT your_verdict, notes, reviewed_at FROM annotations WHERE run_id = ?",
            (run_id,)
        ).fetchall()


def insert_annotation(run_id: str, verdict: str, notes: str):
    ann_id = f"ann_{uuid.uuid4().hex[:8]}"
    with duckdb.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO annotations VALUES (?, ?, ?, ?, ?)",
            (ann_id, run_id, verdict, notes, datetime.now()),
        )


# ── Display helpers ───────────────────────────────────────────────────────────

DIFF_COLOR = {"easy": "green", "medium": "yellow", "hard": "red"}


def show_problem_list(problems: list[tuple]):
    table = Table(
        title="[bold]Problems[/bold]",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("#", style="dim", width=4)
    table.add_column("ID", style="cyan", width=12)
    table.add_column("Title", width=38)
    table.add_column("Difficulty", width=10)
    table.add_column("Tags", width=40, overflow="fold")
    table.add_column("Runs", justify="right", width=5)

    for i, (pid, title, diff, tags, runs) in enumerate(problems, 1):
        color = DIFF_COLOR.get(diff, "white")
        table.add_row(
            str(i), pid, title,
            f"[{color}]{diff}[/{color}]",
            tags or "—",
            str(runs),
        )
    console.print(table)


def show_runs(problem_id: str, title: str, runs: list[tuple]):
    console.print(f"\n[bold cyan]{title}[/bold cyan]  ([dim]{problem_id}[/dim])\n")

    panels = []
    for run_id, model, code, reasoning, tc, sc, run_at in runs:
        anns = get_annotations(run_id)
        ann_text = ""
        if anns:
            for verdict, notes, ts in anns:
                ann_text += f"\n[bold]Verdict:[/bold] {verdict}  [bold]Notes:[/bold] {notes}"

        header = (
            f"[bold]{model}[/bold]  [dim]{run_id}[/dim]\n"
            f"Time: [yellow]{tc or '?'}[/yellow]  Space: [yellow]{sc or '?'}[/yellow]\n"
            f"[italic]{reasoning or '—'}[/italic]"
            + ann_text
        )

        syntax = Syntax(
            code or "# (no solution)",
            "python",
            theme="monokai",
            line_numbers=True,
        )
        panels.append(Panel(
            f"{header}\n\n{syntax.highlight(code or '')}",
            title=model,
            border_style="blue",
            width=console.width // max(len(runs), 1) - 2,
        ))

    console.print(Columns(panels, equal=True, expand=True))
    return {r[1]: r[0] for r in runs}  # model → run_id


# ── Main flow ─────────────────────────────────────────────────────────────────

def annotate_flow(model_to_run_id: dict):
    model = Prompt.ask(
        "\nAnnotate which model?",
        choices=list(model_to_run_id.keys()) + ["skip"],
        default="skip",
    )
    if model == "skip":
        return
    verdict = Prompt.ask(
        "Verdict",
        choices=["correct", "wrong", "partial"],
    )
    notes = Prompt.ask("Notes (optional)", default="")
    insert_annotation(model_to_run_id[model], verdict, notes)
    console.print("[green]✅ Annotation saved.[/green]")


def main():
    while True:
        console.clear()
        problems = list_problems()
        if not problems:
            console.print("[yellow]No problems in DB. Run import_bulk.py first.[/yellow]")
            return

        show_problem_list(problems)

        choice = Prompt.ask(
            "\nEnter # or problem ID to inspect (or [bold]q[/bold] to quit)",
            default="q",
        )
        if choice.lower() == "q":
            break

        # Resolve by number or ID
        problem = None
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(problems):
                problem = problems[idx]
        else:
            for p in problems:
                if p[0].lower() == choice.lower():
                    problem = p
                    break

        if not problem:
            console.print("[red]Not found.[/red]")
            Prompt.ask("Press Enter to continue")
            continue

        pid, title, diff, tags, _ = problem
        runs = get_runs_for_problem(pid)
        if not runs:
            console.print(f"[yellow]No runs yet for {pid}.[/yellow]")
            Prompt.ask("Press Enter to continue")
            continue

        model_to_run_id = show_runs(pid, title, runs)

        if Confirm.ask("\nAdd annotation?", default=False):
            annotate_flow(model_to_run_id)

        Prompt.ask("\nPress Enter to go back")


if __name__ == "__main__":
    main()
