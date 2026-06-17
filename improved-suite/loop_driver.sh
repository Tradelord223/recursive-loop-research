#!/usr/bin/env bash
# loop_driver.sh — a REAL bounded driver for the recursive-loop-system.
#
# Why this exists: the suite's original orchestrator (python_state_orchestrator.py)
# does not drive anything — it counts the substring "Cycle" in a markdown file and
# exits. And the README's central claim ("one starter command launches a
# self-sustaining loop indefinitely") is false: Claude Code does not autonomously
# re-prompt itself across context windows. The LOOP must live OUTSIDE the model.
#
# This script is the missing external loop. It is grounded in the real patterns from
# the shipping `autonomous-loops` skill (Continuous-Claude / Sequential-Pipeline) and
# the real Claude Code primitives Addy Osmani / Boris Cherny describe: `claude -p`
# (headless), filesystem state bridges, and HARD external stop conditions.
#
# Each iteration runs TWO separate `claude -p` invocations on purpose:
#   1. PRIMARY  — execute one cycle of the goal + update state files.
#   2. REVIEWER — a FRESH context that did not author the work, gates what may persist.
# This enforces Anthropic's evaluator-optimizer separation and the autonomous-loops
# rule "the reviewer should never be the author." (See EXPERIMENTS_REPORT.md: Exp2 did
# NOT empirically confirm same-context collusion for blatant cases, so this is kept as
# cited defense-in-depth, not as a measured necessity.)
#
# Usage:
#   ./loop_driver.sh --project ./my-agent --max-iters 10 --max-cost 5.00
#
# Requires: claude CLI on PATH, jq. Pair with the `safety-guard` skill in full-auto.

set -euo pipefail

PROJECT="$(pwd)"
MAX_ITERS=10
MAX_COST=5.00          # USD, hard ceiling across the whole run
COMPLETION_SIGNAL="PROJECT_COMPLETE"
COMPLETION_STREAK=2    # consecutive completion signals before stopping
REVIEW=1               # run the separate-context reviewer pass each iteration
MODEL_PRIMARY="sonnet"
MODEL_REVIEW="opus"    # reviewer is the stronger, independent grader

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2;;
    --max-iters) MAX_ITERS="$2"; shift 2;;
    --max-cost) MAX_COST="$2"; shift 2;;
    --no-review) REVIEW=0; shift;;
    --completion-signal) COMPLETION_SIGNAL="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

STATE="$PROJECT/state"
NOTES="$STATE/SHARED_TASK_NOTES.md"     # the cross-iteration context bridge
ARCH="$STATE/MASTER_RECURSIVE_ARCH.md"
mkdir -p "$STATE"
[[ -f "$NOTES" ]] || printf '# SHARED_TASK_NOTES\n\n## Progress\n\n## Next Steps\n' > "$NOTES"

if [[ ! -f "$ARCH" ]]; then
  echo "FATAL: $ARCH not found. Generate it with the RecursiveLoopEngineer skill first." >&2
  exit 1
fi

spent=0.0
streak=0

# run a headless claude turn, return its cost, append cost to the running total.
# $1 = prompt, $2 = model, $3 = allowed tools (optional). echoes the text result.
run_turn() {
  local prompt="$1" model="$2" tools="${3:-}"
  local extra=(); [[ -n "$tools" ]] && extra=(--allowedTools "$tools")
  local out
  out="$(cd "$PROJECT" && claude -p "$prompt" --model "$model" \
        --output-format json "${extra[@]}")"
  local cost; cost="$(jq -r '.total_cost_usd // .cost_usd // 0' <<<"$out")"
  spent="$(awk -v a="$spent" -v b="$cost" 'BEGIN{printf "%.4f", a+b}')"
  jq -r '.result // .text // empty' <<<"$out"
}

over_budget() { awk -v s="$spent" -v m="$MAX_COST" 'BEGIN{exit !(s>m)}'; }

for ((i=1; i<=MAX_ITERS; i++)); do
  echo "──── iteration $i/$MAX_ITERS  (spent \$$spent / \$$MAX_COST) ────"
  if over_budget; then echo "STOP: cost ceiling reached (\$$spent)."; break; fi

  # back up state before any self-modification this cycle (versioning guardrail)
  cp -r "$STATE" "$STATE.bak-$(date +%Y%m%d-%H%M%S)" 2>/dev/null || true

  # 1) PRIMARY cycle — execute goal + update state. Fresh context each iteration.
  primary_out="$(run_turn "Read $ARCH and $NOTES. Execute ONE cycle of the Primary Goal
Loop. Make concrete progress. Run any tests. Append what you did and what is left to
$NOTES (do not rewrite history). If and ONLY if the entire goal is fully complete and
verified, output the exact token ${COMPLETION_SIGNAL} on its own line." \
    "$MODEL_PRIMARY" "Read,Write,Edit,Bash,Grep,Glob")"
  echo "$primary_out" | tail -n 20

  # 2) REVIEWER pass — SEPARATE context, did not author the work above.
  if [[ "$REVIEW" -eq 1 ]]; then
    review_out="$(run_turn "You are an independent reviewer. You did NOT write this
work. Inspect the working tree and the latest entries in $NOTES. Run the build/tests.
Reject (revert or flag in $NOTES) any change that games a metric, skips a test, swallows
a failure, or removes a guardrail. Confirm the goal's verification actually passes
before any completion claim stands." "$MODEL_REVIEW" "Read,Bash,Grep,Glob,Edit")"
    echo "$review_out" | tail -n 10
  fi

  # 3) completion-signal stop (streak prevents premature exit)
  if grep -qF "$COMPLETION_SIGNAL" <<<"$primary_out"; then
    streak=$((streak+1)); echo "completion signal ($streak/$COMPLETION_STREAK)"
    [[ "$streak" -ge "$COMPLETION_STREAK" ]] && { echo "STOP: goal complete."; break; }
  else
    streak=0
  fi
done

echo "──── driver finished: $i iteration(s), \$$spent spent ────"
echo "Human gates (core-skill edits, major new branches) remain in the model's loop;"
echo "this driver enforces only the EXTERNAL caps: iterations, cost, completion."
