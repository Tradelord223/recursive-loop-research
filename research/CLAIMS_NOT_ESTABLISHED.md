# Claims this project does NOT establish

A standalone register of the limits. The credibility of this project comes from its
disclosed boundaries and its retractions — **not** from the strongest-sounding number in
any results file. If you are deciding how much to trust the work here, read this file
first; it is written to be exhaustive and unflinching, and it is the document the rest of
the repo is held to.

Two rules govern everything below:

1. **Every value oracle in this project was authored by the same person who built the
   judgment being tested.** That circularity ("I wrote the answer key") recurs in new
   clothes across experiments and is the single deepest unresolved threat to every
   positive result. See `../ROADMAP.md` ("The wall, named").
2. **Every "rater," "reviewer," and "committee" is a separate fresh-context Claude
   subagent running the same model.** Every result therefore measures *one model's
   internal self-consistency* — not agreement across different models, not agreement with
   humans, and not correctness in any absolute sense. This is stated as a hard ceiling in
   `../EXPERIMENTS_REPORT.md` and it bounds **all** numbers in this repo.

Cross-references use paths relative to this file (`research/`).

---

## 1. The recursion itself (B5) is UNTESTED

The project's namesake — a *self-recursive* judgment system that improves by feeding
outcomes back into its own next-round judgment — has **not been tested at all.**

- Every experiment to date (Exp3–Exp7) measures a **single round** of judgment: "does the
  ranking correlate with an oracle," "does a committee certify correctness." None of them
  measures the load-bearing recursive claim: **does feeding realized outcomes back improve
  the *next* round's ranking?** That is build-step **B5** in `../ROADMAP.md`, and it is
  explicitly marked "NOT yet tested."
- The live consequential loop is gated on B5 passing. It has not been attempted, so:
  - We do **not** know whether outcome feedback improves judgment.
  - We do **not** know whether it degrades it, drifts, or self-games.
  - We do **not** know whether the feedback signal can be closed without re-introducing the
    circular-oracle problem.
