#!/usr/bin/env python3
"""Blast-radius oracle for Exp5. Realized value = feature-tests a fix repairs.

Value is set by the call graph (how many features route through a function), NOT by any
per-function test allocation. Names are deliberately anti-correlated with value (deceptive),
so only tracing the code yields the right ranking. Oracle is hidden from rankers.
"""
import json, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
APP, CORRECT, TESTS = ROOT / "app", ROOT / "correct", ROOT / "tests"

# task -> the single file its fix replaces. Names chosen to deceive a label-reader:
#   T2 (_pad2) looks trivial but has reach; T4 (validate_security_token) looks critical but is dead.
TASK_FILE = {
    "T1_money": "money.py",
    "T2_pad": "pad.py",
    "T3_slug": "slug.py",
    "T4_token": "token.py",
    "T5_audit": "audit.py",
    "T6_footer": "footer.py",
}


def failing(repo_app: Path) -> set:
    proc = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", str(TESTS), "-v"],
        cwd=repo_app.parent, env={"PYTHONPATH": str(repo_app.parent), "PATH": "/usr/bin:/bin"},
        capture_output=True, text=True,
    )
    out = set()
    for line in proc.stderr.splitlines():
        if line.strip().endswith(("FAIL", "ERROR")):
            out.add(line.split("(")[1].split(")")[0] if "(" in line else line.split(" ")[0])
    return out


def measure(task, base):
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        shutil.copytree(APP, root / "app")
        shutil.copy(CORRECT / TASK_FILE[task], root / "app" / TASK_FILE[task])
        after = failing(root / "app")
    return len(base - after) - len(after - base)


def main():
    # baseline: copy app to temp so we don't run against a dirtied tree
    with tempfile.TemporaryDirectory() as td:
        root = Path(td); shutil.copytree(APP, root / "app")
        base = failing(root / "app")
    rows = [(t, TASK_FILE[t], measure(t, base)) for t in TASK_FILE]
    rows.sort(key=lambda r: -r[2])
    print(f"baseline failing feature-tests: {len(base)}")
    print(f"{'task':12} {'file':10} blast_radius")
    for t, f, v in rows:
        print(f"{t:12} {f:10} {v}")
    json.dump({t: v for t, f, v in rows}, open(ROOT / "oracle_result.json", "w"), indent=2, sort_keys=True)
    print("\noracle ranking:", " > ".join(t for t, f, v in rows))


if __name__ == "__main__":
    main()
