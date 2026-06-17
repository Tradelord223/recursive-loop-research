# OPPORTUNITIES_QUEUE

**Purpose**: Prioritized list of discovered aligned follow-on tasks and improvements. Items that clear the gate may be spawned as new Primary Loops; boundary-band items go to a human first.

**Schema**:

```markdown
## [ID] - [Short Title] (Score: A/I/F/L = Total)

**Neutral spec** (authored by a DIFFERENT agent than the scorer):
- One-line, plainly-worded statement of what the opportunity is. The agent that SCORES this item must not be the one that wrote its description. Score from this neutral spec, or have a second agent re-describe before scoring. (Raters reverse their verdict on rewording alone — Exp1, blinded. Because the Discovery loop both writes and scores, this is a live self-gaming vector; the neutral spec closes it.)

**Description**:
- One-paragraph summary of the opportunity.

**Alignment Justification** (to Original Intent):
- How this directly advances the immutable primary goal.

**Scores** (0-10 each):
- Alignment:
- Impact:
- Feasibility:
- Learning Value:

**Total Score**:

**Boundary-band?**:
- yes if Alignment is 7-8 OR Total is 26-30; otherwise no.
- The boundary band is where scoring is a coin-flip. Boundary-band = yes routes to a human gate, never auto-spawn.

**Recommendation**:
- Auto-spawn as new Primary Loop / Human gate (boundary band or risk) / Defer / Reject

**Proposed Execution Approach**:
- High-level loop type and key verification method.

**Discovered During**:
- Which phase / reflection (date)

**Status**:
- New / Awaiting Human Gate / In Progress / Completed / Parked / Rejected
```

**Rules**:
- Entry gate: only add items with **Alignment >= 8** (the load-bearing gate; see `opportunity-scoring-rubric.md`).
- Routing:
  - **Boundary band → human gate.** If Alignment is 7-8 OR Total is 26-30, set Recommendation to *Human gate* and Status to *Awaiting Human Gate*. Do not auto-spawn.
  - **Auto-spawn only above the band**: Alignment 9-10 AND Total >= 31, and the work is additive/reversible in scope. Alignment 9-10 is the real gate; the `Total >= 31` cutoff is likewise heuristic (one above the band), not a calibrated number.
  - The `Total >= 28` figure is a heuristic, NOT a calibrated or validated threshold — present it as such. It sits inside the human-gate band by design, so the band, not the number, does the routing.
- Alignment absorbs most of the value judgment; the four dimensions are not independent in practice. Do not treat the 40-point total as a precise instrument.
- Score from the **Neutral spec**, authored by a different agent than the scorer (see above).
- Sort by Total Score descending when presenting.
- The Discovery loop is driven externally (`/loop`, `ScheduleWakeup`, or a cron routine via `/schedule`), not by the model re-prompting itself. It should review this file each run.
- When auto-spawning, create a dedicated state directory or git worktree for that opportunity so the new loop is isolated.
- `ALIGNMENT_CHECK.md` spot-checks recently spawned items for scoring drift; expect re-scoring from the neutral spec.
