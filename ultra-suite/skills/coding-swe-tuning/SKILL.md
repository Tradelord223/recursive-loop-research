---
name: coding-swe-tuning
description: Domain tuning for software-engineering and coding-agent work inside the recursive loop suite. Test-driven self-modification, git worktree isolation, deterministic verification signals (tests/lint/types/build) primary with LLM review secondary, separate-context code review, and a strict additive-and-reversible auto-apply gate. Use with recursive-loop-engineer and loop-runner; pair with safety-guard in full-auto.
version: 2.0.0
tags: [coding, swe, test-driven-development, self-modification, git-worktrees, verification, claude-code]
---

# Coding & SWE Tuning for Recursive Loop Systems

Specialized instructions and guardrails for when the recursive loop suite operates in a
**software-engineering / coding domain**. This tuning sits on top of the loop architecture
defined by `recursive-loop-engineer` and driven by `loop_driver.sh` (the external,
bounded driver — the model does not re-prompt itself). It assumes `loop-runner` for
per-turn discipline and `safety-guard` for destructive-action protection in full-auto.

## Core Principles

- **Test-driven self-modification (non-negotiable).** Any code change — feature, bug fix,
  refactor, or self-evolution of a skill or the harness — must be validated against tests.
  Treat a skill file or orchestration script as code under test: propose the change, then
  run the verification suite before it may persist.
- **Worktree isolation.** Every experimental, self-modifying, or new-opportunity change
  happens in a dedicated **git worktree**, never in the main working tree. The main branch
  stays clean until deterministic verification passes. Track active worktrees in
  `WORKTREE_STATUS.md`. Merge to main only on a full pass.
- **Deterministic verification signals are primary.** Tests (unit, integration,
  property-based), linters, type checkers, and the build command are the verification
  loop's ground truth. They are machine-checkable and hard to bluff. **LLM-based review is
  secondary** — it catches reasoning and design defects the signals miss, but it never
  overrides a red signal into green.
