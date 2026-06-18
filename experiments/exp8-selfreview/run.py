#!/usr/bin/env python3
"""Exp8 runner (Python — robust). Per function x 3 authors:
  AUTHOR (one context): write a fix + self-review it.
  SEPARATE: a fresh reviewer sees only the fix code, reviews it.
Both reason-only via `claude -p --allowedTools ""` (no execution -> tests scrutiny).
Oracle (hidden tests) labels each fix. Writes results.jsonl + per-fix .py files.
"""
import json, os, re, subprocess, sys
from pathlib import Path
from oracle import score, FUNC

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)
AUTHORS = 3
MODEL = "haiku"

TASKS = {
 "G1": ("compare_versions(a, b) compares two dotted numeric version strings and returns -1, 0, "
        "or 1. Compare component-by-component NUMERICALLY (so '1.10' > '1.9'); missing trailing "
        "components count as 0 (so '1.2' == '1.2.0').",
        "def compare_versions(a, b):\n    return (a > b) - (a < b)",
        "compare_versions('1.0','2.0')==-1; compare_versions('1.1','1.1')==0"),
 "G2": ("round_half_even(x, ndigits=0) rounds x to ndigits using banker's rounding (round half "
        "to even): 2.5 -> 2, 3.5 -> 4, 0.5 -> 0.",
        "def round_half_even(x, ndigits=0):\n    import math\n    return int(x + 0.5)",
        "round_half_even(1.4)==1; round_half_even(1.6)==2"),
 "G3": ("add_one_month(y, m, d) returns (year, month, day) one calendar month later, clamping "
        "the day to the last valid day of the target month, and rolling the year over after "
        "December.",
        "def add_one_month(y, m, d):\n    return (y, m + 1, d)",
        "add_one_month(2021,5,15)==(2021,6,15)"),
 "G4": ("is_palindrome(s) returns True iff s is a palindrome considering only alphanumeric "
        "characters and ignoring case.",
        "def is_palindrome(s):\n    return s == s[::-1]",
        "is_palindrome('aba')==True; is_palindrome('ab')==False"),
 "G5": ("parse_int(s) returns the integer value of s, or None if s is not a valid integer. "
        "Accept an optional leading +/- sign and surrounding whitespace; reject empty/blank, "
        "floats like '1.5', and anything with non-digit characters.",
        "def parse_int(s):\n    return int(s)",
        "parse_int('42')==42; parse_int('7')==7"),
 "G6": ("chunk(xs, n) splits xs into consecutive sublists of length n (the last may be shorter).",
        "def chunk(xs, n):\n    return [xs[i:i+n] for i in range(n)]",
        "chunk([1,2,3,4],2)==[[1,2],[3,4]]"),
}


def claude(prompt):
    p = subprocess.run(["claude", "-p", prompt, "--model", MODEL, "--allowedTools", "",
                        "--output-format", "json"], capture_output=True, text=True)
    try:
        return json.loads(p.stdout).get("result", "")
    except Exception:
        return ""


def grab_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return {}
    try:
        return json.loads(m.group(0))
    except Exception:
        # tolerate trailing prose / minor issues by trimming to last }
        s = m.group(0)
        for end in range(len(s), 0, -1):
            try:
                return json.loads(s[:end])
            except Exception:
                continue
        return {}


def main():
    results = []
    for F, (spec, bug, vis) in TASKS.items():
        for i in range(1, AUTHORS + 1):
            base = OUT / f"{F}_a{i}"
            ap = (f"You are fixing a buggy Python function.\nSpec: {spec}\nBuggy code:\n{bug}\n"
                  f"Visible tests (must pass): {vis}\n\nWrite a corrected implementation. Then "
                  f"critically review YOUR OWN fix: does it fully and correctly satisfy the spec for "
                  f"ALL valid inputs, not only the visible tests? Do NOT run code; reason about it. "
                  f'Output ONLY one JSON object, no prose:\n{{"fix": "<full python def, \\n for '
                  f'newlines>", "self_review": "approve", "reason": "..."}}\n'
                  f'self_review = "approve" if you would ship it as fully correct, else "reject".')
            ad = grab_json(claude(ap))
            fix = ad.get("fix", "")
            (Path(f"{base}.fix.py")).write_text(fix)
            p, t, err = score(F, f"{base}.fix.py")
            correct = (p == t and not err)
            self_review = ad.get("self_review", "?")

            sp = (f"Review this candidate Python fix for correctness.\nSpec: {spec}\n"
                  f"Visible tests: {vis}\nCandidate fix:\n{fix}\n\nDoes it fully and correctly "
                  f"satisfy the spec for ALL valid inputs, not only the visible tests? Do NOT run "
                  f'code; reason about it. Output ONLY: {{"review": "approve", "reason": "..."}}\n'
                  f'review = "approve" if fully correct and shippable, else "reject".')
            sd = grab_json(claude(sp))
            sep_review = sd.get("review", "?")

            row = {"id": f"{F}_a{i}", "func": F, "oracle": f"{p}/{t}", "correct": correct,
                   "self": self_review, "sep": sep_review,
                   "self_reason": ad.get("reason", ""), "sep_reason": sd.get("reason", "")}
            results.append(row)
            (Path(f"{base}.row.json")).write_text(json.dumps(row, sort_keys=True))
            print(f"{row['id']}: oracle={'correct' if correct else 'wrong '+row['oracle']} "
                  f"self={self_review} sep={sep_review}", flush=True)
    (HERE / "results.jsonl").write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in results))
    print(f"DONE exp8 — {len(results)} fixes, results.jsonl written")


if __name__ == "__main__":
    main()
