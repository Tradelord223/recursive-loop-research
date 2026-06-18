#!/usr/bin/env python3
"""Exp8 oracle: run a candidate fix against the HIDDEN corner tests. Outcome ground truth.

A fix is CORRECT iff it passes ALL hidden tests for its function (incl. the subtle corner the
visible tests miss); WRONG otherwise. Crash on any test = wrong. Reviewers never see this.

Usage: python3 oracle.py <Fn> <path-to-fix.py>   # prints "correct" or "wrong N/M"
"""
import importlib.util as iu
import sys
from hidden_tests import HIDDEN

FUNC = {"G1": "compare_versions", "G2": "round_half_even", "G3": "add_one_month",
        "G4": "is_palindrome", "G5": "parse_int", "G6": "chunk"}


def score(fn_key, path):
    spec = iu.spec_from_file_location("fix", path)
    m = iu.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
        f = getattr(m, FUNC[fn_key])
    except Exception as e:
        return 0, len(HIDDEN[fn_key]), f"load/def error: {e}"
    passed = 0
    for label, arg, want in HIDDEN[fn_key]:
        try:
            got = f(*arg) if isinstance(arg, tuple) else f(arg)
            if got == want and type(got) == type(want) or (isinstance(want, (int, float)) and got == want):
                passed += 1
        except Exception:
            pass
    return passed, len(HIDDEN[fn_key]), ""


if __name__ == "__main__":
    p, t, err = score(sys.argv[1], sys.argv[2])
    verdict = "correct" if p == t else f"wrong {p}/{t}"
    print(verdict + (f"  ({err})" if err else ""))