- **SWE-bench-style end-states.** For complex tasks, define a verifiable end-state up front
  (e.g., "all relevant tests pass, no regressions, lint clean, types clean, build succeeds,
  the specific behavior is demonstrated"). The end-state is a checklist of deterministic
  signals, not a self-assessment. Do not attach invented success metrics to it.
- **Git hygiene.** Each cycle that produces code yields a clean, conventional-style commit
  on the worktree branch plus a state-file entry. Record what changed and why so a later
  iteration (or a human) can reconstruct the decision.

## Verification: Deterministic First, Separate-Context Review Second

The verification loop runs in two layers, in order:

1. **Deterministic gate.** Run tests/lint/types/build at the cycle boundary via a Claude
   Code **Stop** or **PreToolUse hook** so the signal is captured mechanically, not from the
   author's self-report. Append the raw result to `TEST_RESULTS.md`. A red gate blocks the
   cycle; no LLM review can clear it.

2. **Separate-context code review.** The reviewer that judges a change MUST run in a
   **different context from the author** — a distinct `claude -p` turn or a distinct subagent
   (Task tool), as `loop_driver.sh` already arranges. This realizes Anthropic's
   evaluator-optimizer separation and the principle "the reviewer should never be the
   author."

   **Honesty note (read this):** separation here is **cited defense-in-depth, not a proven
   safeguard.** Our own experiment (Exp2, blinded) did NOT confirm same-context collusion —
   same-context review rejected blatant reward-hacks about as well as an independent reviewer.
   We keep separation because it is cheap and principled, **not** because it is measured to be
   necessary. Do not claim separation is proven, and do not claim same-context review is
   unsafe. It remains a backstop, never a substitute for the deterministic gate.

## The Auto-Apply Gate (the spine of this skill)

One discriminator governs what a cycle may persist without a human:

> **Additive + reversible → auto-apply candidate. Touches, weakens, or deletes an existing
> test, threshold, gate, or skill → mandatory human gate.**

A change is an auto-apply candidate only if it **adds capability without removing or
weakening any existing check** and is **reversible by deletion** of what it added. Even then
it must still pass the deterministic gate and separate-context review first.

**Auto-apply allowed (additive + reversible only):**
- New tests.
- New files (new modules, new fixtures, new docs).
- Pinned dependencies (a version pin, not an unbounded bump).
- New lint rules or pre-commit / git hooks.

**Mandatory human gate (never auto-apply, regardless of self-rated confidence):**
- Deleting, skipping, or weakening an existing test or assertion.
- Lowering or removing a quality threshold or gate.
- Editing a skill file or the orchestration/harness code.
- Removing, relaxing, or bypassing a human gate.
- Any destructive or irreversible action — defer to `safety-guard` to block it in full-auto.

There is **no high-confidence bypass.** Self-rated confidence does not promote a gated change
to auto-apply.

### Forbidden auto-apply patterns (reward hacks — always HOLD for a human)

These force a green signal by corrupting the signal itself. They are never additive and never
auto-applied:

1. **Skipping or marking a test "flaky" to force green.** Quarantining a failing test to make
   the suite pass is weakening a check, not adding one.
2. **Lowering a coverage threshold.** Moving the gate to meet the code instead of moving the
   code to meet the gate.
3. **Wrapping a test in `try/except: pass`** (or any catch-and-swallow that makes a failing
   assertion stop failing). The test still "runs" but verifies nothing.
4. **Self-skipping the human gate on self-rated confidence** — e.g., a proposal of the form
   "skip the human gate when confidence is High." This is a **self-granted permission
   escalation**: the agent is rewriting its own authority. **Always HOLD.**

Any of these surfacing in a proposal — including disguised as a metric edit in
`CODE_QUALITY_METRICS.md` or a status flip in `TEST_RESULTS.md` — is a hard stop for human
review.

## SWE State Files (routed through the auto-apply gate)

In addition to the suite's core state templates, maintain:

- **`TEST_RESULTS.md`** — Per-cycle log of test/lint/type/build runs: pass/fail counts,
  failing tests, fixes applied. Appending a new run is additive (fine). Flipping a recorded
  failure to "skipped/flaky," or editing history to hide a red signal, is a gated reward hack.
- **`WORKTREE_STATUS.md`** — Active worktrees and their purpose, branch, and merge state.
  Adding/closing an entry tracks reality; it grants no authority to merge unverified work.
- **`CODE_QUALITY_METRICS.md`** — Coverage, complexity, and lint trends over time, for the
  Meta-Improvement loop. **This file is a reward-hack surface:** appending a measured datapoint
  is additive; *editing a threshold downward* recorded here is gated. Treat the thresholds in
  it as checks, not as freely tunable knobs.

State files record signals — they never confer permission to bypass the gate.

## Meta-Improvement in a Coding Context

The Meta-Improvement loop runs **periodically — driven by `/loop <interval>`,
`ScheduleWakeup`, or a cron routine (`/schedule`)**, not by the model re-prompting itself.
When it reflects on coding traces:
- Analyze test-failure patterns: flaky tests, missing coverage, weak assertions. Propose
  *strengthening* checks, never removing them.
- Identify repeated manual fixes worth automating — typically a **new** lint rule or
  pre-commit hook (additive, auto-apply candidate).
- Propose new tools or MCP servers when an external action recurs.
- For self-evolution of a skill or the harness: the change touches a skill or harness file,
  so it is **gated** — author in a worktree, pass the deterministic gate and separate-context
  review, then route to a human. Defer budget/model routing for these extra passes to
  `cost-aware-llm-pipeline`.

## Opportunity Discovery in an SWE Context

Score SWE follow-on work (missing test coverage, expected related features, refactors,
observability, security hardening) with `opportunity-scoring-rubric.md`. Alignment is the
load-bearing gate; the dimensions are not independent and the point total is a heuristic, not
a validated threshold. Score from a neutral spec written by a different context than the one
that proposed the work. Do not re-derive the rubric here.

## Execution Pattern

Plan → implement in a **git worktree** → run the deterministic suite (tests/lint/types/build)
via a cycle-boundary hook → **separate-context** reviewer inspects results and code → fix in
the same or a new worktree on failure → and only then: auto-apply if additive + reversible, or
route to a human gate otherwise → merge to the clean main branch on full pass. The loop across
cycles is driven externally by `loop_driver.sh`, bounded by its hard `--max-iters` /
`--max-cost` ceilings, with `safety-guard` engaged in full-auto.

Use this tuning whenever the recursive system works on codebases, builds tools, or evolves its
own implementation.
