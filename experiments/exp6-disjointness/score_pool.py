#!/usr/bin/env python3
"""Score every pool implementation against the HIDDEN oracle. Outcome-based.

oracle_score(impl) = # of 12 hidden tests it passes. This is the measured difficulty
variable; raters never see these tests. A crash on a test counts as a fail.
"""
import importlib.util, json
from pathlib import Path
from hidden_tests import HIDDEN

ROOT = Path(__file__).resolve().parent
POOL = ROOT / "pool"


def load(fp):
    spec = importlib.util.spec_from_file_location(fp.stem, fp)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.roman_to_int


def score(fn):
    passed = 0
    for s, want in HIDDEN:
        try:
            if fn(s) == want:
                passed += 1
        except Exception:
            pass
    return passed


def main():
    rows = {}
    for fp in sorted(POOL.glob("impl_*.py")):
        try:
            fn = load(fp)
            rows[fp.stem] = score(fn)
        except Exception as e:
            rows[fp.stem] = -1  # load error
    for k in sorted(rows, key=lambda k: -rows[k]):
        print(f"{k}: {rows[k]}/12")
    json.dump(rows, open(ROOT / "oracle_scores.json", "w"), indent=2, sort_keys=True)
    vals = sorted(set(v for v in rows.values() if v >= 0))
    print(f"\ndistinct oracle scores present: {vals}")
    print(f"score range: {min(vals)}..{max(vals)} (spread of difficulty for pairing)")


if __name__ == "__main__":
    main()
