# solve-bench

## Summary
The `solve-bench` repository is a Python 3 benchmarking framework designed to systematically evaluate Large Language Models (LLMs) on algorithmic programming problems. It prompts models to generate solutions, and executes those solutions across large, scaled synthetic datasets. It uses `timeit` and `tracemalloc` to strictly verify theoretical and empirical time and space complexities.

## Core Tech Stack
*   **Language:** Python 3
*   **Database:** DuckDB (a local, SQLite-like analytical database) used for storing problem metadata, model execution runs, and annotations.
*   **CLI & Output Formatting:** `Rich` library for rendering terminal tables, progress bars, and formatted outputs.
*   **Testing & Benchmarking:** `pytest` for functional correctness testing, and standard library `timeit` & `tracemalloc` for deep execution profiling.

## Current State
The project is actively functional and has generated a substantial corpus of benchmark runs. It successfully manages problem ingestion and currently tracks 71 benchmarks stored in the `benchmark/` folder. A comprehensive report in `reports/benchmark_audit.md` indicates that 60 of these benchmarks are clean, while 11 are flagged for review. Essential pipeline elements like ingestion (`ingest.py`), model execution (`solve.py`), and analysis (`review.py`) are all fully implemented.

## Main Unsolved Problems
*   **Flagged Benchmarks:** There are 11 benchmarks flagged in the audit requiring resolution, primarily due to `complexity_label_mismatch` (where empirical measurements deviate significantly from expected theoretical scale), `extrapolated_100k` (timeouts leading to missed empirical runs at N=100,000), and `missing_metadata`.
*   **Scaling Infeasibility on High Complexities:** A persistent framework limitation is profiling O(N^2), exponential, or factorial algorithms up to input sizes of `N=100_000`, causing timeouts or out-of-memory errors. The current mitigation mapping down needs more rigorous stabilization and mathematical extrapolation handling.
*   **Incomplete Problems:** There are ongoing `TODO` tasks for providing clean Python baseline solutions and deriving `pytest` test cases from raw problem descriptions for multiple unstructured algorithms.
