#!/usr/bin/env python3
"""
gate.py — the human gate, wired to the revealed-preference harness.

Closes the loop the whole project has been building toward: the safety gate (where the loop
pauses for a human on boundary-band opportunities and any destructive/irreversible/skill-edit/
gate-change proposal) is ALSO the training-data source. Every decision a human makes here is
auto-logged to prefs.py, so using the system safely == teaching it your judgment.

Two modes, matching how autonomous loops really run:
  * enqueue  — NON-blocking. A headless loop (loop_driver.sh / action_router.sh escalate) calls
               this when it hits a gate. The proposal is parked; the loop stops or proceeds with
               safe actions. No human needs to be present.
  * review   — interactive. When a human IS present, walk the pending queue: show each proposal,
               (optionally) show the predictor's suggested verdict + confidence, read the human's
               accept/reject/defer + reason, AUTO-LOG accept/reject to prefs.py, and resolve it.

Capture is fail-safe: every resolved decision is written to GATE_RESOLVED.jsonl regardless of
whether prefs.py could be found, so a human decision is never lost.

Std-lib only. prefs.py is located via --prefs, else $PREFS_PY, else a short search; if not found,
prefs logging is skipped (with a warning) but the decision is still captured.
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

VALID_CLASSES = ("boundary-band", "destructive", "irreversible", "skill-edit", "gate-change", "other")


def queue_path(project: Path) -> Path:
    return project / "state" / "GATE_QUEUE.jsonl"


def resolved_path(project: Path) -> Path:
    return project / "state" / "GATE_RESOLVED.jsonl"


def load_jsonl(p: Path) -> list[dict]:
    if not p.exists():
        return []
    return [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]


def write_jsonl(p: Path, recs: list[dict]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in recs), encoding="utf-8")


def append_jsonl(p: Path, rec: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, sort_keys=True) + "\n")


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def resolve_prefs(arg: str | None, project: Path) -> Path | None:
    if arg:
        return Path(arg) if Path(arg).exists() else None
    env = os.environ.get("PREFS_PY")
    if env and Path(env).exists():
        return Path(env)
    for cand in (project / "prefs.py", project / "revealed-preference" / "prefs.py",
                 project.parent / "revealed-preference" / "prefs.py"):
        if cand.exists():
            return cand
    return None


def prefs_call(prefs: Path | None, args: list[str]) -> tuple[bool, str]:
    if prefs is None:
        return False, "prefs.py not found"
    proc = subprocess.run([sys.executable, str(prefs), *args], capture_output=True, text=True)
    return proc.returncode == 0, (proc.stdout + proc.stderr).strip()


# ---------------- commands ----------------
def cmd_enqueue(a):
    rec = {
        "id": a.id or f"g{len(load_jsonl(queue_path(a.project))) + 1}",
        "ts": now(),
        "proposal": a.proposal,
        "context": a.context or "",
        "class": a.cls if a.cls in VALID_CLASSES else "other",
        "status": "pending",
    }
    append_jsonl(queue_path(a.project), rec)
    print(f"[gate] enqueued {rec['id']} ({rec['class']}) — awaiting human review. "
          f"({len(load_jsonl(queue_path(a.project)))} pending)")


def cmd_pending(a):
    recs = [r for r in load_jsonl(queue_path(a.project)) if r.get("status") == "pending"]
    print(f"[gate] {len(recs)} pending:")
    for r in recs:
        print(f"  {r['id']} [{r['class']}] {r['proposal'][:80]}")


def cmd_review(a):
    project = a.project
    prefs = resolve_prefs(a.prefs, project)
    if prefs is None:
        print("[gate] WARNING: prefs.py not found — decisions will be captured to "
              "GATE_RESOLVED.jsonl but NOT logged for learning. Pass --prefs <path> to fix.")
    q = load_jsonl(queue_path(project))
    pending = [r for r in q if r.get("status") == "pending"]
    if not pending:
        print("[gate] no pending items.")
        return
    remaining = [r for r in q if r.get("status") != "pending"]
    for r in pending:
        print("\n" + "=" * 70)
        print(f"GATE {r['id']}  [{r['class']}]   context: {r['context']}")
        print(f"PROPOSAL: {r['proposal']}")
        pref_pre = (["--log", a.prefs_log] if a.prefs_log else [])
        if a.suggest and prefs is not None:
            ok, out = prefs_call(prefs, [*pref_pre, "predict", "--proposal", r["proposal"],
                                         "--context", r["context"]])
            print(f"  predictor suggests: {out.splitlines()[0] if ok and out else '(unavailable)'}")
        ans = input("  decide [a]ccept / [r]eject / [d]efer / [s]kip: ").strip().lower()
        if ans in ("s", "skip", ""):
            r["status"] = "pending"; remaining.append(r); continue
        if ans in ("d", "defer"):
            r["status"] = "deferred"; r["resolved_ts"] = now(); remaining.append(r)
            append_jsonl(resolved_path(project), r); continue
        decision = "accept" if ans in ("a", "accept") else "reject"
        reason = input("  reason (optional): ").strip()
        r["status"] = "resolved"; r["decision"] = decision
        r["reason"] = reason; r["resolved_ts"] = now()
        append_jsonl(resolved_path(project), r)            # fail-safe capture, always
        ok, out = prefs_call(prefs, [*pref_pre, "log", "--proposal", r["proposal"],
                                     "--decision", decision, "--reason", reason,
                                     "--context", r["context"]])
        print(f"  -> {decision}; " + (f"logged to prefs ({out.splitlines()[-1] if out else 'ok'})"
                                       if ok else "prefs logging SKIPPED (captured to GATE_RESOLVED.jsonl)"))
    write_jsonl(queue_path(project), remaining)
    print("\n[gate] review complete.")


def build_parser():
    p = argparse.ArgumentParser(description="Human gate wired to the revealed-preference harness.")
    p.add_argument("--project", type=Path, default=Path.cwd())
    sub = p.add_subparsers(dest="cmd", required=True)

    eq = sub.add_parser("enqueue", help="park a proposal for human review (non-blocking)")
    eq.add_argument("--proposal", required=True)
    eq.add_argument("--context", default="")
    eq.add_argument("--class", dest="cls", default="other", help=f"one of {VALID_CLASSES}")
    eq.add_argument("--id", default="")
    eq.set_defaults(func=cmd_enqueue)

    pd = sub.add_parser("pending", help="list pending gate items")
    pd.set_defaults(func=cmd_pending)

    rv = sub.add_parser("review", help="interactively decide pending items; auto-logs to prefs.py")
    rv.add_argument("--prefs", default="", help="path to prefs.py (else $PREFS_PY / search)")
    rv.add_argument("--prefs-log", dest="prefs_log", default="", help="prefs log file to write decisions to")
    rv.add_argument("--suggest", action="store_true", help="show predictor's suggested verdict first")
    rv.set_defaults(func=cmd_review)
    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)
