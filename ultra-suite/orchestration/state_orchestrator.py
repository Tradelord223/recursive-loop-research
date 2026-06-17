#!/usr/bin/env python3
"""
state_orchestrator.py - a small, REAL bounds helper for the recursive-loop-system.

The primary driver is `loop_driver.sh` (sibling file): it is the external loop that
re-invokes `claude -p` each iteration. Claude Code does NOT re-prompt itself across
context windows, so the loop and its bounds must live outside the model. This helper
does NOT drive the model; it is the durable, on-disk bounds LEDGER for the loop entry
points that are NOT the shipped driver -- the scheduled `/loop`/cron Meta-Improvement
and Discovery runs (see claude-code-commands.md), and any custom driver you write.

Note on `loop_driver.sh`: the shipped driver keeps its OWN inline state backup and its
OWN awk-summed cost ceiling and does not call this helper. This script gives those other
entry points the same backup + cycle/cost bounds against one shared counter, so spend and
cycles are tracked consistently across every entry point rather than only inside the
driver process. Wire it into a custom driver or scheduler by calling `begin-cycle` before
each cycle and `add-cost` after each turn.

What it does (every printed check is actually computed from the counter file or the
filesystem -- there are no decorative guardrails):
  * maintains a JSON counter at state/.loop_counter.json (cycles, cost_usd, caps);
  * enforces max-cycles and max-cost -- on `check`/`begin-cycle` it prints a clear STOP
    and exits nonzero (2) when either cap is met or exceeded;
  * `begin-cycle` makes a dated backup of the entire state/ dir BEFORE the cycle, then
    (if within bounds) increments the cycle counter;
  * `add-cost` accumulates spend so the cost cap is enforced against real numbers;
  * prints the next recommended action based on the last recorded phase.

Std-lib only. Counter shape is intentionally aligned with `loop_driver.sh`
(state dir = <project>/state, backups = <project>/state.bak-YYYYmmdd-HHMMSS,
cost in USD). Cross-reference: opportunity-scoring-rubric.md for the scoring gate,
claude-code-commands.md for how the loops are launched/scheduled.

Examples:
    # one-time init / inspect bounds and next action
    python3 state_orchestrator.py --project ./agent --max-cycles 10 --max-cost 5.00 --status

    # a custom driver or scheduler calls this BEFORE each cycle: backup + bound check +
    # increment. Exits nonzero -> the caller must STOP and not start the cycle.
    python3 state_orchestrator.py --project ./agent begin-cycle || exit 0

    # after a claude -p turn reports its cost, record it (and re-check the cap):
    python3 state_orchestrator.py --project ./agent add-cost 0.42
"""

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

STATE_DIR = "state"
COUNTER_FILE = ".loop_counter.json"
PROGRESS_FILE = "PROGRESS.md"
NOTES_FILE = "SHARED_TASK_NOTES.md"
ARCH_FILE = "MASTER_RECURSIVE_ARCH.md"

EXIT_OK = 0
EXIT_STOP = 2  # a bound was hit; caller (driver) must not start a new cycle


def state_path(project: Path) -> Path:
    return project / STATE_DIR


def counter_path(project: Path) -> Path:
    return state_path(project) / COUNTER_FILE


def load_counter(project: Path) -> dict:
    p = counter_path(project)
    if p.exists():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            sys.stderr.write(f"[orchestrator] corrupt counter {p}: {exc}\n")
            sys.exit(1)
    else:
        data = {}
    # fill defaults without clobbering existing values
    data.setdefault("cycles", 0)
    data.setdefault("cost_usd", 0.0)
    data.setdefault("max_cycles", None)
    data.setdefault("max_cost_usd", None)
    data.setdefault("last_phase", "init")
    data.setdefault("created", datetime.now().isoformat(timespec="seconds"))
    return data


def save_counter(project: Path, data: dict) -> None:
    sp = state_path(project)
    sp.mkdir(parents=True, exist_ok=True)
    data["updated"] = datetime.now().isoformat(timespec="seconds")
    counter_path(project).write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


