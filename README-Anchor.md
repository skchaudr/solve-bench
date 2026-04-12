# solve-bench

## Summary
`solve-bench` is a benchmarking framework designed to evaluate how well various AI models solve medium-to-hard algorithmic problems. It stores problem descriptions and AI-generated solutions in a local DuckDB database, then uses dynamically generated harnesses to rigorously test the empirical time and space complexity of the code across massive input scales. By comparing self-reported theoretical complexities with empirical runtime data, it provides deep insights into the practical coding capabilities of large language models.

## Core Tech Stack
- **Language:** Python 3
- **Database:** DuckDB (for storing problems, runs, and annotations locally in `solve-bench.db`)
- **CLI/UI:** Rich (for beautiful terminal formatting, progress bars, and tables)
- **Benchmarking:** Standard libraries `timeit` and `tracemalloc`
- **LLM Integrations:** Google Vertex AI (Gemini), Anthropic (Claude), OpenAI SDKs (GPT-4o)

## Current State
The project has a fully operational data pipeline and an initialized local DuckDB schema. Numerous benchmark suites have been successfully populated within the `benchmark/` directory, complete with generated test cases and baseline empirical results. The core execution layer features active scripts for dispatching batch inference tasks (`dispatch_*.py`), generating solutions across different models (`solve.py`), analyzing code complexity statically (`analyze.py`), and executing side-by-side performance comparisons (`compare.py`).

## Main Unsolved Problems
- **Secure Execution Environment:** Currently, AI-generated Python code is executed directly on the host machine without secure sandboxing, posing serious security and stability risks if a model hallucinated malicious or destructive code.
- **API Rate Limits and Quotas:** The system frequently encounters strict provider rate limits and quota caps, necessitating complex workarounds like batching, task packing (`dispatch_packed.py`), and explicit sleep timers that slow down evaluation loops.
- **Complexity Analysis Reliability:** While `analyze.py` uses an LLM to perform static complexity analysis, there is an ongoing challenge in bridging the gap between an LLM's self-reported "theoretical" complexity and the true "empirical" measurements derived by the benchmarking harnesses.
- **Automated Test Validation Validation:** Full automation of tracking whether a model's run successfully passes its associated pytest test cases is incomplete; currently, human annotations are often required via `review.py` to manually record verdicts.