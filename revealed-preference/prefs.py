#!/usr/bin/env python3
"""
prefs.py — Revealed-Preference Harness.

The one non-circular brick: instead of scoring proposals against a rubric *I* wrote, this
learns to predict the USER's real accept/reject decisions, and measures how well it does
against the user's own held-out decisions. The value signal is external — the user's actual
calls — so it escapes the "I authored the answer key" circularity that ρ=1.0 synthetic
oracles kept smuggling back in (see ../ROADMAP.md, ../experiments/exp5-deceptive/results.md).

WHAT IT DOES NOT DO: it does not, on day one, prove anything. With zero logged decisions there
is nothing to learn. A real result requires the user's real decisions (rule of thumb: >= 20,
and a learning curve needs more). The synthetic smoke test (`--predictor stub` on a toy log)
only verifies the MEASUREMENT MACHINERY, never a judgment claim.

Design notes:
- Two predictors. `stub` = deterministic (predict the majority class of the context); used to
  unit-test the eval math with NO LLM and NO cost. `llm` = the real one: few-shots the user's
  past decisions to a headless `claude -p` and predicts the next. The harness MEASURES the
  predictor; it is not the predictor.
- Two eval modes. `loo` = leave-one-out accuracy (does it predict a held-out decision?).
  `prequential` = process decisions in time order, predict each from ONLY prior ones, and report
  accuracy in successive buckets. The prequential learning curve is the honest B5 test: does
  more of the user's history improve prediction? It has headroom by construction (early
  predictions are uninformed), so it cannot saturate the way the synthetic oracles did.
- Baseline: majority-class accuracy. Beating it = real preference signal learned, not class skew.

Capture: every time the loop's boundary-band human gate pauses and the user decides, log it:
    python3 prefs.py log --proposal "..." --decision accept --reason "..." --context "<goal>"
The safety gate we already built thus doubles as the training-data source.

Std-lib only (+ `claude` CLI for --predictor llm).
"""
import argparse
import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LOG = Path(__file__).resolve().parent / "prefs_log.jsonl"
READY_THRESHOLD = 20  # decisions before loo/accuracy is worth reporting
DECISIONS = ("accept", "reject")


def load(log: Path) -> list[dict]:
    if not log.exists():
        return []
    out = []
    for line in log.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            out.append(json.loads(line))
    return out


def append(log: Path, rec: dict) -> None:
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")


# ---------------- predictors ----------------
def predict_stub(context: list[dict], proposal: str, ctx_label: str) -> tuple[str, float]:
    """Deterministic: predict the majority decision in context. For testing eval math only."""
    if not context:
        return "accept", 0.5
    c = Counter(r["decision"] for r in context)
    top, n = c.most_common(1)[0]
    return top, n / len(context)


def predict_llm(context: list[dict], proposal: str, ctx_label: str,
                model: str = "sonnet") -> tuple[str, float]:
    """Few-shot the user's past decisions; predict their next. The real predictor."""
    shots = []
    for r in context:
        line = f"PROPOSAL: {r['proposal']}\nUSER DECISION: {r['decision']}"
        if r.get("reason"):
            line += f"\nUSER REASON: {r['reason']}"
        shots.append(line)
    examples = "\n\n".join(shots) if shots else "(no prior decisions yet)"
    prompt = (
        "You are predicting how ONE specific user decides which proposals to accept or reject. "
        "Learn their revealed preferences ONLY from their past decisions below — do not impose "
        "your own rubric.\n\n"
        f"=== THIS USER'S PAST DECISIONS ===\n{examples}\n\n"
        f"=== PREDICT THE USER'S DECISION ON ===\n"
        f"{('CONTEXT: ' + ctx_label + chr(10)) if ctx_label else ''}PROPOSAL: {proposal}\n\n"
        "Output ONLY one line: decision=accept|reject,confidence=<0.0-1.0>"
    )
    proc = subprocess.run(
        ["claude", "-p", prompt, "--model", model, "--output-format", "json",
         "--allowedTools", ""],
        capture_output=True, text=True,
    )
    try:
        result = json.loads(proc.stdout).get("result", "")
    except json.JSONDecodeError:
        return "reject", 0.0
    dec, conf = "reject", 0.0
    for tok in result.replace("\n", ",").split(","):
        tok = tok.strip().lower()
        if tok.startswith("decision="):
            v = tok.split("=", 1)[1].strip()
            if v in DECISIONS:
                dec = v
        elif tok.startswith("confidence="):
            try:
                conf = float(tok.split("=", 1)[1])
            except ValueError:
                pass
    return dec, conf


PREDICTORS = {"stub": predict_stub, "llm": predict_llm}


# ---------------- evaluation ----------------
def majority_baseline(recs: list[dict]) -> float:
    c = Counter(r["decision"] for r in recs)
    return c.most_common(1)[0][1] / len(recs) if recs else 0.0


def eval_loo(recs, predictor):
    correct = 0
    for i, r in enumerate(recs):
        ctx = recs[:i] + recs[i + 1:]
        pred, _ = predictor(ctx, r["proposal"], r.get("context", ""))
        correct += (pred == r["decision"])
    return correct / len(recs)


