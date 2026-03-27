import duckdb
import argparse
import uuid
import json
import os
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

DB_FILE = "solve-bench.db"
SA_KEY_PATH = os.path.expanduser("~/.config/solve-bench/sa-key.json")
GCP_PROJECT = "gen-lang-client-0824562549"
GCP_REGION = "us-central1"

SYSTEM_PROMPT = """You are an expert competitive programmer. Given a coding problem, respond with a JSON object and nothing else — no markdown, no explanation outside the JSON.

The JSON must have exactly these keys:
{
  "solution_code": "<complete, runnable solution in Python>",
  "reasoning": "<brief explanation of the approach>",
  "language": "python",
  "time_complexity": "<Big-O, e.g. O(n log n)>",
  "space_complexity": "<Big-O, e.g. O(n)>"
}"""


def get_problem(problem_id: str) -> dict:
    with duckdb.connect(DB_FILE) as conn:
        row = conn.execute(
            "SELECT id, title, prompt FROM problems WHERE id = ?", (problem_id,)
        ).fetchone()
    if not row:
        raise ValueError(f"Problem '{problem_id}' not found in DB.")
    return {"id": row[0], "title": row[1], "prompt": row[2]}


def parse_model_response(text: str) -> dict:
    """Strip markdown fences if present, then parse JSON."""
    text = text.strip()
    if text.startswith("```"):
        lines = text.splitlines()
        text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
    return json.loads(text)


def call_claude(prompt: str) -> dict:
    import anthropic
    import google.auth
    import google.auth.transport.requests

    credentials, _ = google.auth.load_credentials_from_file(
        SA_KEY_PATH,
        scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
    credentials.refresh(google.auth.transport.requests.Request())

    client = anthropic.AnthropicVertex(
        project_id=GCP_PROJECT,
        region=GCP_REGION,
        access_token=credentials.token,
    )
    message = client.messages.create(
        model="claude-sonnet-4-6@20250514",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )
    return parse_model_response(message.content[0].text)


def call_gemini(prompt: str) -> dict:
    import vertexai
    from vertexai.generative_models import GenerativeModel, GenerationConfig

    vertexai.init(project=GCP_PROJECT, location=GCP_REGION)
    model = GenerativeModel(
        "gemini-2.0-flash-001",
        system_instruction=SYSTEM_PROMPT,
    )
    response = model.generate_content(
        prompt,
        generation_config=GenerationConfig(
            response_mime_type="application/json",
            max_output_tokens=4096,
        ),
    )
    return parse_model_response(response.text)


def call_gpt(prompt: str) -> dict:
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OPENAI_API_KEY not set.")
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        max_tokens=4096,
    )
    return parse_model_response(response.choices[0].message.content)


MODELS = {
    "claude": call_claude,
    "gemini": call_gemini,
    "gpt-4o": call_gpt,
}


def insert_run(problem_id: str, model: str, result: dict):
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
                result.get("solution_code", ""),
                result.get("reasoning", ""),
                result.get("time_complexity", ""),
                result.get("space_complexity", ""),
                None,
                datetime.now(),
            ),
        )
    return run_id


def solve(problem_id: str, models: list[str]):
    problem = get_problem(problem_id)
    print(f"Solving: {problem['title']} ({problem_id})")
    print(f"Models:  {', '.join(models)}\n")

    def run_model(name):
        fn = MODELS[name]
        try:
            result = fn(problem["prompt"])
            run_id = insert_run(problem_id, name, result)
            print(f"  ✅ {name:10s} → {run_id}  [{result.get('time_complexity', '?')}]")
            return name, True
        except Exception as e:
            print(f"  ❌ {name:10s} → FAILED: {e}")
            return name, False

    with ThreadPoolExecutor(max_workers=len(models)) as pool:
        futures = {pool.submit(run_model, m): m for m in models}
        for f in as_completed(futures):
            f.result()  # already printed inside run_model


def main():
    parser = argparse.ArgumentParser(description="solve-bench: Solve a problem with all models")
    parser.add_argument("problem_id", help="ID of the problem to solve (e.g. prob_abc12345)")
    parser.add_argument(
        "--models",
        nargs="+",
        choices=list(MODELS.keys()),
        default=list(MODELS.keys()),
        help="Models to run (default: all three)",
    )
    args = parser.parse_args()
    solve(args.problem_id, args.models)


if __name__ == "__main__":
    main()