- A measurement substrate for B5 exists (`../revealed-preference/prefs.py`, wired to the
  human gate at `../ultra-suite/orchestration/gate.py`) and its machinery is verified
  deterministically and on the LLM path. **But it is awaiting real data** (≥20 of the
  user's genuine accept/reject decisions). No accuracy is claimed; no recursion has run.
- Compounding constraint: B5 is **untestable on a saturated metric.** Exp5 hit ρ=1.0,
  which leaves no headroom for feedback to improve anything. B5 needs a *contestable,
  non-computable* value signal with genuine rater spread — i.e. an external one — or it
  will produce another clean-but-empty number. See `../experiments/exp5-deceptive/results.md`
  ("B5 is untestable on a saturated metric").

**Status: the central claim of a working recursive self-improvement loop is UNESTABLISHED.**
What exists is a partially-validated *single-round judgment kernel* plus scaffolding, not a
demonstrated learning loop.

---

## 2. Value-calibration under ambiguity is OPEN

The kernel has been shown to do something narrower than "judge value":

- Exp5 (`../experiments/exp5-deceptive/results.md`) showed the model **grounds rankings in
  code structure rather than labels, and resists deception** (it dismissed scary-named dead
  code and correctly valued a trivial-named helper reached by two features). That is real
  and worth having.
- But Exp5 *defined* value ≡ call-graph reach, a quantity with a **unique computable
  answer.** The model computed reach on a task where value was defined to equal reach. That
  proves call-graph tracing and distractor-resistance — **not** value judgment under
  ambiguity.
- The **unanimity (6/6, ρ=1.0) is the tell, not the triumph.** Genuine value judgment is
  contestable; this project's own data shows spread exactly where value is contestable
  (Exp1 item B1 split 2-of-6; Exp3 ties). Exp5 produced no spread because the task had a
  right answer every rater could compute. It never entered the regime that matters.

What is therefore **NOT established:** that the system can calibrate **multi-dimensional,
contestable value** — real value being roughly severity × reach × user-exposure ×
frequency, which has **no single computable oracle** and on which competent independent
raters would legitimately disagree. Every value proxy tested so far (test-count in Exp4,
blast-radius in Exp5) is one dimension, computable, and author-defined.

**Status: value-calibration on contestable value is OPEN and untested.**

---

## 3. Single-model self-consistency is the CEILING — correctness is not measured

This is the most important limit to internalize, because it caps every positive result.

- Every rater/reviewer/committee member is the **same model in a fresh context.** So a high
  agreement number means "this model is consistent with itself," **not** "this model is
  right," and **not** "independent judges concur."
- Worse than a neutral ceiling: same-model raters share blind spots, so they can be
  **consistently and confidently wrong together.** Exp6
  (`../experiments/exp6-disjointness/results.md`) demonstrated this concretely: on pair P13,
  a same-model committee unanimously rated a strictly-dominated (4/12) implementation
  *equal* to a perfect (12/12) one — 6/6, confident, wrong — because every rater missed the
  same double-count bug. Inter-rater agreement there certified nothing.
- Consequently the project does **not** claim, anywhere, that its gate verdicts are
  *correct* in an absolute sense. It claims only consistency, and only within the bands the
  data covers.

**Status: self-consistency is all that is measured. Absolute correctness of the judgment is
not established by any experiment here.**

---

## 4. Cross-model and human agreement are ABSENT

A direct consequence of #3, called out separately because it is the obvious next question
and the project must not be read as having answered it.

- **No cross-vendor / cross-model validation.** Exp7 added Claude *tier* diversity
  (opus/sonnet/haiku) but these are all Claude — shared-family blind spots remain. A
  genuinely independent (non-Claude) rater was **never tested.** Listed as the real next
  step in `../experiments/exp7-diverse/results.md`.
- **No human agreement.** No experiment compares the system's rankings or verdicts against
  human judgment. The literature scan (`./LITERATURE.md`) notes the only non-circular
  validator is **revealed human preference** — and that data does not yet exist (≥20 real
  decisions pending; see #1).
- Therefore: claims of the form "the judgment is good/right/trustworthy" are **unsupported**
  by any external referent. The system has only ever been graded against (a) oracles its own
  author built, and (b) other instances of itself.

**Status: cross-model agreement and human agreement are entirely unmeasured.**

---

## 5. The four retracted / demoted results

Kept visible on purpose. A result that was walked back is more informative than one that
was never stress-tested, and these four are the spine of the project's credibility. One
line each on why; full accounting in the cited files.

1. **Exp4 ρ=0.986 — RETRACTED.** The near-perfect correlation between predicted ranking and
   "realized value" was confounded: realized value = how many tests *I chose to write* per
   function (author-set, not independent), and the task descriptions **telegraphed** bug-vs-
   cosmetic, so the model may have read the answer off the wording rather than the code.
   Demoted B2 from PASSED to PARTIAL. (`../experiments/exp4-closedloop/results.md`)

2. **Exp5 ρ=1.0 — DEMOTED to a narrow sub-claim.** Value was *defined* as call-graph reach
   and the model merely computed reach two ways — a tautology that moved but did not leave;
   ρ=1.0 / 6-of-6 unanimity is the signature of a task with a single computable answer, not
   of value judgment under ambiguity. Survives only as: structure-grounding + deception-
   resistance. (`../experiments/exp5-deceptive/results.md`)

3. **P03 — RETRACTED as evidence (circular).** P03 (impl_04 vs impl_06, both 4/12 on *my* 12
   toy tests) was initially counted as a second unanimous error; but "passes an equal number
   of my toy tests" is not "equal merit" — impl_06 is the right algorithm one bug away, and a
   maintainer could defensibly rank it higher. Scoring the raters "wrong" there just re-
   asserts merit ≡ test-count (the Exp5 error in new clothes). Dropped; the Exp6 finding rests
   solely on P13, which needs only domination, no merit definition.
   (`../experiments/exp6-disjointness/results.md`)

4. **Exp6→Exp7 "diversity fixes it" — DEMOTED / NOT SUPPORTED.** The claim that committee
   diversity converts confident-wrong unanimity into informative disagreement collapsed under
   a control: a **6× opus run through the clean Exp7 harness was ~50/50 on P13, not
   unanimous** — so Exp6's 6/6 was a **persona/sampling artifact** (cavecrew = opus + caveman
   persona + small n), not robust same-model blindness, and the diversity contrast varied
   three things at once (persona, harness, model-mix), not one.
   (`../experiments/exp7-diverse/results.md`)

What survives from this leg is **not** a diversity result but a methodology result: in a
single session, controls demoted four clean-looking findings. That discipline — not any ρ —
is the contribution. See `./LITERATURE.md` ("What Exp6/Exp7 actually showed").

---

## 6. Other limits that bound the positive results

Real but smaller caveats, recorded so no positive result is read past its evidence.

- **Exp1 — the gate is calibrated only loosely.** Blinded re-runs showed `Total≥28` is
  unsubstantiated (Alignment≥8 does essentially all the adjudication, and is a coin-flip in
  the A≈7–8 band); and that raters are **strongly suggestible to self-authored framing** — a
  self-gaming vector, since the discovery loop both writes and scores opportunities. Two
  conclusions were retracted after a leading-stimulus methodology error.
  (`../EXPERIMENTS_REPORT.md`, Exp1)
- **Exp2 — the collusion result is NULL, and is two failures, not a finding.** Same-context
  self-review did not rubber-stamp bad proposals — but the "these are YOUR proposals"
  manipulation never induced ownership in a stateless subagent (manipulation failure) and the
  planted hacks were blatant (floor effect). It **failed to find** the risk; the separate-
  reviewer fix is kept as cited defense-in-depth, **explicitly unvalidated**, not as measured
  necessity. (`../EXPERIMENTS_REPORT.md`, Exp2)
- **Exp3 — pairwise fixes ordering, not the cut line.** Relative judgment is far lower-noise
  than absolute scoring (validated), but "B1 is rank 2 of 6" does not answer "is rank-2 worth
  a build cycle." The cut still needs a fixed reference anchor (B3, not yet experimentally
  validated). (`../experiments/exp3-pairwise/results.md`)