def eval_prequential(recs, predictor, warmup=5, buckets=4):
    recs = sorted(recs, key=lambda r: r.get("ts", ""))
    results = []  # (index, correct?)
    for i in range(warmup, len(recs)):
        pred, _ = predictor(recs[:i], recs[i]["proposal"], recs[i].get("context", ""))
        results.append(pred == recs[i]["decision"])
    overall = sum(results) / len(results) if results else 0.0
    # bucketed learning curve
    curve = []
    if results:
        size = max(1, len(results) // buckets)
        for b in range(0, len(results), size):
            chunk = results[b:b + size]
            curve.append(round(sum(chunk) / len(chunk), 3))
    return overall, curve, len(results)


# ---------------- commands ----------------
def cmd_log(a):
    if a.decision not in DECISIONS:
        sys.exit(f"--decision must be one of {DECISIONS}")
    rec = {
        "id": a.id or f"d{len(load(a.log)) + 1}",
        "ts": a.ts or datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "context": a.context or "",
        "proposal": a.proposal,
        "decision": a.decision,
        "reason": a.reason or "",
        "source": "human",
    }
    append(a.log, rec)
    print(f"[prefs] logged {rec['id']}: {rec['decision']}  (total {len(load(a.log))})")


def cmd_stats(a):
    recs = load(a.log)
    c = Counter(r["decision"] for r in recs)
    print(f"[prefs] decisions logged : {len(recs)}")
    print(f"[prefs] class balance    : {dict(c)}")
    print(f"[prefs] majority baseline: {majority_baseline(recs):.1%}" if recs else "[prefs] majority baseline: n/a")
    ready = len(recs) >= READY_THRESHOLD
    print(f"[prefs] eval readiness   : {'READY' if ready else f'NOT READY (need >= {READY_THRESHOLD}, have {len(recs)})'}")
    if not ready:
        print("[prefs] -> log more REAL decisions before trusting any accuracy number.")


def cmd_predict(a):
    recs = load(a.log)
    pred, conf = PREDICTORS[a.predictor](recs, a.proposal, a.context or "")
    print(f"decision={pred},confidence={conf:.2f}  (from {len(recs)} prior decisions, predictor={a.predictor})")
    if len(recs) < READY_THRESHOLD:
        print(f"[prefs] WARNING: only {len(recs)} prior decisions — prediction is low-confidence by construction.")


def cmd_evaluate(a):
    recs = load(a.log)
    if len(recs) < (a.warmup + 2):
        sys.exit(f"[prefs] need more decisions to evaluate (have {len(recs)}). Log real ones first.")
    base = majority_baseline(recs)
    pf = PREDICTORS[a.predictor]
    if a.mode == "loo":
        acc = eval_loo(recs, pf)
        print(f"[prefs] LOO accuracy (predictor={a.predictor}): {acc:.1%}")
        print(f"[prefs] majority baseline             : {base:.1%}")
        print(f"[prefs] lift over baseline            : {acc - base:+.1%}")
    else:
        acc, curve, n = eval_prequential(recs, pf, warmup=a.warmup)
        print(f"[prefs] prequential accuracy (predictor={a.predictor}, n={n}): {acc:.1%}")
        print(f"[prefs] majority baseline                         : {base:.1%}")
        print(f"[prefs] learning curve (early -> late buckets)     : {curve}")
        print("[prefs] rising curve => more of the user's history improves prediction (the B5 signal).")
    if a.predictor == "stub":
        print("[prefs] NOTE: 'stub' only verifies the eval machinery. Real results need --predictor llm on REAL data.")


def build_parser():
    p = argparse.ArgumentParser(description="Revealed-preference harness: learn & predict the user's real decisions.")
    p.add_argument("--log", type=Path, default=DEFAULT_LOG)
    sub = p.add_subparsers(dest="cmd", required=True)

    lg = sub.add_parser("log", help="record a real human accept/reject decision")
    lg.add_argument("--proposal", required=True)
    lg.add_argument("--decision", required=True, help="accept | reject")
    lg.add_argument("--reason", default="")
    lg.add_argument("--context", default="")
    lg.add_argument("--id", default="")
    lg.add_argument("--ts", default="")
    lg.set_defaults(func=cmd_log)

    st = sub.add_parser("stats", help="log size, class balance, eval readiness")
    st.set_defaults(func=cmd_stats)

    pr = sub.add_parser("predict", help="predict the user's decision on a new proposal")
    pr.add_argument("--proposal", required=True)
    pr.add_argument("--context", default="")
    pr.add_argument("--predictor", choices=PREDICTORS, default="llm")
    pr.set_defaults(func=cmd_predict)

    ev = sub.add_parser("evaluate", help="measure prediction accuracy vs the user's held-out decisions")
    ev.add_argument("--mode", choices=("loo", "prequential"), default="prequential")
    ev.add_argument("--predictor", choices=PREDICTORS, default="llm")
    ev.add_argument("--warmup", type=int, default=5)
    ev.set_defaults(func=cmd_evaluate)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
