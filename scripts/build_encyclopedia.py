import json
import os
from pathlib import Path
from collections import defaultdict

def extract_data(benchmark_dir):
    data = []

    benchmark_path = Path(benchmark_dir)
    if not benchmark_path.exists():
        print(f"Error: {benchmark_dir} not found.")
        return data

    for problem_dir in benchmark_path.iterdir():
        if problem_dir.is_dir():
            results_file = problem_dir / "results.json"
            solution_file = problem_dir / "solution.py"

            if results_file.exists():
                try:
                    with open(results_file, 'r') as f:
                        results = json.load(f)
                except json.JSONDecodeError:
                    print(f"Error decoding {results_file}")
                    continue

                solution_code = ""
                if solution_file.exists():
                    with open(solution_file, 'r') as f:
                        solution_code = f.read()

                results['solution_code'] = solution_code
                results['dir_name'] = problem_dir.name

                # Standardize some keys to avoid missing keys later
                if 'topic' not in results:
                    results['topic'] = "Unknown"
                if 'title' not in results:
                    results['title'] = results.get('problem_id', problem_dir.name)
                if 'problem_id' not in results:
                    results['problem_id'] = problem_dir.name

                data.append(results)

    return data

def generate_encyclopedia(data, output_dir):
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    problems_dir = out_path / "problems"
    problems_dir.mkdir(parents=True, exist_ok=True)

    # Group data by topic
    topics_data = defaultdict(list)
    for p in data:
        topic = p.get('topic', 'Unknown')
        topics_data[topic].append(p)

    # Sort topics alphabetically
    sorted_topics = sorted(topics_data.keys())

    # 1. Main README.md
    readme_content = "# Data Structures and Algorithms Encyclopedia\n\n"
    readme_content += "This encyclopedia is an interactive learning tool automatically generated from algorithmic coding challenges.\n\n"
    readme_content += "## Topics\n\n"

    for topic in sorted_topics:
        safe_topic_name = topic.replace(" ", "_").replace("/", "_")
        topic_filename = f"{safe_topic_name}.md"
        readme_content += f"- [{topic}]({topic_filename}) ({len(topics_data[topic])} problems)\n"

        # 2. Topic-specific markdown files
        generate_topic_file(topic, topics_data[topic], out_path / topic_filename)

    with open(out_path / "README.md", "w") as f:
        f.write(readme_content)

    # 3. Problem-specific markdown files
    for p in data:
        pid = p.get('problem_id', 'Unknown')
        if pid != 'Unknown':
            generate_problem_file(p, problems_dir / f"{pid}.md")

def generate_topic_file(topic, problems, filepath):
    content = f"# Topic: {topic}\n\n"
    content += "## Problems\n\n"

    # Sort problems by ID
    sorted_problems = sorted(problems, key=lambda x: x.get('problem_id', ''))

    content += "| Problem ID | Title | Time Complexity | Space Complexity |\n"
    content += "|---|---|---|---|\n"

    for p in sorted_problems:
        pid = p.get('problem_id', 'Unknown')
        title = p.get('title', 'Unknown')
        time_c = p.get('empirical_time_complexity', 'Unknown')
        space_c = p.get('empirical_space_complexity', 'Unknown')

        # Link to individual problem file
        prob_link = f"problems/{pid}.md"
        content += f"| [{pid}]({prob_link}) | {title} | `{time_c}` | `{space_c}` |\n"

    with open(filepath, "w") as f:
        f.write(content)

def generate_problem_file(problem, filepath):
    pid = problem.get('problem_id', 'Unknown')
    title = problem.get('title', 'Unknown')
    topic = problem.get('topic', 'Unknown')
    time_c = problem.get('empirical_time_complexity', 'Unknown')
    space_c = problem.get('empirical_space_complexity', 'Unknown')
    notes = problem.get('notes', 'No notes available.')
    solution_code = problem.get('solution_code', '')

    content = f"# {pid}: {title}\n\n"
    content += f"**Topic**: [{topic}](../{topic.replace(' ', '_').replace('/', '_')}.md)\n\n"
    content += f"**Empirical Time Complexity**: `{time_c}`\n\n"
    content += f"**Empirical Space Complexity**: `{space_c}`\n\n"

    content += "## Notes\n\n"
    content += f"{notes}\n\n"

    content += "## Solution\n\n"
    if solution_code:
        content += f"```python\n{solution_code}\n```\n"
    else:
        content += "No solution code available.\n"

    # Benchmarks table
    benchmarks = problem.get('benchmarks', [])
    if benchmarks:
        content += "\n## Benchmarks\n\n"
        content += "| N | Average Time (ms) | Peak Memory (KB) |\n"
        content += "|---|---|---|\n"
        for b in benchmarks:
            n = b.get('n', '')
            avg_t = b.get('avg_time_ms', '')
            peak_m = b.get('peak_memory_kb', '')
            content += f"| {n} | {avg_t} | {peak_m} |\n"

    with open(filepath, "w") as f:
        f.write(content)


if __name__ == "__main__":
    benchmark_dir = "benchmark"
    output_dir = "encyclopedia"

    data = extract_data(benchmark_dir)
    print(f"Extracted data for {len(data)} problems.")

    generate_encyclopedia(data, output_dir)
    print(f"Generated encyclopedia at {output_dir}/")