def apply_caps(data: dict, args) -> None:
    """Persist caps when supplied on the CLI; CLI overrides stored values."""
    if args.max_cycles is not None:
        data["max_cycles"] = args.max_cycles
    if args.max_cost is not None:
        data["max_cost_usd"] = args.max_cost


def evaluate_bounds(data: dict):
    """Return (stop: bool, reasons: list[str]) computed from real counters.

    `stop` means a cap is met/exceeded and NO new cycle may start.
    """
    reasons = []
    stop = False
    mc = data.get("max_cycles")
    if mc is not None and data["cycles"] >= mc:
        stop = True
        reasons.append(f"max-cycles reached: {data['cycles']}/{mc}")
    cap = data.get("max_cost_usd")
    if cap is not None and data["cost_usd"] >= cap:
        stop = True
        reasons.append(f"cost ceiling reached: ${data['cost_usd']:.4f}/${cap:.2f}")
    return stop, reasons


def print_bounds(data: dict) -> None:
    mc = data.get("max_cycles")
    cap = data.get("max_cost_usd")
    mc_s = "unbounded" if mc is None else str(mc)
    cap_s = "unbounded" if cap is None else f"${cap:.2f}"
    print(f"[orchestrator] cycles : {data['cycles']}/{mc_s}")
    print(f"[orchestrator] cost   : ${data['cost_usd']:.4f}/{cap_s}")
    print(f"[orchestrator] phase  : {data['last_phase']}")


def next_action(project: Path, data: dict, stop: bool, reasons) -> str:
    """Compute a recommendation from real filesystem + counter state."""
    sp = state_path(project)
    if not (sp / ARCH_FILE).exists():
        return (f"Generate {STATE_DIR}/{ARCH_FILE} with the RecursiveLoopEngineer skill "
                f"before running loop_driver.sh.")
    if stop:
        return ("STOP. " + "; ".join(reasons) +
                ". Hand to a human: raise caps deliberately, or close out the run.")
    phase = data["last_phase"]
    # Meta-Improvement / Discovery cadence hint (see claude-code-commands.md section 2).
    if data["cycles"] > 0 and data["cycles"] % 3 == 0 and phase != "meta":
        return ("Run a Meta-Improvement / Opportunity Discovery pass "
                "(see claude-code-commands.md section 2); score new work against "
                "opportunity-scoring-rubric.md before queueing.")
    return ("Run the next Primary cycle via loop_driver.sh "
            "(it reads SHARED_TASK_NOTES.md + PROGRESS.md and continues).")


def backup_state(project: Path) -> Path | None:
    """Dated backup of the whole state/ dir, matching loop_driver.sh's convention.

    The counter file itself is excluded from the copy so backups don't nest counters.
    """
    sp = state_path(project)
    if not sp.is_dir():
        return None
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    dest = project / f"{STATE_DIR}.bak-{stamp}"
    # disambiguate if two cycles land in the same second
    suffix = 1
    while dest.exists():
        dest = project / f"{STATE_DIR}.bak-{stamp}.{suffix}"
        suffix += 1
    shutil.copytree(sp, dest, ignore=shutil.ignore_patterns(COUNTER_FILE))
    return dest


# --- commands ---------------------------------------------------------------

def cmd_status(project: Path, args) -> int:
    data = load_counter(project)
    apply_caps(data, args)
    save_counter(project, data)
    stop, reasons = evaluate_bounds(data)
    print_bounds(data)
    if reasons:
        for r in reasons:
            print(f"[orchestrator] STOP: {r}")
    print(f"[orchestrator] next : {next_action(project, data, stop, reasons)}")
    return EXIT_STOP if stop else EXIT_OK


def cmd_check(project: Path, args) -> int:
    """Bound check only; no mutation of cycle/cost. Exits nonzero if a cap is hit."""
    data = load_counter(project)
    apply_caps(data, args)
    save_counter(project, data)
    stop, reasons = evaluate_bounds(data)
    if stop:
        for r in reasons:
            print(f"[orchestrator] STOP: {r}")
        return EXIT_STOP
    print_bounds(data)
    return EXIT_OK


