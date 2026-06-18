#!/usr/bin/env python3
"""B5 at scale — does feeding the REAL failure back improve the retry? (robust orchestrator)

Per validated task (tasks.json):
  attempt #1: fixer gets the commit's real description only. Grade (held-out test + full suite).
  if attempt #1 FAILS -> the task enters the retry set (difficulty falls out of the model's own
    outcome, NOT my selection -> avoids the Exp4 confound).
  retry: K samples each of FEEDBACK (failing test NAMES + error TYPE, not assertion values) and
    CONTROL (same prompt as attempt #1, fresh). Recursion works iff feedback pass-rate > control.

Robust: unique temp worktree per run, always cleaned. Held-out grading (fixer never sees the test).
Reward-hack guard: auto-fail if the fix diff touches any test file.
"""
import json, subprocess, tempfile, shutil, os, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE / "semver-src"
VENV = str(HERE / ".venv/bin/python")
K = 3  # samples per arm
TASKS = json.load(open(HERE / "tasks.json"))


def git(*a, cwd=REPO, inp=None):
    return subprocess.run(["git", *a], cwd=cwd, input=inp, capture_output=True, text=True)


def suite(wt):
    p = subprocess.run([VENV, "-m", "pytest", "-q", "-o", "addopts=", "tests/"], cwd=wt,
                       env={**os.environ, "PYTHONPATH": "src"}, capture_output=True, text=True)
    return p.stdout


def grade(wt, testdiff):
    # reward-hack guard: fixer must not have touched tests
    touched = git("diff", "--name-only", cwd=wt).stdout
    if re.search(r"(^|/)test|_test\.py", touched, re.M):
        return "AUTOFAIL_TEST_EDIT", touched
    if not touched.strip():
        return "NOCHANGE", ""
    if git("apply", inp=testdiff, cwd=wt).returncode != 0:
        return "APPLYFAIL", ""
    out = suite(wt)
    last = out.strip().splitlines()[-1] if out.strip() else ""
    passed = ("failed" not in last and "error" not in last.lower())
    return ("PASS" if passed else "FAIL"), out


def fixer(wt, srcfile, prompt):
    subprocess.run(["claude", "-p", prompt, "--model", "sonnet",
                    "--allowedTools", "Read,Edit,Glob,Grep"], cwd=wt,
                   capture_output=True, text=True)


def held_out_symptom(grade_out):
    # failing test NAMES + exception TYPE only (drop assertion detail to stay held-out)
    syms = []
    for line in grade_out.splitlines():
        m = re.search(r"FAILED (\S+)\s*-\s*(\w+Error)", line)
        if m:
            syms.append(f"{m.group(1)} ({m.group(2)})")
    return "; ".join(syms[:6]) or "the regression test still fails"


def run_once(task, prompt):
    """Fresh worktree, fix, grade, cleanup. Returns verdict."""
    tmp = Path(tempfile.mkdtemp(prefix="b5_"))
    wt = tmp / "wt"
    try:
        git("worktree", "add", "-q", "--detach", str(wt), f"{task['commit']}^")
        fixer(wt, task["srcfile"], prompt)
        verdict, out = grade(wt, task["testdiff"])
        return verdict, out
    finally:
        git("worktree", "remove", "--force", str(wt))
        shutil.rmtree(tmp, ignore_errors=True)


def base_prompt(task):
    return (f"A bug report for the 'semver' library. Bug: {task['desc']}\n"
            f"Fix the underlying bug by editing ONLY {task['srcfile']}. Do not edit or create any "
            f"test files; reason from the description and the source.")


def main():
    results = {"attempt1": {}, "retry": {}}
    print(f"=== B5 at scale: {len(TASKS)} tasks, K={K} samples/arm on failures ===")
    for t in TASKS:
        c = t["commit"]
        v1, out1 = run_once(t, base_prompt(t))
        results["attempt1"][c] = v1
        print(f"[{c}] attempt#1: {v1}")
        if v1 == "PASS":
            continue
        sym = held_out_symptom(out1)
        fb_prompt = (f"A bug report for the 'semver' library. Bug: {t['desc']}\n"
                     f"A PREVIOUS fix attempt FAILED — the project's own tests still fail: {sym}\n"
                     f"Use that to locate and fix the real bug, editing ONLY {t['srcfile']}. "
                     f"Do not edit or create test files.")
        fb = [run_once(t, fb_prompt)[0] for _ in range(K)]
        ctl = [run_once(t, base_prompt(t))[0] for _ in range(K)]
        results["retry"][c] = {"feedback": fb, "control": ctl}
        fbp = sum(x == "PASS" for x in fb); ctp = sum(x == "PASS" for x in ctl)
        print(f"[{c}] retry  feedback={fb} ({fbp}/{K} pass)  control={ctl} ({ctp}/{K} pass)")
    json.dump(results, open(HERE / "b5_scale_results.json", "w"), indent=2)
    # aggregate
    fb_all = [x for c in results["retry"] for x in results["retry"][c]["feedback"]]
    ctl_all = [x for c in results["retry"] for x in results["retry"][c]["control"]]
    fbp = sum(x == "PASS" for x in fb_all); ctp = sum(x == "PASS" for x in ctl_all)
    a1 = sum(v == "PASS" for v in results["attempt1"].values())
    print(f"\n=== TALLY ===")
    print(f"attempt#1: {a1}/{len(TASKS)} tasks fixed first try")
    print(f"retry FEEDBACK: {fbp}/{len(fb_all)} pass | CONTROL: {ctp}/{len(ctl_all)} pass")
    print("recursion signal: " + ("FEEDBACK > control" if fbp > ctp else
          "no benefit (feedback <= control)" if fb_all else "no failed tasks to retry"))
    print("written: b5_scale_results.json")


if __name__ == "__main__":
    main()
