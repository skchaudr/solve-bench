---
description: Dispatch Jules benchmark tasks in verified batches of 15
argument-hint: [--dry-run] [--batch-size N] [--delay N]
allowed-tools: [Bash]
---

# Jules Dispatch

Dispatch solve-bench benchmark tasks to Jules in safe, verified batches.

## What this does
1. Checks which problems are already dispatched (reads `jules remote list`)
2. Dispatches remaining problems in batches of 15 with a 2s delay between each
3. After each batch: verifies all tasks actually registered before continuing
4. Reports any dropped tasks explicitly — never claims success without verification

## Arguments
$ARGUMENTS

## Instructions

Run the batched dispatcher from the solve-bench project root:

```bash
cd /home/saboor/work/repos/solve-bench
```

If `--dry-run` is in arguments, run:
```bash
.venv/bin/python dispatch_jules_batched.py --dry-run
```

Otherwise run:
```bash
.venv/bin/python dispatch_jules_batched.py
```

If `--batch-size N` is provided, pass it through.
If `--delay N` is provided, pass it through.

After completion, report:
- How many tasks were dispatched
- How many were confirmed by Jules
- How many were dropped (if any)
- What to do next if there were drops