def cmd_begin_cycle(project: Path, args) -> int:
    """Pre-cycle gate: enforce caps, back up state, then increment the cycle counter.

    On STOP, exits nonzero WITHOUT backing up or incrementing -- the cycle must not run.
    """
    data = load_counter(project)
    apply_caps(data, args)
    stop, reasons = evaluate_bounds(data)
    if stop:
        save_counter(project, data)
        for r in reasons:
            print(f"[orchestrator] STOP: {r}")
        print("[orchestrator] not starting cycle.")
        return EXIT_STOP

    dest = backup_state(project)
    if dest is not None:
        print(f"[orchestrator] backup: {dest}")
    else:
        print(f"[orchestrator] no {STATE_DIR}/ dir yet to back up; continuing.")

    data["cycles"] += 1
    data["last_phase"] = args.phase
    save_counter(project, data)
    print(f"[orchestrator] begin cycle {data['cycles']} (phase={data['last_phase']})")
    print_bounds(data)
    return EXIT_OK


def cmd_add_cost(project: Path, args) -> int:
    """Accumulate spend, then re-check the cost cap against the real running total."""
    try:
        amount = float(args.amount)
    except ValueError:
        sys.stderr.write(f"[orchestrator] not a number: {args.amount!r}\n")
        return 1
    if amount < 0:
        sys.stderr.write("[orchestrator] cost must be >= 0\n")
        return 1
    data = load_counter(project)
    apply_caps(data, args)
    data["cost_usd"] = round(data["cost_usd"] + amount, 6)
    save_counter(project, data)
    print(f"[orchestrator] +${amount:.4f} -> total ${data['cost_usd']:.4f}")
    stop, reasons = evaluate_bounds(data)
    if stop:
        for r in reasons:
            print(f"[orchestrator] STOP: {r}")
        return EXIT_STOP
    return EXIT_OK


def cmd_set_phase(project: Path, args) -> int:
    data = load_counter(project)
    apply_caps(data, args)
    data["last_phase"] = args.phase
    save_counter(project, data)
    print(f"[orchestrator] phase -> {data['last_phase']}")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Bounds helper for the recursive-loop-system. "
                    "Primary driver is loop_driver.sh.")
    p.add_argument("--project", type=Path, default=Path.cwd(),
                   help="project root containing state/ (default: cwd)")
    p.add_argument("--max-cycles", type=int, default=None,
                   help="hard cap on cycles; persisted to the counter when given")
    p.add_argument("--max-cost", type=float, default=None,
                   help="hard USD cost ceiling; persisted to the counter when given")
    p.add_argument("--status", action="store_true",
                   help="print bounds + next recommended action (default action)")

    sub = p.add_subparsers(dest="command")
    sub.add_parser("status", help="print bounds + next recommended action")
    sub.add_parser("check", help="bound check only; nonzero exit if a cap is hit")
    bc = sub.add_parser("begin-cycle",
                        help="enforce caps, back up state/, increment cycle")
    bc.add_argument("--phase", default="primary",
                    help="phase label for this cycle (e.g. primary, meta, discovery)")
    ac = sub.add_parser("add-cost", help="accumulate USD spend and re-check the cap")
    ac.add_argument("amount", help="USD amount to add (e.g. 0.42)")
    sp = sub.add_parser("set-phase", help="record the current phase label")
    sp.add_argument("phase", help="phase label (e.g. primary, meta, discovery)")
    return p


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    project = args.project.resolve()

    dispatch = {
        "status": cmd_status,
        "check": cmd_check,
        "begin-cycle": cmd_begin_cycle,
        "add-cost": cmd_add_cost,
        "set-phase": cmd_set_phase,
        None: cmd_status,  # no subcommand -> status (honors --status too)
    }
    return dispatch[args.command](project, args)


if __name__ == "__main__":
    sys.exit(main())
