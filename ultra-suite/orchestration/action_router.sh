#!/usr/bin/env bash
# action_router.sh — PROTOTYPE of the mechanism that lets a loop cycle invoke a skill,
# a workflow, or an agent fleet (the "teach the loops to run workflows / invoke skills" ask).
#
# HONESTY LABEL (read this): this proves the EASY 20% — the mechanism. Each cycle, one
# headless `claude -p` "router turn" emits a STRUCTURED ACTION, and this script dispatches it.
# The hard 80% — whether the chosen action is the RIGHT one — is NOT solved here. Action
# SELECTION below is ungrounded (the model picks); it becomes real only after the closed-loop
# correctness experiment (ROADMAP.md, brick B2) and the outcome-feedback recalibration (B5).
# Until then this runs in --dry-run by default and executes only safe, additive action types.
#
# Verified capability (probe): a headless `claude -p` toolset includes Skill, Workflow, Agent,
# Bash, Edit. Workflow firing is opt-in-gated, so workflow actions are PLANNED here, not fired,
# unless you pass --allow-workflow and supply the opt-in keyword in the prompt yourself.
#
# Usage:
#   ./action_router.sh --project ./agent                 # dry-run: print the chosen action
#   ./action_router.sh --project ./agent --execute        # execute SAFE action types only
#
# Pair with loop_driver.sh (the bounded outer loop) and state_orchestrator.py (the caps ledger).
# Safety: never runs outside the external caps; escalate-to-human is always a valid action.

set -euo pipefail

PROJECT="$(pwd)"
DRYRUN=1
ALLOW_WORKFLOW=0
MODEL="sonnet"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --project) PROJECT="$2"; shift 2;;
    --execute) DRYRUN=0; shift;;
    --allow-workflow) ALLOW_WORKFLOW=1; shift;;
    --model) MODEL="$2"; shift 2;;
    *) echo "unknown arg: $1" >&2; exit 2;;
  esac
done

STATE="$PROJECT/state"
NOTES="$STATE/SHARED_TASK_NOTES.md"
ARCH="$STATE/MASTER_RECURSIVE_ARCH.md"
[[ -f "$ARCH" ]] || { echo "FATAL: $ARCH missing (generate with recursive-loop-engineer)"; exit 1; }

# 1) ENFORCE CAPS FIRST — the router never proposes an action past the bounds.
if ! python3 "$(dirname "$0")/state_orchestrator.py" --project "$PROJECT" check >/dev/null 2>&1; then
  echo "[router] caps reached — escalating to human, no action chosen."
  exit 2
fi

# 2) ROUTER TURN — model proposes ONE action from a fixed menu, as strict JSON.
#    NOTE: this selection is ungrounded (brick B2/B5 will ground it against realized outcomes).
read -r -d '' ROUTER_PROMPT <<'EOF' || true
Read state/MASTER_RECURSIVE_ARCH.md and state/SHARED_TASK_NOTES.md. Decide the SINGLE best next
action to advance the goal this cycle. Choose from this fixed menu and output ONLY one JSON
object, no prose:

{"action":"primary"}                                  // do one cycle of the primary goal yourself
{"action":"skill","skill":"<name>","prompt":"..."}    // invoke a specific installed skill
{"action":"workflow","name":"<name>","args":{...}}    // run a multi-agent workflow (PLANNED unless allowed)
{"action":"agents","n":<int>,"task":"..."}            // fan out N parallel subagents for independent work
{"action":"escalate","reason":"..."}                  // hand to a human (use when uncertain or at a gate)

Rules: prefer "escalate" whenever the choice is genuinely uncertain or touches a human gate
(skill edits, destructive/irreversible changes, boundary-band opportunities). Keep it minimal.
EOF

RAW="$(cd "$PROJECT" && claude -p "$ROUTER_PROMPT" --model "$MODEL" --output-format json --allowedTools "Read")"
ACTION_JSON="$(python3 -c "import sys,json; print(json.loads(sys.stdin.read()).get('result','').strip())" <<<"$RAW")"
echo "[router] chosen action: $ACTION_JSON"

ACT="$(python3 -c "import sys,json; print(json.loads(sys.argv[1]).get('action','?'))" "$ACTION_JSON" 2>/dev/null || echo '?')"

# 3) DISPATCH. Safe/additive types may execute; consequential types are planned or escalated.
case "$ACT" in
  primary)
    echo "[router] -> hand back to loop_driver.sh for one primary cycle (bounded, with separate reviewer)."
    ;;
  skill)
    SK="$(python3 -c "import sys,json;d=json.loads(sys.argv[1]);print(d.get('skill',''))" "$ACTION_JSON")"
    PR="$(python3 -c "import sys,json;d=json.loads(sys.argv[1]);print(d.get('prompt',''))" "$ACTION_JSON")"
    if [[ "$DRYRUN" -eq 1 ]]; then echo "[router] DRY-RUN would invoke skill '$SK'"; else
      echo "[router] invoking skill '$SK' (read-only-ish; widen --allowedTools deliberately)"
      (cd "$PROJECT" && claude -p "Use the $SK skill. $PR" --model "$MODEL" --allowedTools "Read,Skill,Grep,Glob")
    fi
    ;;
  agents)
    echo "[router] agent-fleet action PLANNED (fan-out runs inside a primary cycle so caps apply): $ACTION_JSON"
    ;;
  workflow)
    if [[ "$ALLOW_WORKFLOW" -eq 1 && "$DRYRUN" -eq 0 ]]; then
      echo "[router] workflow execution requires the opt-in keyword in your driver prompt — not auto-fired here."
    else
      echo "[router] workflow action PLANNED (opt-in gated): $ACTION_JSON"
    fi
    ;;
  escalate)
    REASON="$(python3 -c "import sys,json;print(json.loads(sys.argv[1]).get('reason','(no reason given)'))" "$ACTION_JSON" 2>/dev/null || echo '(unparseable)')"
    python3 "$(dirname "$0")/gate.py" --project "$PROJECT" enqueue \
      --proposal "$REASON" --context "router cycle" --class boundary-band \
      && echo "[router] escalated to human gate (parked; run gate.py review to decide + auto-log)."
    exit 3
    ;;
  *)
    python3 "$(dirname "$0")/gate.py" --project "$PROJECT" enqueue \
      --proposal "unparseable router action: $ACTION_JSON" --context "router cycle" --class other \
      && echo "[router] unknown action -> parked at human gate (fail safe)."
    exit 3
    ;;
esac

echo "[router] cycle done. SELECTION IS UNGROUNDED until ROADMAP.md brick B2 validates the kernel."
