# Recursive Loop System — Ultra Suite (v3)

A bounded, self-improving, opportunity-discovering autonomous agent system for Claude Code,
built on three coordinated loops over persistent file state. This is the corrected,
grounded successor to the v2 package: same thesis, every claim now true and wired to real
Claude Code primitives, and every threshold/safety claim either backed by an experiment or
explicitly labeled as unproven.

> The one-line correction that drives everything here: **the loop lives outside the model.**
> A single prompt does not run forever. An external driver (`loop_driver.sh`, `/loop`,
> `ScheduleWakeup`, a cron routine, or hooks) re-invokes Claude each cycle. The skills below
> describe *what to think* each cycle; the driver is *what makes the next cycle happen*.

## The three loops (and the real primitives that run them)

| Loop | What it does | Driven by | LangChain 4-layer |
|------|--------------|-----------|-------------------|
| **Primary Execution** | Complete the goal with strong verification | `loop_driver.sh` / `continuous-claude` / Actions | Agent + Verification |
| **Meta-Improvement** | Reflect on traces/mistakes → propose improvements | scheduled `/loop` / `ScheduleWakeup` / cron | Hill-Climbing |
| **Opportunity Discovery** | Find aligned follow-on work, score it, gate it | post-cycle hook / scheduled run | (feeds Agent) |
| *(trigger layer)* | Fire cycles on schedule/event | cron routine / hooks / `ScheduleWakeup` | Event-Driven |

## Contents

```
skills/
  recursive-loop-engineer/SKILL.md   # flagship: one prompt -> a Master Recursive Architecture Spec
  loop-runner/SKILL.md               # operator: runs the loops via real external drivers, enforces caps + gates
  coding-swe-tuning/SKILL.md         # SWE domain: worktrees, deterministic verification, separated review
opportunity-scoring-rubric.md        # corrected: Alignment is the gate; Total is a heuristic; boundary band -> human
state-templates/                     # SHARED_TASK_NOTES (the context bridge) + corrected logs/queues
orchestration/
  loop_driver.sh                     # the real bounded external loop (claude -p, cost/iter caps, separate reviewer)
  state_orchestrator.py              # real cycle/cost counter + state backup (replaces the v2 no-op)
  action_router.sh                   # cycle picks an action {skill,workflow,agents,primary,escalate}
  gate.py                            # human gate: parks proposals, review auto-logs decisions to prefs.py
  claude-code-commands.md            # real launch / schedule / resume patterns
EXPERIMENTS_REPORT.md                # the two backed experiments (provenance for every corrected claim)
experiments/                         # raw stimuli + rating data behind the report
EVIDENCE.md                          # one-page map: each claim -> its source/experiment
```

## What changed from v2, and why

Every change is traceable to verified research or a backed experiment in
`EXPERIMENTS_REPORT.md`:

- **Executable, not aspirational.** v2's "one starter command runs indefinitely" was false
  and its Python orchestrator was a no-op (it counted the word "Cycle" in a file). Replaced
  by `loop_driver.sh` (real `claude -p` loop, hard cost/iteration caps, completion-signal
  streak, `SHARED_TASK_NOTES.md` context bridge, separate-context reviewer) and a real
  `state_orchestrator.py`.
- **Rubric corrected (Exp1, blinded).** `Alignment ≥ 8` is the load-bearing gate; the
  `Total ≥ 28` cutoff is a heuristic, *not* a validated threshold; the four dimensions are
  not independent; the boundary band (Align 7–8 or Total 26–30) goes to a human; and scoring
  is separated from authoring (raters reverse verdict on rewording — a self-gaming vector).
- **Evaluator-optimizer separation** (Anthropic pattern; `autonomous-loops` "reviewer ≠
  author") is enforced — but labeled honestly as cited defense-in-depth that our own
  collusion experiment (Exp2) did **not** confirm.
- **Auto-apply is additive + reversible only.** Anything destructive, irreversible,
  gate-weakening, or skill-editing requires a human gate — no "high-confidence" bypass.
- **Defers to shipping skills** instead of reinventing: `autonomous-loops` (loop
  architectures), `safety-guard` (destructive-action protection), `cost-aware-llm-pipeline`
  (budget + model routing).

See `INSTALL.md` to install, and `EVIDENCE.md` for the provenance of each claim.
