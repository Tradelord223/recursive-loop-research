# Claude Code Commands & Patterns for the Recursive Loop System

How to actually run the three-loop system (Primary Execution + Meta-Improvement +
Opportunity Discovery) using **real** Claude Code primitives. There is no magic starter
prompt that loops forever. **The loop lives outside the model.** Claude Code runs one
turn-loop per invocation and stops; an external driver re-invokes it. This document shows
the real launch, scheduling, hook, worktree, safety, and cost paths, plus how to resume.

Primary driver: `loop_driver.sh` (sibling file, do not duplicate its logic here).
Bounds helper: `state_orchestrator.py` (sibling file).
Scoring contract: `opportunity-scoring-rubric.md`.
Defer to the shipping `autonomous-loops`, `safety-guard`, and `cost-aware-llm-pipeline`
skills — do not reinvent what they provide.

---

## 0. Prerequisites & Project Setup

```bash
mkdir my-recursive-agent && cd my-recursive-agent
mkdir -p state
# Copy the state templates from ../state-templates/ into state/ and customize.
# Generate the spec with the RecursiveLoopEngineer skill (writes the file below):
#   state/MASTER_RECURSIVE_ARCH.md
```

Required on PATH: the `claude` CLI and `jq`. `loop_driver.sh` aborts if
`state/MASTER_RECURSIVE_ARCH.md` is missing — generate it first.

State files the loops read/write (templates in `../state-templates/`):
`MASTER_RECURSIVE_ARCH.md`, `SHARED_TASK_NOTES.md` (the cross-iteration context bridge),
`PROGRESS.md`, `MISTAKE_LEARNING_LOG.md`, `IMPROVEMENT_PROPOSALS.md`,
`OPPORTUNITIES_QUEUE.md`, `SKILL_EVOLUTION_LOG.md`, `ALIGNMENT_CHECK.md`.

---

## 1. Launch the Primary Execution Loop (the real driver)

`loop_driver.sh` is the external loop. It re-invokes `claude -p` (headless) once per
iteration with a fresh context, bridges state across iterations via
`SHARED_TASK_NOTES.md`, and enforces **hard external bounds** that no model "willpower"
can override.

```bash
./loop_driver.sh --project ./my-recursive-agent --max-iters 10 --max-cost 5.00
```

- `--max-iters N` — hard cap on iterations.
- `--max-cost USD` — hard cost ceiling summed across the whole run from each turn's
  reported `total_cost_usd`. The driver stops the moment the running total exceeds it.
- `--completion-signal TOKEN` — the exact token the Primary turn must emit (default
  `PROJECT_COMPLETE`) to count toward the completion streak; the driver stops only after
  the streak repeats, which prevents a premature single-turn exit.
- `--no-review` — disable the separate-context reviewer pass (NOT recommended; see §3).

Set conservative bounds first (`--max-iters 3 --max-cost 1.00`) and watch one full run
before widening them.

Add the fourth external bound — **max duration** — by wrapping the driver in `timeout`,
since the driver itself does not cap wall-clock time:

```bash
timeout 3600 ./loop_driver.sh --project ./my-recursive-agent --max-iters 10 --max-cost 5.00
```

These four bounds — iterations, cost, max duration, and the completion streak — are the
only things keeping the system bounded, and all four live outside the model: iterations,
cost, and completion in `loop_driver.sh`; duration in the `timeout` wrapper (or the
cron/`/schedule` window for scheduled runs). They are external by design.

---

## 2. Schedule periodic Meta-Improvement / Discovery

The Primary loop runs the goal. Meta-Improvement and Opportunity Discovery are best run
on their own cadence, not jammed into every Primary turn. Pick one trigger:

- **`/loop <interval>`** — recurring in-session run, e.g.
  `/loop 30m Run one Meta-Improvement cycle: read MISTAKE_LEARNING_LOG.md and the latest
  trace, append concrete proposals to IMPROVEMENT_PROPOSALS.md. Apply ONLY additive,
  reversible changes; route everything else to a human (see §4).`
- **`ScheduleWakeup`** — schedule a single future Discovery/Meta turn from inside a
  session when the work is bursty rather than fixed-cadence.
- **A cron routine via `/schedule`** — for unattended, machine-level cadence (e.g. a
  daily Discovery pass). This is the **Event-Driven Loop** layer (LangChain 4-layer
  model) that the original suite omitted; it is what makes the system periodic without a
  human re-prompting it.

Map of loops to drivers:

| Loop | Real driver |
|------|-------------|
| Primary Execution | `loop_driver.sh` (`claude -p` chain) |
| Meta-Improvement (Hill-Climbing) | `/loop <interval>`, `ScheduleWakeup`, or cron routine |
| Opportunity Discovery (Event-Driven) | cron routine / `ScheduleWakeup`; scores via `opportunity-scoring-rubric.md` |
| Verification | the reviewer pass in `loop_driver.sh` (separate `claude -p`, §3) |

Keep Discovery on a leash: cap it to 2–3 candidates per run and gate scoring per §5.

---

## 3. Evaluator-optimizer separation (the reviewer is never the author)

`loop_driver.sh` runs two `claude -p` invocations per iteration on purpose: a PRIMARY
turn that does the work, then a REVIEWER turn in a **fresh context that did not author
that work**. This is Anthropic's evaluator-optimizer pattern (one LLM generates, a
separate one evaluates) and the `autonomous-loops` rule "the reviewer should never be the
author."

Honesty note: keep this as **cited defense-in-depth**. Our own experiment (Exp2,
`../EXPERIMENTS_REPORT.md`) did NOT find same-context collusion on blatant reward-hacks —
a same-context reviewer rejected them about as well as an independent one. So separation
is principled and cheap, **not empirically proven necessary**. Do not claim otherwise.

