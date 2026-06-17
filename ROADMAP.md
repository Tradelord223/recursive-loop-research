# Roadmap — a REAL self-recursive judgment system

Goal (user's): loops that invoke skills and workflows, with a genuine self-recursive judgment
system deciding what to do — not a suggestion engine, an actual decider that improves itself.

This is buildable. The honest framing below is what keeps it from becoming an impressive demo
that quietly doesn't work.

## The reframe: grounding, not bootstrapping

Recursive self-improvement is **already proven — wherever the reward is unfakeable.** AlphaZero
is recursive self-judgment via self-play; it works because win/loss can't be gamed. Formal-
verification loops, same. The open (hard) problem is *not* "self-recursive judgment" in general
— it's **self-recursive judgment with no unfakeable reward.**

So one question is asked of every component: **where is the signal this judgment cannot fake?**
- "Did this code change pass the tests / fix the bug / avoid regressions?" → unfakeable. BUILD HERE.
- "Is this opportunity good?" (model scores its own idea vs a rubric it wrote) → fakeable. The
  trap. Never the kernel.

Test-grounded self-improvement in the coding domain *is* the vision, and it is genuinely
achievable. We build where reality votes.

## Two asks, opposite difficulty (do not conflate)

1. **Mechanism — loops invoke skills/workflows.** EASY (~20%). Verified: a headless
   `claude -p` turn has Skill, Workflow, Agent, Bash, Edit in its toolset. A "router" turn emits
   a structured ACTION; the driver executes it. Prototype: `orchestration/action_router.sh`.
   (Caveat: the Workflow tool is present but its firing is opt-in-gated; for autonomous use, run
   it through a permission/keyword the driver supplies, or fall back to the Agent tool.)
2. **Judgment — which action, and was the choice right.** HARD (~80%). This is the entire
   research problem. A working router is NOT progress on judgment; conflating them is the trap.

## The keystone (shared checkpoint — we do NOT skip this)

**Exp3 proved consistency, not correctness.** Pairwise stabilized item B1's *ranking*; it did
not show the ranking is *right*. The whole system rests on one untested assumption: **that
stabilized, anchored judgment tracks realized value.**

→ **The make-or-break experiment, before any grounded loop is built:** in a real repo with a
test suite — rank candidate tasks → implement the top one → measure *realized* value (tests
pass / bug fixed / no regression) → ask: does *predicted-worth* correlate with *realized-value*,
and does feeding outcomes back *improve the next round's ranking*? If yes, the kernel is real and
we build the loop on it. If no, we've found the real wall before spending on scaffolding.

This is a gate, not a step. Building the full grounded loop before it passes is the v2 sin one
level up.

## The grounding stack (what makes judgment real, cheapest → hardest signal)

1. Relative/pairwise + fixed reference anchor — cheapest noise-reducer. **Validated (Exp3).**
2. Panel disagreement → route to human (uncertainty as a signal). Partly in place.
3. Revealed human preference — learn from your accept/reject log; predict *your* decision.
4. External world metrics — conversion, latency, revenue (real but delayed/noisy).
5. Deterministic code signals — tests/build/lint/perf. **Hardest ground truth. The kernel.**

A real system stacks these and **closes the loop**: action → grounded outcome → recalibrate the
judgment (reference anchors, scorer). Self-recursive, but reality keeps voting, so it can't drift
into self-delusion. That last clause is the difference between this and the thing people call
impossible.

## Safety scales UP with autonomy (designed in from line 1)

A loop that can invoke workflows spawns agent fleets — the runaway/cost surface multiplies. So
the external hard caps (`--max-iters`/`--max-cost`/duration), `safety-guard`, and the
additive+reversible auto-apply gate get *more* load-bearing the moment the loop can call tools,
not less. The router must run inside those bounds, never outside them.

## Build order (each brick experiment-gated before it's trusted)

- **B1 ✓ DONE** — pairwise > absolute scoring (Exp3): relative judgment is far lower-noise.
- **B2 ~ PARTIAL — closed-loop correctness experiment (Exp4).** Coarse result is solid: judgment
  robustly separates real bugs from cosmetic no-ops (unanimous, no position bias). The
  fine-grained ρ=0.986 was **retracted on review** — confounded by (a) the oracle being my own
  test-allocation and (b) telegraphing descriptions (no code-independent signal). Value-prediction
  against an independent signal is NOT yet established.
- **B2.5 ✓ PASSED (narrow sub-claim) — Exp5.** Grounds rankings in **code structure, not labels**,
  and **resists deception** (scary-named dead code → 0; trivial-named reachable helper → #2 via the
  `format_date`→`_pad2` indirection). ρ=1.0 / 6-of-6 unanimous. BUT the verdict is narrow: I
  *defined* value ≡ call-graph reach, and reach has a unique computable answer — so this proves
  **call-graph-tracing + distractor-resistance**, NOT value-judgment under ambiguity. The
  unanimity is the tell. **Value-calibration on contestable, multi-dimensional value: still OPEN.**
- **B3** — reference-anchored gate: turn the pairwise ranking into a stable spawn/no-spawn cut
  (beat a fixed floor reference, not an absolute 28).
- **B4** — action-router (mechanism; prototype already drafted): cycle proposes → ranks →
  executes one of {skill, workflow, agent-fleet, primary work, escalate-to-human}, in bounds.
- **B5** — outcome feedback → recalibration: the actual self-recursion (does feeding test
  outcomes back improve next-round ranking?). NOT yet tested. The live consequential loop is
  gated on B2.5 **and** B5 passing.
- **B6** — drift monitor: semantic distance of chosen actions from the Original Intent over
  generations; halt/escalate past a threshold.

## Side study (Exp6) — disagreement-gating, scanned + stress-tested

- **Lit scan** (`research/LITERATURE.md`): the "disagreement → abstain/escalate" idea is **prior
  art** (QBC 1992 → ensembles → self-consistency → ReDAct/Oversight 2026). Not claimed as novel.
- **Exp6 + Exp7** (`experiments/exp6-disjointness/`, `experiments/exp7-diverse/`): tested whether a
  **same-model committee** is blindly unanimous and whether **diversity** fixes it. **Both demoted by
  a controlled baseline.** Exp6 observed a committee (cavecrew-builder = opus + caveman persona) go
  6/6 unanimous-WRONG on P13 (strictly-dominated impl rated tied with a perfect one) — but a 6×opus
  control through the clean Exp7 harness showed clean opus is **~50/50 on P13, not unanimous**. So
  Exp6's unanimity was a **persona/sampling artifact**, not robust same-model blindness, and Exp7's
  "diversity breaks it" contrast is **NOT supported** (single-tier already disagrees as much). Two
  more retractions: P03 (circular, "equal on my toy tests" ≠ merit) and the Exp6→Exp7 "controlled
  manipulation" framing (3 things varied, not 1). **What survives:** an *existence* proof that
  consensus CAN be confidently wrong, and the unchanged design rule (justified anyway): **never
  auto-act on the loop's own consensus; route past a non-model signal.** The methodology — controls
  catching my own clean-looking overclaims — is the real result of this leg.

Status: B1 ✓ (pairwise > absolute). B2.5 ✓ narrow (structure-grounding + deception-resistance;
value-calibration still OPEN). B4 mechanism prototyped.

**The wall, named:** every synthetic value oracle is one I author → circularity keeps recurring
(test-density → blast-radius → next). Testing value-prediction and B5 (feedback improves
next-round) requires an **EXTERNAL value signal I didn't generate** — the user's real
accept/reject decisions, or real outcome metrics in real repos — AND a non-saturated task (ρ=1.0
leaves no headroom for feedback to improve). **Next is not another synthetic ranker; it's
instrumenting a real signal.**

**B5 substrate BUILT — `revealed-preference/prefs.py`.** Logs the user's real accept/reject
decisions, predicts the user's call via few-shot of their history, and grades against their
held-out decisions (LOO + prequential learning curve vs a majority baseline). Measurement
machinery verified deterministically (stub) + LLM path verified. **Awaiting real data**
(≥20 decisions) — no accuracy claimed yet. The only non-circular path to the B5 answer.

**Gate WIRED — `ultra-suite/orchestration/gate.py`.** Capture is now automatic: the headless loop
parks gate proposals (`enqueue`, called from `action_router.sh` escalate + surfaced by
`loop_driver.sh`); the human `review`s them, and each accept/reject auto-logs to prefs.py
(`review --suggest` pre-shows the predictor's guess so corrections become training examples).
Fail-safe capture to `state/GATE_RESOLVED.jsonl`. Verified end-to-end. The safety gate IS the
training-data source — so real B5 data accrues simply by running the system safely.
