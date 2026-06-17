#!/usr/bin/env bash
# run_checks.sh — local + CI check runner for recursive-loop-research (item P2.5).
#
# What it does (all deterministic, no spend, no network):
#   1. python3 -m unittest discover -s tests   — the stdlib test suite. The harness uses a
#      stub predictor + synthetic fixtures (tests/test_harness.py docstring); it does NOT
#      shell out to the claude CLI and costs nothing.
#   2. python3 -m py_compile on every orchestration .py file (ultra-suite/orchestration/*.py:
#      currently gate.py, state_orchestrator.py, dashboard.py) plus the prefs module the tests
#      load (revealed-preference/prefs.py). py_compile is purely static — it never executes code.
#   3. bash -n on the two driver scripts (ultra-suite/orchestration/loop_driver.sh and
#      action_router.sh). -n is a syntax-only parse; it never runs the `claude -p` lines.
#
# Deliberately NOT done here (and therefore claude-CLI-free, so this runs unchanged in CI):
#   - Actually executing loop_driver.sh / action_router.sh. A real driver run needs the
#     `claude` CLI (and `jq`) and spends tokens — see those scripts' own honesty labels. This
#     runner only proves the test math and that the orchestration sources parse, not that the
#     loop "works." That boundary is intentional and matches the project's disclosed-limits ethos.
#
# Usage: ./run_checks.sh    (exits 0 only if every check passes)
set -euo pipefail

# Resolve to repo root so relative paths work regardless of caller cwd.
cd "$(dirname "$0")"

echo "== [1/3] python3 -m unittest discover -s tests =="
python3 -m unittest discover -s tests

echo
echo "== [2/3] py_compile orchestration .py files (+ prefs module the tests load) =="
# Glob the orchestration dir so new orchestration modules are covered automatically.
python3 -m py_compile \
  ultra-suite/orchestration/*.py \
  revealed-preference/prefs.py
echo "py_compile OK"

echo
echo "== [3/3] bash -n on the driver scripts (syntax only; claude CLI never invoked) =="
bash -n ultra-suite/orchestration/loop_driver.sh
echo "loop_driver.sh OK"
bash -n ultra-suite/orchestration/action_router.sh
echo "action_router.sh OK"

echo
echo "All checks passed."
