#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from statistics import median

EXPECTED_SCALES = [100, 1000, 10000, 100000]
DEFAULT_BENCH_ROOT = Path("benchmark")
DEFAULT_REPORT_PATH = Path("reports/benchmark_audit.md")


@dataclass
class BenchmarkAudit:
    problem_id: str
    path: Path
    title: str
    topic: str
    time_complexity: str
    space_complexity: str
    notes: str
    benchmarks: list[dict]
    flags: list[str] = field(default_factory=list)
    details: list[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return not self.flags

    @property
    def avg_time_100k(self) -> float | None:
        for bench in self.benchmarks:
            if bench.get("n") == 100000:
                return _safe_float(bench.get("avg_time_ms"))
        return None


def _safe_float(value) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def normalize_label(label: str) -> str:
    return re.sub(r"\s+", "", (label or "")).upper()


def expected_ratio(label: str, prev_n: int, curr_n: int) -> float | None:
    norm = normalize_label(label)
    if not norm:
        return None

    factor = curr_n / prev_n
    log_ratio = math.log(curr_n) / math.log(prev_n)

    if norm in {"O(1)", "O(CONSTANT)"}:
        return 1.0
    if any(token in norm for token in ["4^N", "2^N", "!", "FACTORIAL"]):
        return None
    if any(token in norm for token in ["N^3", "V^3"]):
        return factor**3
    if any(token in norm for token in ["N^2", "V^2"]) and "LOG" not in norm:
        return factor**2
    if "V^2LOGV" in norm or "N^2LOGN" in norm:
        return (factor**2) * log_ratio
    if any(token in norm for token in ["NLOG", "LOG(SUM", "ELOGV"]):
        return factor * log_ratio
    if any(token in norm for token in ["V+E", "E+V", "N*L", "N)", "O(N", "O(V"]):
        return factor
    return None


def load_results(results_path: Path) -> dict:
    with results_path.open() as fh:
        return json.load(fh)


def detect_missing_metadata(results: dict) -> tuple[list[str], list[str]]:
    flags: list[str] = []
    details: list[str] = []

    missing = []
    for key in ["title", "topic", "notes", "empirical_time_complexity", "empirical_space_complexity"]:
        value = results.get(key)
        if value in (None, ""):
            missing.append(key)

    if missing:
        flags.append("missing_metadata")
        details.append("missing_metadata: " + ", ".join(missing))

    return flags, details


def detect_scale_flags(benchmarks: list[dict]) -> tuple[list[str], list[str]]:
    flags: list[str] = []
    details: list[str] = []

    scales = [bench.get("n") for bench in benchmarks]
    if scales != EXPECTED_SCALES:
        flags.append("missing_scale")
        details.append(f"missing_scale: found {scales}, expected {EXPECTED_SCALES}")

    return flags, details


def detect_extrapolation(notes: str, bench_py_text: str) -> tuple[list[str], list[str]]:
    flags: list[str] = []
    details: list[str] = []

    haystacks = [notes.lower(), bench_py_text.lower()]
    patterns = [
        "extrapolat",
        "skip n=100000",
        "skip n = 100000",
        "mapped n values",
        "mapped down to",
        "map the large n values",
        "too slow",
        "astronomical amount of time",
    ]
    matches = [pattern for pattern in patterns if any(pattern in text for text in haystacks)]
    if matches:
        flags.append("extrapolated_100k")
        details.append("extrapolated_100k: " + ", ".join(sorted(set(matches))))

    return flags, details


def detect_ratio_flags(time_complexity: str, benchmarks: list[dict], skip_mismatch: bool) -> tuple[list[str], list[str]]:
    flags: list[str] = []
    details: list[str] = []

    ratios: list[tuple[int, int, float, float]] = []
    deviations: list[float] = []

    for prev, curr in zip(benchmarks, benchmarks[1:]):
        prev_n = prev.get("n")
        curr_n = curr.get("n")
        prev_ms = _safe_float(prev.get("avg_time_ms"))
        curr_ms = _safe_float(curr.get("avg_time_ms"))
        if not all([prev_n, curr_n, prev_ms, curr_ms]) or prev_ms <= 0:
            continue

        expected = expected_ratio(time_complexity, int(prev_n), int(curr_n))
        actual = curr_ms / prev_ms
        if expected is None or expected <= 0:
            continue

        ratios.append((int(prev_n), int(curr_n), actual, expected))
        if actual > expected * 20:
            flags.append("timing_jump_gt_20x_expected")
            details.append(
                f"timing_jump_gt_20x_expected: {prev_n}->{curr_n} actual={actual:.2f}x expected={expected:.2f}x"
            )

        # Small scales are often dominated by interpreter and setup noise.
        # Use the larger-scale steps for label trustworthiness.
        if int(prev_n) >= 1000:
            deviations.append(abs(math.log10(actual / expected)))

    if not skip_mismatch and deviations and median(deviations) > 0.40:
        worst = max(ratios, key=lambda item: abs(math.log10(item[2] / item[3])))
        flags.append("complexity_label_mismatch")
        details.append(
            "complexity_label_mismatch: "
            f"median log10 deviation={median(deviations):.2f}; worst step {worst[0]}->{worst[1]} "
            f"actual={worst[2]:.2f}x expected={worst[3]:.2f}x for {time_complexity}"
        )

    return flags, details


def audit_one(problem_dir: Path) -> BenchmarkAudit:
    results_path = problem_dir / "results.json"
    bench_path = problem_dir / "bench.py"
    results = load_results(results_path)
    bench_py_text = bench_path.read_text() if bench_path.exists() else ""

    audit = BenchmarkAudit(
        problem_id=results.get("problem_id", problem_dir.name),
        path=problem_dir,
        title=results.get("title", ""),
        topic=results.get("topic", ""),
        time_complexity=results.get("empirical_time_complexity", ""),
        space_complexity=results.get("empirical_space_complexity", ""),
        notes=results.get("notes", ""),
        benchmarks=results.get("benchmarks", []),
    )

    for detector in (
        detect_missing_metadata,
        lambda r: detect_scale_flags(audit.benchmarks),
    ):
        detector_flags, detector_details = detector(results)
        audit.flags.extend(detector_flags)
        audit.details.extend(detector_details)

    extrapolation_flags, extrapolation_details = detect_extrapolation(audit.notes, bench_py_text)
    audit.flags.extend(extrapolation_flags)
    audit.details.extend(extrapolation_details)

    ratio_flags, ratio_details = detect_ratio_flags(
        audit.time_complexity,
        audit.benchmarks,
        skip_mismatch="extrapolated_100k" in audit.flags,
    )
    audit.flags.extend(ratio_flags)
    audit.details.extend(ratio_details)

    audit.flags = sorted(set(audit.flags))
    audit.details = list(dict.fromkeys(audit.details))
    return audit


def choose_recommended(clean_audits: list[BenchmarkAudit]) -> dict[str, list[BenchmarkAudit]]:
    by_topic: dict[str, list[BenchmarkAudit]] = defaultdict(list)
    for audit in clean_audits:
        by_topic[audit.topic].append(audit)

    recommendations: dict[str, list[BenchmarkAudit]] = {}
    for topic, audits in by_topic.items():
        ordered = sorted(
            audits,
            key=lambda audit: (
                audit.avg_time_100k is None,
                audit.avg_time_100k if audit.avg_time_100k is not None else float("inf"),
                audit.problem_id,
            ),
        )
        recommendations[topic] = ordered[:2]
    return dict(sorted(recommendations.items()))


def render_report(audits: list[BenchmarkAudit]) -> str:
    total = len(audits)
    clean = [audit for audit in audits if audit.is_clean]
    flagged = [audit for audit in audits if not audit.is_clean]

    flag_counts = Counter(flag for audit in flagged for flag in audit.flags)
    topic_counts = Counter(audit.topic or "UNKNOWN" for audit in audits)
    clean_topic_counts = Counter(audit.topic or "UNKNOWN" for audit in clean)
    recommendations = choose_recommended(clean)

    lines: list[str] = []
    lines.append("# Benchmark Audit")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Total benchmark folders: {total}")
    lines.append(f"- Clean benchmarks: {len(clean)}")
    lines.append(f"- Flagged benchmarks: {len(flagged)}")
    lines.append("")
    lines.append("## Topics")
    lines.append("")
    for topic, count in sorted(topic_counts.items()):
        lines.append(f"- {topic}: {count} total, {clean_topic_counts.get(topic, 0)} clean")
    lines.append("")
    lines.append("## Flag Counts")
    lines.append("")
    for flag, count in sorted(flag_counts.items()):
        lines.append(f"- `{flag}`: {count}")
    if not flag_counts:
        lines.append("- None")
    lines.append("")
    lines.append("## Recommended Validation Sample")
    lines.append("")
    for topic in sorted(topic_counts):
        picks = recommendations.get(topic, [])
        if not picks:
            lines.append(f"- {topic}: no clean benchmarks available")
            continue
        summary = ", ".join(
            f"`{pick.problem_id}` ({pick.title or 'missing title'}, 100k={pick.avg_time_100k:.2f}ms)"
            for pick in picks
            if pick.avg_time_100k is not None
        )
        lines.append(f"- {topic}: {summary}")
    lines.append("")
    lines.append("## Flagged Benchmarks")
    lines.append("")
    if not flagged:
        lines.append("- None")
    else:
        for audit in sorted(flagged, key=lambda item: (item.topic or "UNKNOWN", item.problem_id)):
            title = audit.title or "missing title"
            topic = audit.topic or "UNKNOWN"
            reasons = ", ".join(f"`{flag}`" for flag in audit.flags)
            lines.append(f"- `{audit.problem_id}` | {title} | {topic} | {reasons}")
            for detail in audit.details:
                lines.append(f"  - {detail}")
    lines.append("")
    lines.append("## Clean Benchmarks")
    lines.append("")
    if not clean:
        lines.append("- None")
    else:
        for audit in sorted(clean, key=lambda item: (item.topic or "UNKNOWN", item.problem_id)):
            title = audit.title or "missing title"
            topic = audit.topic or "UNKNOWN"
            time_100k = f"{audit.avg_time_100k:.2f}ms" if audit.avg_time_100k is not None else "n/a"
            lines.append(f"- `{audit.problem_id}` | {title} | {topic} | 100k={time_100k}")

    lines.append("")
    lines.append("## Notes")
    lines.append("")
    lines.append("- `complexity_label_mismatch` is based on the 1k->10k and 10k->100k timing ratios versus the declared empirical time complexity.")
    lines.append("- `timing_jump_gt_20x_expected` is intentionally conservative and only triggers on extreme blow-ups.")
    lines.append("- `extrapolated_100k` is flagged when `bench.py` or `results.json` notes indicate the 100k result was skipped, mapped, or extrapolated rather than directly measured.")

    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit benchmark folders and generate a markdown report.")
    parser.add_argument("--bench-root", type=Path, default=DEFAULT_BENCH_ROOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_REPORT_PATH)
    args = parser.parse_args()

    problem_dirs = sorted(path for path in args.bench_root.iterdir() if path.is_dir())
    audits = [audit_one(problem_dir) for problem_dir in problem_dirs]

    report = render_report(audits)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report)

    clean_count = sum(audit.is_clean for audit in audits)
    flagged_count = len(audits) - clean_count
    print(f"Wrote {args.output} ({clean_count} clean, {flagged_count} flagged)")


if __name__ == "__main__":
    main()
