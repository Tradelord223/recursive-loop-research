# Opportunity Scoring Rubric — Discovery Loop Gate

**Version**: 2.0
**Purpose**: Give the Opportunity Discovery loop a consistent way to decide which follow-on tasks are worth spawning. This rubric is a triage instrument, not a calibrated score. Read it as such.
**Provenance**: Corrected per the blinded Experiment 1 findings in `EXPERIMENTS_REPORT.md`. Two earlier conclusions (a clean "Total≥28 gate" and "Total kills aligned trivia") were retracted after the stimuli were blinded; do not reintroduce them.

---

## How this gate actually works (read first)

**`Alignment >= 8` is the load-bearing gate. It does essentially all the adjudication.**
Everything else on this page is supporting context for that one decision and for routing the cases the gate cannot resolve alone.

Three facts about this rubric — established by blinded rating in `EXPERIMENTS_REPORT.md` — that you must keep in front of you:

1. **The four dimensions are NOT scored independently in practice.** Raters fold "low-value / tangential / trivial" straight into the Alignment number. Once an item is judged trivial it does not keep a high Alignment score, so the nominal 40-point, 4-axis structure collapses to a single value judgment wearing the Alignment label. Do not treat the four axes as orthogonal evidence.

2. **`Total` is a HEURISTIC, not a calibrated or validated cutoff.** Across 60 blinded ratings, `Total` independently rejected an aligned (A≥8) item in only 3 ratings and never at consensus — no blinded "aligned-but-Total-killed" item could be produced at all. Use `Total` for coarse prioritization and to flag the boundary band. Never present any `Total` number — including 28 — as a validated threshold, and never auto-spawn on `Total` alone.

3. **The gate is a coin-flip at the boundary, and raters are swayed by wording.** A borderline item split 2-of-6 raters under blinding. The same opportunity reversed its spawn/reject verdict purely on how its description was worded — moving the score more than the opportunity's actual content did. Both facts drive the routing rules below.

Honest scope: these findings measure one model's self-consistency, not whether the verdicts are correct in any absolute sense, and not cross-model or human agreement. Spot-check spawned items by hand at each scheduled `ALIGNMENT_CHECK.md` review.

---

## Scoring Dimensions (0–10 each)

### 1. Alignment (the gate — everything turns on this)
- **10**: Directly and obviously advances the immutable Original Intent with a clear causal link.
- **7–9**: Strong indirect support or a natural extension that users of the primary deliverable would expect.
- **4–6**: Related but tangential; nice-to-have only in a broader vision.
- **0–3**: Weak or no clear connection to the original goal.
- **Alignment ≤ 6 auto-rejects; Alignment 7–8 goes to the human gate (never auto-reject, never auto-spawn).** Alignment is the one load-bearing cutoff on the page, but 7–8 is the coin-flip band — see the cascade below. In practice "low value" and "trivial" show up here as a depressed Alignment score, not on the other axes — expect that and do not fight it.

### 2. Impact
- **10**: High user/business value, or materially compounds the primary deliverable.
- **7–9**: Meaningful improvement in capability, reliability, or user experience.
- **4–6**: Incremental or niche value.
- **0–3**: Low or speculative value.

### 3. Feasibility (within the current loop system)
- **10**: Implementable with existing tools, state files, and loop patterns in a few cycles.
- **7–9**: Needs moderate new patterns or one new tool/skill addition.
- **4–6**: Needs significant new capability or an external dependency.
- **0–3**: Out of reach or extremely high effort right now.

### 4. Learning Value (for the system itself)
- **10**: Teaches reusable skills/patterns the agent can apply across future loops.
- **7–9**: Solid learning in verification, state management, or domain knowledge.
- **4–6**: Some incremental learning.
- **0–3**: Mostly repetitive work, little new insight.

**Total** = sum of the four axes, out of 40. Treat it as a rough sort key for the queue and as the trigger for the boundary-band routing below — not as a decision threshold in its own right.

---

## Routing rules (replaces the old auto-spawn threshold)

There is no "auto-spawn at Total ≥ 28." Apply the following as a **first-match-wins cascade** — evaluate top to bottom and stop at the first rule that matches. This is exhaustive and unambiguous; every opportunity lands in exactly one route, and any case the gate can't resolve falls through to the human.