- **Scale and legibility.** Every code experiment uses tiny, clean, traceable artifacts (6
  functions, one file, a legible call graph). Real codebases have large/obscure graphs
  (dynamic dispatch, framework magic, cross-module) where the judgment will likely degrade.
  Nothing here is established at repo scale.
- **Synthetic, self-authored oracles throughout.** Test-count, blast-radius, and hidden-
  execution oracles are all tasks the author built. The only non-circular validator named
  anywhere in the project is the user's **revealed preference** — which has no data yet.
- **The disagreement-gating idea is prior art, not novel.** Query-by-Committee (1992), deep
  ensembles, self-consistency, selective prediction, ReDAct/Oversight (2026). The project
  claims an *illustration* against an execution oracle, not a discovery. (`./LITERATURE.md`)
- **Build steps B3, B4 (judgment side), B5, B6 are not experimentally validated.** B4's
  *mechanism* (a router that emits an action) is prototyped, but a working router is **not**
  progress on judgment; conflating the two is the named trap. (`../ROADMAP.md`)

---

## 7. One-paragraph honest summary

This project has established, narrowly and within a single model's self-consistency, that
**relative (pairwise) judgment is lower-noise than absolute scoring** (Exp3) and that the
kernel can **ground rankings in code structure and resist deceptive labels** on a tractable
call graph (Exp5). It has **not** established that judgment calibrates contestable value, that
any verdict is correct in an absolute sense, that independent models or humans agree with it,
or — most importantly — that the **recursive learning loop works at all** (B5 untested). Four
clean-looking results were retracted or demoted by controls and adversarial review. The single
unresolved threat underneath all of it is that **every value oracle was authored by the same
hand as the judgment**, and the only escape — real external human/outcome signal — has not yet
produced data. Treat every positive number in this repo as bounded by this file.
