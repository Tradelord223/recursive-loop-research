#!/usr/bin/env python3
"""
dashboard.py — a glanceable, read-only status board for a recursive-loop project.

Reads the durable state a running loop leaves behind and prints one compact summary:

  * cycles + cost      from state/.loop_counter.json   (written by state_orchestrator.py)
  * gate items         pending  -> state/GATE_QUEUE.jsonl
                       resolved -> state/GATE_RESOLVED.jsonl
  * decision sources   agent    -> state/AGENT_DECISIONS.jsonl
                       human    -> revealed-preference/prefs_log.jsonl
  * accept / reject     tallied across every decision log it can find

It is deliberately MODEST: it only reports what is on disk. It does not run the loop,
does not score opportunities, and does not judge whether a project is "healthy" — it
mirrors files so a human can see state at a glance before deciding anything. Every
source file is optional; a missing file is reported as absent, never invented.

This is the read-only sibling of:
  * orchestration/state_orchestrator.py  — owns/writes .loop_counter.json + enforces caps
  * orchestration/gate.py                — enqueues/resolves GATE_QUEUE/RESOLVED + logs to prefs
  * revealed-preference/prefs.py         — the human revealed-preference harness (prefs_log.jsonl)

Std-lib only. Python 3.8+.

Usage:
  python3 dashboard.py --project /path/to/project
  python3 dashboard.py --project . --json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Source locations, relative to the project root. These mirror the layout the
# rest of the suite writes to; see the module docstring for the owning tool.
# ---------------------------------------------------------------------------
COUNTER_REL = Path("state") / ".loop_counter.json"
GATE_QUEUE_REL = Path("state") / "GATE_QUEUE.jsonl"
GATE_RESOLVED_REL = Path("state") / "GATE_RESOLVED.jsonl"
AGENT_DECISIONS_REL = Path("state") / "AGENT_DECISIONS.jsonl"
PREFS_LOG_REL = Path("revealed-preference") / "prefs_log.jsonl"


# ---------------------------------------------------------------------------
# Tolerant readers. Anything missing or malformed degrades to "absent / 0 valid
# records" rather than raising — a status board must never crash on a half-
# written log, and it must never overstate what it actually read.
# ---------------------------------------------------------------------------
def read_json(path: Path):
    """Return parsed dict from a JSON file, or None if absent/unreadable."""
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, NotADirectoryError, IsADirectoryError, OSError):
        return None
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None


def read_jsonl(path: Path):
    """
    Return (records, skipped) for a JSONL file.

    `records` is the list of successfully-parsed objects; `skipped` counts blank
    or malformed lines so the board can disclose data it could not read rather
    than silently dropping it. A missing file yields ([], 0).
    """
    records = []
    skipped = 0
    try:
        text = path.read_text(encoding="utf-8")
    except (FileNotFoundError, NotADirectoryError, IsADirectoryError, OSError):
        return records, skipped
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except (json.JSONDecodeError, ValueError):
            skipped += 1
            continue
        if isinstance(obj, dict):
            records.append(obj)
        else:
            skipped += 1
    return records, skipped


def tally_decisions(records):
    """
    Count accept / reject / other across a list of decision records.

    Looks at the common `decision` field used by gate.py, prefs.py and the
    agent-decision log. Unknown or absent values are bucketed as "other" so the
    totals always add up to len(records) — no quiet discards.
    """
    accept = reject = other = 0
    for r in records:
        d = str(r.get("decision", "")).strip().lower()
        if d == "accept":
            accept += 1
        elif d == "reject":
            reject += 1
        else:
            other += 1
    return {"accept": accept, "reject": reject, "other": other}


# ---------------------------------------------------------------------------
# Collection: read every source once into a plain dict the renderers consume.
# ---------------------------------------------------------------------------
def collect(project: Path) -> dict:
    counter_path = project / COUNTER_REL
    counter = read_json(counter_path)

    pending, pending_skipped = read_jsonl(project / GATE_QUEUE_REL)
    resolved, resolved_skipped = read_jsonl(project / GATE_RESOLVED_REL)
    agent, agent_skipped = read_jsonl(project / AGENT_DECISIONS_REL)
    human, human_skipped = read_jsonl(project / PREFS_LOG_REL)

    return {
        "project": str(project),
        "loop_counter": {
            "present": counter is not None,
            "path": str(COUNTER_REL),
            "cycles": (counter.get("cycles") if isinstance(counter, dict) else None),
            "cost_usd": (counter.get("cost_usd") if isinstance(counter, dict) else None),
            "max_cycles": (counter.get("max_cycles") if isinstance(counter, dict) else None),
            "max_cost_usd": (counter.get("max_cost_usd") if isinstance(counter, dict) else None),
        },
        "gate": {
            "pending": len(pending),
            "pending_skipped": pending_skipped,
            "resolved": len(resolved),
            "resolved_skipped": resolved_skipped,
            "resolved_tally": tally_decisions(resolved),
        },
        "agent": {
            "count": len(agent),
            "skipped": agent_skipped,
            "tally": tally_decisions(agent),
        },
        "human": {
            "count": len(human),
            "skipped": human_skipped,
            "tally": tally_decisions(human),
        },
    }


# ---------------------------------------------------------------------------
# Rendering.
# ---------------------------------------------------------------------------
def _fmt_cap(value) -> str:
    return "no cap" if value is None else str(value)


def _fmt_cost_cap(value) -> str:
    if value is None:
        return "no cap"
    try:
        return f"${float(value):.2f}"
    except (TypeError, ValueError):
        return str(value)


def render_text(data: dict) -> str:
    out = []
    out.append("=" * 60)
    out.append("recursive-loop status board")
    out.append(f"project: {data['project']}")
    out.append("=" * 60)

    # --- cycles + cost ---
    lc = data["loop_counter"]
    out.append("")
    out.append("LOOP COUNTER  (state/.loop_counter.json)")
    if not lc["present"]:
        out.append("  absent — no cycles run yet, or this project does not use the counter.")
    else:
        cycles = lc["cycles"] if lc["cycles"] is not None else 0
        out.append(f"  cycles : {cycles} / {_fmt_cap(lc['max_cycles'])}")
        cost = lc["cost_usd"]
        if cost is None:
            cost_str = "0.0000"
        else:
            try:
                cost_str = f"{float(cost):.4f}"
            except (TypeError, ValueError):
                cost_str = str(cost)
        out.append(f"  cost   : ${cost_str} / {_fmt_cost_cap(lc['max_cost_usd'])}")

    # --- gate items ---
    g = data["gate"]
    out.append("")
    out.append("GATE QUEUE")
    out.append(f"  pending  : {g['pending']:>4}   (state/GATE_QUEUE.jsonl)")
    out.append(f"  resolved : {g['resolved']:>4}   (state/GATE_RESOLVED.jsonl)")
    rt = g["resolved_tally"]
    out.append(f"             accept {rt['accept']}  reject {rt['reject']}  other {rt['other']}")
    if g["pending_skipped"] or g["resolved_skipped"]:
        out.append(
            f"  [unreadable lines skipped: queue={g['pending_skipped']} "
            f"resolved={g['resolved_skipped']}]"
        )

    # --- decision sources ---
    a = data["agent"]
    h = data["human"]
    out.append("")
    out.append("DECISIONS BY SOURCE")
    out.append(f"  agent : {a['count']:>4}   (state/AGENT_DECISIONS.jsonl)")
    out.append(
        f"          accept {a['tally']['accept']}  "
        f"reject {a['tally']['reject']}  other {a['tally']['other']}"
    )
    out.append(f"  human : {h['count']:>4}   (revealed-preference/prefs_log.jsonl)")
    out.append(
        f"          accept {h['tally']['accept']}  "
        f"reject {h['tally']['reject']}  other {h['tally']['other']}"
    )
    if a["skipped"] or h["skipped"]:
        out.append(
            f"  [unreadable lines skipped: agent={a['skipped']} human={h['skipped']}]"
        )

    # --- combined accept/reject across every decision log ---
    total_accept = (
        a["tally"]["accept"] + h["tally"]["accept"] + g["resolved_tally"]["accept"]
    )
    total_reject = (
        a["tally"]["reject"] + h["tally"]["reject"] + g["resolved_tally"]["reject"]
    )
    out.append("")
    out.append("ACCEPT / REJECT  (agent + human + resolved gate, combined)")
    out.append(f"  accept : {total_accept}")
    out.append(f"  reject : {total_reject}")

    out.append("")
    out.append("read-only mirror of files on disk; nothing was run or modified.")
    out.append("=" * 60)
    return "\n".join(out)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Glanceable, read-only status board for a recursive-loop project."
    )
    parser.add_argument(
        "--project",
        default=".",
        help="path to the project root (the directory containing state/). default: current dir",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit the collected status as JSON instead of the text board",
    )
    args = parser.parse_args(argv)

    project = Path(args.project).expanduser()
    if not project.exists():
        print(f"[dashboard] project path does not exist: {project}", file=sys.stderr)
        return 1
    if not project.is_dir():
        print(f"[dashboard] project path is not a directory: {project}", file=sys.stderr)
        return 1

    data = collect(project)

    if args.json:
        print(json.dumps(data, indent=2, sort_keys=True))
    else:
        print(render_text(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
