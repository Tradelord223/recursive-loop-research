#!/usr/bin/env python3
"""Mine semver for clean SWE-bench-lite tasks and VALIDATE each:
 - commit touches exactly one source file under src/semver/ AND >=1 test file
 - test-diff applies to parent (regression test added) and then FAILS (bug present)
 - gold src-diff makes the suite GREEN (construction valid)
Writes tasks.json (validated tasks only). Difficulty is NOT curated — we take all that validate.
"""
import json, subprocess, tempfile, shutil, os, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE / "semver-src"
VENV = HERE / ".venv/bin/python"


def git(*a, cwd=REPO):
    return subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True)


def files_in(commit):
    out = git("show", "--stat", "--pretty=", "--name-only", commit).stdout.splitlines()
    return [f for f in out if f.strip()]


def run_suite(wt):
    p = subprocess.run([str(VENV), "-m", "pytest", "-q", "-o", "addopts=", "tests/"],
                       cwd=wt, env={**os.environ, "PYTHONPATH": "src", "PATH": os.environ["PATH"]},
                       capture_output=True, text=True)
    last = p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
    return ("failed" not in last and "error" not in last.lower()), last


def validate(commit):
    fs = files_in(commit)
    srcs = [f for f in fs if f.startswith("src/semver/") and f.endswith(".py")]
    tests = [f for f in fs if ("test" in f) and f.endswith(".py")]
    if len(srcs) != 1 or not tests:
        return None
    srcfile = srcs[0]
    testdiff = git("diff", f"{commit}^", commit, "--", *tests).stdout
    srcdiff = git("diff", f"{commit}^", commit, "--", "src/").stdout
    if not testdiff or not srcdiff:
        return None
    subj = git("log", "-1", "--pretty=%s", commit).stdout.strip()
    desc = re.sub(r"^(Fix|Fixes|Bugfix)[:#\s\d]*", "", subj, flags=re.I).strip() or subj

    tmp = Path(tempfile.mkdtemp(prefix="mine_"))
    wt = tmp / "wt"
    ok = False
    try:
        git("worktree", "add", "-q", "--detach", str(wt), f"{commit}^")
        # apply test diff (regression test present); bug still present -> must FAIL
        if subprocess.run(["git", "apply"], cwd=wt, input=testdiff, text=True,
                          capture_output=True).returncode != 0:
            return None
        green_buggy, _ = run_suite(wt)
        if green_buggy:
            return None  # regression test didn't actually catch the bug -> not a usable task
        # apply gold src fix -> must GREEN
        if subprocess.run(["git", "apply"], cwd=wt, input=srcdiff, text=True,
                          capture_output=True).returncode != 0:
            return None
        green_fixed, _ = run_suite(wt)
        ok = green_fixed
    finally:
        git("worktree", "remove", "--force", str(wt))
        shutil.rmtree(tmp, ignore_errors=True)
    if not ok:
        return None
    return {"commit": commit, "srcfile": srcfile, "desc": desc,
            "testdiff": testdiff, "srcdiff_lines": srcdiff.count("\n")}


def main():
    # candidate commits: "fix" in message, touch src + tests
    cands = git("log", "--oneline", "-i", "--grep=fix", "-n", "120", "--pretty=%h").stdout.split()
    tasks = []
    for c in cands:
        t = validate(c)
        if t:
            tasks.append(t)
            print(f"VALID  {c}  ({t['srcdiff_lines']} src diff lines)  {t['desc'][:60]}")
        if len(tasks) >= 10:
            break
    json.dump(tasks, open(HERE / "tasks.json", "w"), indent=2)
    print(f"\n{len(tasks)} validated tasks -> tasks.json")


if __name__ == "__main__":
    main()
