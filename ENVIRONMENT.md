# Environment

What you need to read, run the Python pieces, run the tests, and (separately) run an
actual loop. This file is deliberately specific about what is *verified* versus what is
*nominally compatible*, in keeping with the rest of this repo — see [`README.md`](README.md)
and [`EXPERIMENTS_REPORT.md`](EXPERIMENTS_REPORT.md).

## TL;DR

- **No third-party Python packages.** The repo is stdlib-only. See
  [`requirements.txt`](requirements.txt) — it installs nothing on purpose.
- **The only hard external tools are CLIs, not pip packages:** the `claude` CLI and `jq`.
- **Reading the analysis costs nothing.** Re-running an *actual loop* (the shell drivers)
  invokes the `claude` CLI and therefore spends real API money.

## Python

- **Verified interpreter:** `Python 3.14.5` (`python3 --version`, recorded on this machine
  2026-06-17, macOS / Darwin 25.5.0, Homebrew `python3` at `/opt/homebrew/bin/python3`).
- **Realistic floor:** the code uses only long-stable standard-library modules
  (`argparse`, `json`, `os`, `re`, `subprocess`, `sys`, `pathlib`, `unittest`,
  `importlib`, `tempfile`, `shutil`, `datetime`, `collections`). It should run on any
  Python **3.8+**. That floor is reasoned from the imports, **not** tested across versions
  — only 3.14.5 has actually been exercised here, so treat older versions as "expected to
  work," not "verified."
- **No virtualenv required.** Because there are no dependencies, you can run everything
  with the system `python3`. A venv is harmless but buys you nothing.

### Verifying the no-dependency claim yourself

```bash
python3 --version
# Confirms there are no third-party imports anywhere in the tree:
grep -rhoE '^(import|from) [a-zA-Z0-9_]+' --include='*.py' . | sort -u
```

Everything that appears is either a stdlib module or a *local* module in the same
experiment directory (`app`, `textkit`, `hidden_tests`), never an installed package.

## External command-line tools

| Tool | Verified version (this machine) | Needed for | Needed for? |
|------|---------------------------------|------------|-------------|
| `python3` | 3.14.5 | running any `.py`, running the tests | the Python pieces |
| `claude` CLI | 2.1.181 (Claude Code), at `~/.local/bin/claude` | every loop iteration / reviewer turn / router turn | **only** to run an actual loop or rerun a loop-based experiment |
| `jq` | jq-1.7.1 | parsing `claude -p --output-format json` (cost cap + result extraction) in the shell drivers | only to run the shell drivers |

The `claude` + `jq` requirement is declared at the top of the drivers themselves
(`# Requires: claude CLI on PATH, jq`):

- [`improved-suite/loop_driver.sh`](improved-suite/loop_driver.sh)
- [`ultra-suite/orchestration/loop_driver.sh`](ultra-suite/orchestration/loop_driver.sh)
- [`ultra-suite/orchestration/action_router.sh`](ultra-suite/orchestration/action_router.sh)

Those drivers call `claude -p ... --output-format json` and pipe the result through
`jq` to read `total_cost_usd` (the cost cap) and `result` (the turn output). Without
`jq` the cost accounting and output extraction break; without the `claude` CLI there is
no loop at all.

## Running the tests (no API spend, no network)

The test harness is stdlib `unittest`. It uses a **stub predictor and synthetic
fixtures** — it does **not** call the `claude` CLI and does **not** spend money
(see the header of [`tests/test_harness.py`](tests/test_harness.py)).

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

`pytest` will also collect and run it, but pytest is **optional** and is **not** a
dependency of this suite. Do not add it to `requirements.txt`.

## Running an actual loop (this spends real money)

The shell drivers are the only "live" entry points. They require the `claude` CLI and
`jq`, and **each iteration is a real, billed `claude -p` invocation.** Use the built-in
hard caps (`--max-iters`, `--max-cost`) and pair with the `safety-guard` skill in
full-auto, exactly as the driver headers instruct.

```bash
./improved-suite/loop_driver.sh --project ./my-agent --max-iters 10 --max-cost 5.00
```

## Honest scope (so the environment isn't oversold)

This repo's findings are honest about their own limits, and the environment doc should
not undo that:

- The experiments measure **one model's internal self-consistency**, not cross-model or
  human agreement, and not absolute correctness — see the method note in
  [`EXPERIMENTS_REPORT.md`](EXPERIMENTS_REPORT.md). Re-running them with the `claude` CLI
  reproduces *that* ceiling, nothing stronger.
- Two Exp1 conclusions were **retracted** after blinded re-runs (the "0 decision flips"
  and "Total≥28 kills aligned trivia" claims); the load-bearing gate is `Alignment≥8`,
  noisy in the A≈7–8 band, and `Total≥28` is treated as **unsubstantiated**.
- Exp2 was a **NULL** result (a manipulation + floor failure), so the separate-reviewer
  design in the drivers is **cited defense-in-depth, not an empirically validated
  necessity.**

Installing the environment lets you re-run the analysis; it does not upgrade any of those
claims. Details and the full retraction trail are in
[`EXPERIMENTS_REPORT.md`](EXPERIMENTS_REPORT.md).
