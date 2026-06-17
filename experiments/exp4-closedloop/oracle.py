#!/usr/bin/env python3
"""Deterministic realized-value oracle for Exp4.

For each candidate task, apply ONLY that task's fix (copy the correct version of the one
file over the buggy repo, in an isolated temp copy), run the unittest suite, and measure
realized value = (tests that go failing->passing) - (tests that go passing->failing).

The oracle is computed from test outcomes the rankers never see. This is the unfakeable
ground truth the whole experiment turns on.
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT / "repo"
CORRECT = ROOT / "correct"
TESTS = ROOT / "tests"

# task -> the single file its fix replaces
TASK_FILE = {
    "T1": "parse.py",
    "T2": "slug.py",
    "T3": "truncate.py",
    "T4": "normalize.py",
    "T5": "wordcount.py",   # task = add docstring; correct == buggy -> 0 delta
    "T6": "titlecase.py",   # task = rename internal var; correct == buggy -> 0 delta
}


def run_tests(repo_dir: Path) -> set[str]:
    """Return the set of FAILING test ids (failures + errors)."""
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(TESTS), "-v"],
        cwd=repo_dir, env={"PYTHONPATH": str(repo_dir), "PATH": "/usr/bin:/bin"},
        capture_output=True, text=True,
    )
    failing = set()
    for line in proc.stderr.splitlines():
        # unittest -v emits e.g. "test_basic (test_textkit.TestParseKV.test_basic) ... FAIL"
        if line.strip().endswith(("FAIL", "ERROR")):
            tid = line.split("(")[1].split(")")[0] if "(" in line else line.split(" ")[0]
            failing.add(tid)
    return failing


def measure(task: str, baseline_fail: set[str]) -> dict:
    with tempfile.TemporaryDirectory() as td:
        tmp_repo = Path(td) / "repo"
        shutil.copytree(REPO, tmp_repo)
        # apply only this task's fix
        shutil.copy(CORRECT / TASK_FILE[task], tmp_repo / "textkit" / TASK_FILE[task])
        after_fail = run_tests(tmp_repo)
    fixed = baseline_fail - after_fail          # failing -> passing
    regressed = after_fail - baseline_fail      # passing -> failing
    return {
        "task": task,
        "file": TASK_FILE[task],
        "fixed": len(fixed),
        "regressed": len(regressed),
        "realized_value": len(fixed) - len(regressed),
    }


def main():
    baseline_fail = run_tests(REPO)
    rows = [measure(t, baseline_fail) for t in TASK_FILE]
    rows.sort(key=lambda r: -r["realized_value"])
    print(f"baseline failing tests: {len(baseline_fail)}")
    print(f"{'task':5} {'file':14} {'fixed':6} {'regr':5} {'realized_value':14}")
    for r in rows:
        print(f"{r['task']:5} {r['file']:14} {r['fixed']:<6} {r['regressed']:<5} {r['realized_value']:<14}")
    oracle = {r["task"]: r["realized_value"] for r in rows}
    (ROOT / "oracle_result.json").write_text(json.dumps(oracle, indent=2, sort_keys=True) + "\n")
    print("\noracle ranking (by realized value):", " > ".join(r["task"] for r in rows))
    print("written: oracle_result.json")


if __name__ == "__main__":
    main()
