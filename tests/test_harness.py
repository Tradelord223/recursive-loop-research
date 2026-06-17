#!/usr/bin/env python3
"""P2.1 (agent-accepted) — deterministic tests for the harness eval math + gate state machine.

Stub predictor + synthetic fixtures only: no claude CLI, no spend. Validates prefs.py's
eval_loo / eval_prequential / majority_baseline and gate.py's enqueue->resolve roundtrip.
Runs under stdlib unittest (the suite is stdlib-only) and under pytest.

This file exists to OUTCOME-VALIDATE the autonomous loop's decision to accept P2.1: if these
pass and genuinely exercise the math, the agent's judgment is confirmed by an unfakeable signal
(test pass/fail), not by self-agreement.
"""
import importlib.util as iu
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PREFS = ROOT / "revealed-preference" / "prefs.py"
GATE = ROOT / "ultra-suite" / "orchestration" / "gate.py"


def _load(path, name):
    spec = iu.spec_from_file_location(name, path)
    m = iu.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


prefs = _load(PREFS, "prefs")


def rec(i, decision):
    return {"id": f"d{i}", "ts": f"2026-06-17T10:{i:02d}:00+00:00", "context": "t",
            "proposal": f"p{i}", "decision": decision, "reason": "", "source": "synthetic"}


class TestMajorityBaseline(unittest.TestCase):
    def test_all_accept(self):
        self.assertEqual(prefs.majority_baseline([rec(i, "accept") for i in range(5)]), 1.0)

    def test_seven_three(self):
        recs = [rec(i, "accept") for i in range(7)] + [rec(i, "reject") for i in range(7, 10)]
        self.assertAlmostEqual(prefs.majority_baseline(recs), 0.7)

    def test_empty(self):
        self.assertEqual(prefs.majority_baseline([]), 0.0)


class TestEvalLOO(unittest.TestCase):
    def test_stub_matches_majority_on_skewed(self):
        # stub predicts context-majority; on a 7/3 split LOO accuracy should equal the
        # majority baseline (it predicts 'accept' for held-out, correct 7/10).
        recs = [rec(i, "accept") for i in range(7)] + [rec(i, "reject") for i in range(7, 10)]
        acc = prefs.eval_loo(recs, prefs.predict_stub)
        self.assertAlmostEqual(acc, 0.7)

    def test_unanimous_is_perfect(self):
        recs = [rec(i, "accept") for i in range(6)]
        self.assertEqual(prefs.eval_loo(recs, prefs.predict_stub), 1.0)


class TestEvalPrequential(unittest.TestCase):
    def test_returns_curve_and_count(self):
        recs = [rec(i, "accept") for i in range(6)] + [rec(i, "reject") for i in range(6, 12)]
        acc, curve, n = prefs.eval_prequential(recs, prefs.predict_stub, warmup=2, buckets=4)
        self.assertEqual(n, len(recs) - 2)            # predicts every post-warmup item
        self.assertTrue(0.0 <= acc <= 1.0)
        self.assertGreaterEqual(len(curve), 1)
        self.assertTrue(all(0.0 <= b <= 1.0 for b in curve))

    def test_all_same_class_perfect_after_warmup(self):
        recs = [rec(i, "accept") for i in range(10)]
        acc, curve, n = prefs.eval_prequential(recs, prefs.predict_stub, warmup=2)
        self.assertEqual(acc, 1.0)


class TestGateStateMachine(unittest.TestCase):
    def test_enqueue_then_pending_roundtrip(self):
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td)
            (proj / "state").mkdir()
            r = subprocess.run([sys.executable, str(GATE), "--project", str(proj),
                                "enqueue", "--proposal", "add a test", "--context", "x",
                                "--class", "boundary-band"],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            q = proj / "state" / "GATE_QUEUE.jsonl"
            self.assertTrue(q.exists())
            recs = [json.loads(x) for x in q.read_text().splitlines() if x.strip()]
            self.assertEqual(len(recs), 1)
            self.assertEqual(recs[0]["status"], "pending")
            self.assertEqual(recs[0]["class"], "boundary-band")
            # pending lists it
            p = subprocess.run([sys.executable, str(GATE), "--project", str(proj), "pending"],
                               capture_output=True, text=True)
            self.assertIn("1 pending", p.stdout)

    def test_unknown_class_rejected(self):
        # P2.3: unknown --class is REJECTED (nonzero exit, nothing enqueued), not coerced.
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td); (proj / "state").mkdir()
            r = subprocess.run([sys.executable, str(GATE), "--project", str(proj), "enqueue",
                                "--proposal", "p", "--class", "bogus-class"],
                               capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)
            self.assertFalse((proj/"state"/"GATE_QUEUE.jsonl").exists())

    def test_empty_proposal_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td); (proj / "state").mkdir()
            r = subprocess.run([sys.executable, str(GATE), "--project", str(proj), "enqueue",
                                "--proposal", "   ", "--class", "other"],
                               capture_output=True, text=True)
            self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
