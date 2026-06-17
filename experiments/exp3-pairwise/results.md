# Exp3 — Pairwise tournament vs absolute scoring (does relative judgment cut the noise?)

**Question.** Exp1 (blinded) showed absolute 0–10 scoring is a coin-flip at the boundary —
item B1 split 2-of-6 raters on the spawn/reject verdict. Does *pairwise* comparison (judge
"which of these two is more worth building," aggregate to a ranking) reduce that noise?

**Method.** Same blinded corpus B1–B6, same goal, same model. 8 independent raters each judged
all 15 pairs (forced choice + confidence). **A/B order counterbalanced**: 4 raters saw each pair
forward, 4 reversed, to cancel position bias. Aggregated by Copeland win-count. Compared against
Exp1's absolute data on the identical items.

**Results.**
- Per-pair agreement: **12/15 unanimous, 2/15 near (7/8), 1/15 split.** The only split (P14,
  B4 vs B6) is between the two lowest-ranked off-goal items — it never affects a spawn decision.
- Ranking (Copeland): **B3 > B1 > B2 > B4 > B6 > B5** — a clean total order, transitive, with
  near-unanimous support on every consequential pair.
- Position-bias check: aggregate left-slot win rate **50.0%** (59/118). FWD 79% / REV 22% mirror
  almost exactly → raters pick by item merit, not slot. Counterbalancing validated; no bias.
- **Headline — pairwise resolved the item absolute scoring couldn't.** B1, whose absolute
  spawn-verdict split 2-spawn/4-reject (Exp1), is ranked **#2 unanimously** under pairwise:
  beats B2/B4/B5/B6 8-of-8 on all four pairs, loses to B3 8-of-8. Its *relative* position is
  rock-stable even though its *absolute* spawn-worthiness was a coin-flip.

**Interpretation.**
- Relative judgment is dramatically more consistent than absolute scoring for this gate — the
  noise Exp1 measured was largely an artifact of asking for an absolute number, not of the
  underlying preferences. The model knows B1 > B2 and B1 < B3 with certainty; it just can't
  reliably put a stable number on B1.
- **But pairwise fixes ORDERING, not the CUT LINE.** "B1 is rank 2 of 6" is solid; "is rank-2
  worth a build cycle" is a separate question pairwise alone does not answer. The fix is to
  anchor the cut: rank by pairwise tournament, then gate by comparison against a **fixed
  reference item** (a known "we'd definitely build this" and a known "we'd never bother"
  baseline), instead of an absolute 28-point cutoff.

**Honest scope (unchanged ceiling).** Still one model's self-consistency across fresh contexts,
not cross-model/human agreement and not absolute correctness. What it does establish: *given* a
fixed reference frame, relative judgment is the lower-noise instrument — a real, usable
improvement to the rubric, and the foundation for a grounded judgment gate.

**→ Design change this licenses:** replace the absolute `Total` cutoff with
(1) pairwise/tournament ranking of candidates, and (2) a reference-anchored spawn line. Carries
directly into the grounded self-recursive judgment system (next phase).