To get separation outside the driver (e.g. inside one interactive session), use a
subagent (Task tool) for the review, or a distinct `claude -p` call — never have the
author grade its own output in the same context.

---

## 4. Wire hooks for cycle-boundary tests / state writes

Run deterministic code at cycle boundaries with Claude Code **hooks** (settings.json),
so verification and bookkeeping do not depend on the model remembering to do them:

- **Stop hook** — at the end of a turn, run the project's tests and append the result to
  `PROGRESS.md`. A nonzero exit surfaces the failure to the next iteration.
- **PreToolUse hook** — before destructive tools (e.g. `Bash` running `rm`, `git push`,
  deploys), invoke the `safety-guard` skill's check and block/escalate. Do not write a
  bespoke destructive-action guard; defer to `safety-guard`.

Hooks are the mechanism behind the driver's "run tests every cycle" expectation; the
driver does not silently assume tests ran.

---

## 5. Opportunity scoring & the auto-apply boundary (hard rules)

Discovery proposes follow-on work and scores it with `opportunity-scoring-rubric.md`.
Enforce these exactly:

- **`Alignment >= 8` is the load-bearing gate** and does essentially all the
  adjudication. Reject below it.
- The `Total >= 28` cutoff is a **heuristic, not a validated/calibrated threshold**.
  Treat it as a soft prioritizer, never as proof an item is worth doing.
- **Boundary band → human gate, not auto-spawn:** any item scoring Alignment 7–8 OR
  Total 26–30 goes to a human. That band is where scoring is a coin-flip.
- **Separate authoring from scoring:** the agent that wrote an opportunity's description
  must NOT score it (raters are swayed by wording — a self-gaming vector, since Discovery
  both writes and scores). Score from a neutral one-line spec, or have a second agent
  re-describe it first.

Auto-apply is restricted to **additive + reversible** changes only — new tests, new
files, pinned dependencies, new lint hooks. Anything that deletes or weakens a test,
lowers a gate, edits a skill, or removes/bypasses a human gate → **mandatory human
review**. There is no "high-confidence" bypass: a proposal of the form "skip the human
gate when self-rated confidence is High" is a self-granted permission escalation — always
HOLD it for a human.

---

## 6. Isolate self-modification in git worktrees

When the system modifies its own loops, skills, or specs, do it on an isolated worktree
so a bad change cannot corrupt the working tree:

```bash
git worktree add ../rl-experiment-$(date +%Y%m%d) -b rl/self-mod-xyz
# run the change + tests inside the worktree; merge only after the reviewer pass (§3)
# and, for skill/spec edits, after the human gate (§5).
git worktree remove ../rl-experiment-$(date +%Y%m%d)
```

`loop_driver.sh` already snapshots `state/` (dated `state.bak-TIMESTAMP`) inline before
each cycle. For loop entry points that are NOT the driver — scheduled Meta-Improvement /
Discovery runs (§2) or a custom driver — call `state_orchestrator.py begin-cycle`, which
makes the same dated backup before the cycle, so state is recoverable across every entry
point even outside a worktree.

---

## 7. Cost & model routing

Route model and cost decisions through the `cost-aware-llm-pipeline` skill — do not
reinvent budget tracking. `loop_driver.sh` already takes `--max-cost` as a hard ceiling
(summing each turn's reported `total_cost_usd`) and defaults to a cheaper model for
Primary work and a stronger model for the reviewer pass; let `cost-aware-llm-pipeline`
inform which model each task should use, and keep `--max-cost` as the external backstop.

For non-driver entry points (scheduled Meta/Discovery runs, custom drivers) that need a
spend ceiling spanning more than one process, feed each turn's cost to
`state_orchestrator.py add-cost <usd>`: it accumulates spend in a shared JSON counter and
exits nonzero (STOP) once the configured cap is exceeded, so a budget can be enforced
across runs that the driver's per-process total cannot see.

---

## 8. Full-auto safety

Before running unattended (no human watching each turn), enable the `safety-guard` skill
so destructive or irreversible actions (deletes, force-push, deploys, mass edits) are
blocked or escalated. Pair it with the PreToolUse hook in §4. Full-auto without
`safety-guard` is unsupported.

---

## 9. Resume after a pause

State is on disk, so resuming is just re-running the driver against the same project —
each turn reads `SHARED_TASK_NOTES.md` and `PROGRESS.md` to recover where it left off:

```bash
./loop_driver.sh --project ./my-recursive-agent --max-iters 10 --max-cost 5.00
```

For a one-off interactive resume (no new driver run), start a session with:

```
Resume the recursive loop system in ./my-recursive-agent. Read state/SHARED_TASK_NOTES.md
and state/PROGRESS.md, determine the next action from the last recorded phase, and
continue. Do not restart from scratch.
```

Check bounds and the recommended next action at any time:

```bash
python3 state_orchestrator.py --project ./my-recursive-agent --status
```

---

## Reference

- `loop_driver.sh` — the external Primary driver; owns the iteration/cost/completion
  bounds. Do not replace it with a single prompt.
- `state_orchestrator.py` — JSON cycle/cost counter, bound enforcement, pre-cycle state
  backup, next-action hint. A helper for, not a replacement of, the driver.
- `opportunity-scoring-rubric.md` — the scoring contract enforced in §5.
- `../state-templates/` — schemas for the state files.
- Skills: `autonomous-loops` (loop architectures), `safety-guard` (destructive-action
  protection), `cost-aware-llm-pipeline` (budget/model routing).
- `../EXPERIMENTS_REPORT.md` — evidence behind §3 and §5.