| # | Condition (first match wins) | Route |
|---|---|---|
| 1 | Alignment ≤ 6 | **Reject.** Drop from the queue. |
| 2 | Alignment ≥ 9 **and** Total clearly above the boundary band | **Eligible to spawn** via `loop_driver.sh`, subject to the SEPARATE-AUTHORING rule below and to `safety-guard`. |
| 3 | Everything else (Alignment 7–8, OR Total inside/below the band, OR any case rules 1–2 didn't catch) | **BOUNDARY BAND → human gate.** Do NOT auto-spawn. Park in `OPPORTUNITIES_QUEUE.md` flagged for human review. |

"Above the boundary band" means clear of the 26–30 zone; treat it as a relative position, never as a fixed validated number. The cascade routes uncertainty to a person by construction: only an unambiguous Alignment-9+ item clear of the band spawns on its own.

### BOUNDARY-BAND rule
Any opportunity landing at **Alignment 7–8 OR Total 26–30** is in the coin-flip zone where this rubric cannot decide reliably — a borderline item split 2-of-6 raters under blinding (`EXPERIMENTS_REPORT.md`, Exp1). These go to a human, never to auto-spawn. The band is wider than the spawn-eligible region on purpose: when the gate can't decide, a person decides.

### SEPARATE-AUTHORING rule
The agent that **scores** an opportunity must NOT be the agent that **wrote its description.** Raters reverse their verdict on rewording, and the Discovery loop both writes and scores — so an opportunity can be (even unintentionally) phrased to pass its own gate. This is a self-gaming vector. Enforce one of:
- Score from a **neutral one-line spec** the scorer did not author; or
- Have a **second agent re-describe** the opportunity first (a distinct `claude -p` turn or a distinct subagent), then score the re-description.

This is the same evaluator-optimizer separation the rest of the suite applies to self-modification. Exp2 (`EXPERIMENTS_REPORT.md`) did not empirically confirm collusion, so treat separation here as cheap, principled defense-in-depth — not as proven necessity. Keep it; it costs little.

---

## Worked examples

The four-axis scores below are illustrative. In every case the **routing decision is driven by Alignment plus the boundary-band rule** — not by a precise `Total` arithmetic.

### Example 1 — SaaS landing-page goal
**Neutral spec (authored separately from the scorer):** "Add an A/B testing harness for hero copy and CTAs, logging results to a dashboard."

- Alignment: 9 (directly serves the page's conversion goal)
- Impact: 8
- Feasibility: 6 (new analytics + dashboard)
- Learning Value: 7
- **Total: 30** → **Boundary band (Total 26–30) → human gate.** Despite strong Alignment, the Total sits in the coin-flip zone, so this is parked for human review rather than auto-spawned. A person decides whether the new analytics dependency is worth a cycle now.

### Example 2 — AI coding-assistant goal
**Neutral spec:** "Generate property-based tests for core functions."

- Alignment: 10 (core to a reliable coding agent)
- Impact: 9
- Feasibility: 8
- Learning Value: 9
- **Total: 36** → **Spawn-eligible.** Alignment is unambiguous and Total sits well clear of the boundary band. Route to `loop_driver.sh` (subject to `safety-guard`). Because the change is additive and reversible (new tests only), it is also a candidate for the Meta-Improvement loop to fold into the core verification step.

### Example 3 — General research-agent goal
**Neutral spec:** "Build a weekly competitor-analysis sub-agent that maintains a living landscape doc."

- Alignment: 6 (related to research, not core to the stated research goal)
- Impact: 7
- Feasibility: 8
- Learning Value: 5
- **Total: 26** → **Reject.** Alignment ≤ 6 settles it; the Total is moot. Note that the "tangential" judgment lands as a low Alignment score — that is the expected behavior, not a scoring error.

### Example 4 — Borderline item routed to a human (the case the old rubric got wrong)
**Neutral spec:** "Ship a default visual theme for the tool's generated output."

- Alignment: 7–9 (raters disagree on whether a default theme advances the Original Intent or is polish)
- Impact: 6
- Feasibility: 7
- Learning Value: 6
- **Total: spread 27–31, straddling the band** → **Boundary band → human gate.** This is the kind of borderline item that, under blinding, split 2-of-6 raters on the spawn/reject verdict (`EXPERIMENTS_REPORT.md`, Exp1, item B1). It clears neither rule 1 nor rule 2 of the cascade cleanly, so it falls to rule 3. The rubric cannot adjudicate it. Correct action: park in `OPPORTUNITIES_QUEUE.md` for a human, NOT auto-spawn. Re-running the scorer to "break the tie" only re-rolls the coin flip.

---

## Using this in the Discovery loop

1. Brainstorm 5–10 candidates.
2. For each, produce a **neutral one-line spec authored by a different agent than the scorer** (SEPARATE-AUTHORING rule).
3. Score each spec against the four dimensions, with written justification.
4. **Apply the Alignment gate first:** drop everything with Alignment ≤ 6.
5. **Apply the boundary-band rule:** route Alignment 7–8 OR Total 26–30 to the human gate. Do not auto-spawn these.
6. Of what remains, sort by Total + Learning Value for prioritization only, then spawn eligible items via `loop_driver.sh` under `safety-guard`.
7. Record every candidate, its score, its route, and the author/scorer split in `OPPORTUNITIES_QUEUE.md`.
8. At each scheduled `ALIGNMENT_CHECK.md` review, spot-check spawned items by hand — the gate is single-model self-consistency, not a calibrated instrument.
