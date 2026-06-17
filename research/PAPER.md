# A Negative-Result Map for Self-Recursive Judgment in a Single-Model Loop

*Consolidated writeup, Experiments 1–7. Status: 2026-06-17.*

## What this paper is, and is not

This is an honest, grounded study of whether a recursive Claude Code loop can judge **its
own** work well enough to decide what to do next without a human in the loop. It is not a
results-paper announcing a positive finding. **The contribution is a methodology and a
negative map**: a sequence of experiments in which controls, blinding, and adversarial
self-review repeatedly demoted our own clean-looking results, leaving a precise account of
*where the open problem actually is* and *which signals are circular*.

The headline question — **does the loop's judgment track the value a real maintainer would
assign?** — is **UNKNOWN.** It cannot be answered with any oracle we authored (every such
oracle made "judgment predicts value" collapse into "the model agrees with my answer key"),
and the only non-circular instrument we have (the user's real accept/reject decisions) does
not yet hold enough data. As of this writing the revealed-preference log holds **5**
decisions; the pre-registered bar is **>= 20** before any accuracy number is reportable.
Until then, the headline is open.

Read every number below against one fixed ceiling, stated once and never relaxed:

> **Single-model self-consistency ceiling.** Every "rater," "reviewer," and "committee
> member" in this study is a fresh-context Claude subagent running the same model. These
> experiments measure *one model's internal self-consistency across contexts* — not
> agreement across different models, not agreement with humans, and not whether any verdict
> is *correct* in an absolute sense. A unanimous panel here is six draws from one
> distribution, not six witnesses.

The per-experiment raw data, stimuli, and analysis live under `../experiments/`. This file
consolidates and supersedes the per-leg narratives for the purpose of a single read; where
it and a sibling file could appear to disagree, the sibling's raw data is authoritative and
this file is the summary. Source-of-truth cross-references are given inline.

---

## The single discipline that produced every real result

One question was asked of every component: **where is the signal this judgment cannot
fake?** (`../ROADMAP.md`). Recursive self-improvement is already proven *wherever the reward
is unfakeable* — AlphaZero via self-play, formal-verification loops. The open, hard problem
is self-recursive judgment **with no unfakeable reward**. So the project's spine is a single
methodological commitment:

- Prefer deterministic, externally-set signals (tests pass / build / call-graph) over the
  model's own scores.
- When forced to use a synthetic oracle, **assume it is circular until proven otherwise**,
  and have a separate-context control try to break the result.
- Blind the stimuli; never let a description tell the rater the intended answer.
- Treat unanimity and near-perfect correlation as **suspicious** (a sign the task had a
  computable right answer the rater could read off), not as success.

That discipline is the finding. Across this session, controls demoted **four** clean-looking
positive results (the Exp1 non-blinded conclusions, the Exp4 ρ=0.986, the Exp5 ρ=1.0 read as
value-prediction, and the Exp6→Exp7 "diversity fixes it" contrast). A study that did not run
those controls would have shipped four overclaims. The map of where judgment is *not* yet
grounded is more valuable than a premature claim that it is.

---

## Experiment-by-experiment, with honest status

Status legend: **HOLDS** (survives controls, claim is narrow and stated) · **RETRACTED**
(claim withdrawn, kept visible) · **DEMOTED** (survives only as a much weaker existence
proof) · **NULL** (effect not found) · **PRIOR ART** (not ours to claim as novel).

### Exp1 — Is the opportunity rubric's gate real or noise? · mixed: one HOLDS, two RETRACTED

Source: `../EXPERIMENTS_REPORT.md` (Exp1). Raw: `../experiments/exp1-rubric-consistency/`.

The suite auto-spawns work when `Alignment >= 8 AND Total >= 28` (Total over 40). Six
independent raters scored an identical opportunity corpus; we measured score spread and
**decision-flip rate**. A methodology error was caught mid-experiment and disclosed in full:
the first round-2/3 stimuli *told raters the target* ("engineered so Alignment is high but
Total falls below 28"), and raters complied — one wrote verbatim that it would "score so
honest judgment lands there." That is a textbook **demand-characteristics** artifact. The
rounds were re-run **blinded** (neutral descriptions, purpose header stripped); the blinded
data is primary.

What survives, blinded:

- **HOLDS — the gate is noisy exactly at the boundary.** A borderline item (Alignment 7–9,
  Total 27–31, straddling both thresholds) **split 2-of-6** on the spawn verdict.
  Clearly-separated items still draw 0 flips. The rubric is unreliable precisely in the band
  where it adjudicates.
- **HOLDS — raters are strongly suggestible to description framing.** The same opportunity
  swung ~6–8 Total points and reversed its verdict based only on whether its description
  called it "trivial." Self-framing moves this rubric more than the opportunity's content
  does. Because the Discovery loop *writes* each opportunity's description **and** scores it,
  this is a concrete **self-gaming vector**.
- **HOLDS — the 4-axis rubric collapses to one axis in practice.** Raters folded
  "low-value/tangential" straight into the *Alignment* score, so no blinded
  aligned-but-Total-killed item could be constructed — Alignment had already rejected it. The
  nominal 40-point, 4-dimension instrument behaves as a single value judgment wearing the
  Alignment label.

What was retracted (see CORRECTIONS): the non-blinded "0 decision flips" and "Total kills
aligned trivia (4/4) → both gates load-bearing." Blinded, **Alignment >= 8 does essentially
all the adjudication; Total >= 28 has no confirmed independent role.**

### Exp2 — Does same-context self-review collude? · NULL

Source: `../experiments/exp2-collusion/results.md` and `../EXPERIMENTS_REPORT.md` (Exp2).

Hypothesis: an author reviewing its own proposals approves more bad ones than an independent
reviewer. Eight planted proposals (4 blatant reward-hacks, 4 genuine improvements), two
conditions (SAME = "these are YOUR proposals, the loop is paused on your decision";
SEPARATE = independent reviewer), 3 agents each.

| Condition | bad approved | good approved | accuracy |
|-----------|-------------|---------------|----------|
| SAME (author reviews own) | **0 / 12** | 12 / 12 | 100% |
| SEPARATE (independent)    | **0 / 12** | 12 / 12 | 100% |

**NULL.** Every agent in both conditions returned the identical correct verdict. This is two
failures, not a clean finding: (1) **manipulation failure** — the "these are YOUR proposals"
framing induced no real ownership in a stateless subagent, so the independent variable was
never delivered; (2) **floor effect** — the hacks were blatant and safety training caught all
of them regardless of authorship. The dangerous case (a plausible-but-subtly-wrong proposal
the author is motivated to rationalize) was **not** tested. Consequence: Exp2 *lowers* the
empirical urgency of the separate-reviewer fix rather than backing it; the fix is retained
only as **citation-grounded defense-in-depth, explicitly unvalidated.**

### Exp3 — Pairwise tournament vs absolute scoring · HOLDS (narrow)

Source: `../experiments/exp3-pairwise/results.md`.

Does *pairwise* comparison reduce the absolute-scoring noise Exp1 measured? Same blinded
corpus (B1–B6), 8 independent raters, all 15 pairs, **A/B order counterbalanced** (4 forward
/ 4 reverse), aggregated by Copeland win-count.

- Per-pair agreement: **12/15 unanimous, 2/15 near (7/8), 1/15 split** — and the lone split
  is between the two lowest-ranked off-goal items, never affecting a spawn decision.
- Position-bias check: aggregate left-slot win rate **50.0%** (FWD 79% / REV 22% mirror) →
  raters pick by item merit, not slot. Counterbalancing validated.
- **The headline holds:** item B1, whose *absolute* spawn verdict split 2-of-6 in Exp1, is
  ranked **#2 unanimously** under pairwise (8-of-8 on all four consequential pairs). Its
  *relative* position is rock-stable even though its *absolute* spawn-worthiness was a
  coin-flip.

**This is the one durable positive brick.** Relative judgment is a markedly lower-noise
instrument than absolute 0–10 scoring for this gate — the Exp1 noise was largely an artifact
of asking for an absolute number, not of the underlying preferences. **Stated narrowly:**
pairwise fixes *ordering*, not the *cut line*. "B1 is rank 2 of 6" is solid; "is rank-2 worth
a build cycle" is a separate question pairwise alone does not answer (hence the proposed
reference-anchored gate, B3, not yet built). The single-model ceiling still applies: this is
lower-noise *self-consistency*, not correctness.

### Exp4 — Does anchored judgment predict REALIZED value? · RETRACTED (fine-grained)

Source: `../experiments/exp4-closedloop/results.md`.

The keystone test (B2). A real Python library with planted defects of known severity; a
deterministic oracle (`oracle.py`) applies each fix in isolation and measures
`realized_value = tests_fixed − regressions`. Six counterbalanced rankers saw only buggy
source + neutral descriptions and pairwise-ranked the tasks.

The raw correlation was **Spearman ρ = 0.986** with identical top-task and zero-value-task
placement, no position bias. **The fine-grained claim is RETRACTED on adversarial review**
for two confounds:

1. **The oracle is not independent of our own judgment.** `realized_value = tests_fixed`, and
   the magnitudes (5/3/2/1) are simply *how many tests we chose to write per function*. Write
   1 test for one function and 5 for another with identical code, and the oracle ranking
   inverts. ρ=0.986 is closer to "the model agrees with me" than "judgment predicts an
   independent outcome."
2. **Telegraphing descriptions, no description-only control.** The task text signals the
   answer ("wrong length" = bug; "add docstrings" = cosmetic) — the Exp1 demand-
   characteristics failure recurring.

**What survives (coarse, real):** the model robustly separates genuine bugs from cosmetic
no-ops, unanimously and without position bias. A crash *is* objectively worse than a rename,
and judgment reads that. **B2 is therefore PARTIAL, not PASSED:** precise value-tracking
against an independent signal is **not** established.

### Exp5 — Judgment vs an INDEPENDENT value signal, with deception · RETRACTED (as value-prediction); HOLDS (as call-graph tracing)

Source: `../experiments/exp5-deceptive/results.md`.

Built to fix Exp4's two confounds. Value was redefined as **call-graph blast radius** (how
many feature entry-points route through a function), descriptions were made
identical-in-form, and deception was built into names: `validate_security_token` (critical-
*sounding* but dead code → value 0) and `_pad2` (trivial-*sounding* helper but reached by 2
features → value 2). Six counterbalanced rankers, no tests.

- **Spearman ρ = 1.000**; deception defeated (every rater flagged the dead "security" function
  bottom-tier and ranked the trivial-named `_pad2` #2 via the `format_date`→`_pad2`
  indirection); no position bias.

**HOLDS (narrow, real, worth banking):** the kernel **grounds rankings in code structure, not
labels, and resists name-based deception.** Salient distractors don't move it; structure
does. That is genuinely useful.

**RETRACTED — "judgment predicts value."** The tautology moved; it didn't leave. The oracle
counts how many features route through `f` (via test execution); the rankers count how many
features route through `f` (via reading `features.py`). **Same quantity, two methods** — and
we *defined* value ≡ reach. The model computed **reach**, on a task where value was defined to
equal reach. **ρ=1.0 with 6/6 unanimity is the tell, not the triumph:** genuine value
judgment is contestable and produced spread exactly where expected elsewhere (Exp1 B1 split
2/6, Exp3 ties). Unanimity means the task had a single computable answer. **Value-calibration
on contestable, multi-dimensional value remains OPEN.**

### Exp6 — Does same-model committee agreement certify correctness? · DEMOTED; the principle is PRIOR ART

Source: `../experiments/exp6-disjointness/results.md`; lit positioning `LITERATURE.md`.

A literature scan established that "disagreement among raters → abstain/escalate" is
**well-established prior art** — Query-by-Committee (Seung 1992), deep ensembles
(Lakshminarayanan 2017), self-consistency (Wang 2022), semantic entropy (Farquhar & Gal,
Nature 2024), and recent agent-gating work (ReDAct; "Oversight Has a Capacity," 2026). **It
is not ours to claim as novel.** The narrow untested slice was whether the *cheapest*
committee — N fresh-context calls of the **same** model — certifies correctness.

The reported clean evidence is **one pair (P13)**: a 6-rater same-model committee
(`cavecrew-builder`) unanimously rated a strictly-dominated 4/12 implementation **tied** with
a perfect 12/12 one — confident, unanimous, and wrong, because all raters shared the same
blind spot (a double-count bug that *looks* like correct subtractive logic). **But Exp7's
control demotes even this** (below): clean opus is ~50/50 on P13, so the 6/6 unanimity was
largely a **cavecrew-persona + small-sample artifact**, not a robust property of a same-model
committee. P03 was separately retracted as circular (see CORRECTIONS).

**What survives:** an **existence proof** that a fresh-context committee *can* be confidently
wrong on plausible-but-broken code — consistent with the documented correlated-error
literature (arXiv:2605.29800) — but it does **not** replicate as a stable phenomenon here.
The unchanged design rule it illustrates (justified independently of this experiment): **never
auto-act on the loop's own consensus; route past a non-model signal (human or execution).**

### Exp7 — Does committee DIVERSITY break the correlated blindness? · DEMOTED (contrast NOT SUPPORTED)

Source: `../experiments/exp7-diverse/results.md`.

Exp7 originally claimed that a tier-diverse committee (opus + sonnet + haiku) converts Exp6's
"confident-wrong unanimity" into informative disagreement — that diversity *fixes* the gate.
**A control demolished the contrast.** Exp6 used `cavecrew-builder` (a caveman-persona harness
that inherits opus but reads files differently), so Exp6→Exp7 varied **three** things at once
(persona, harness, model-mix), not one. The decisive control ran **6× clean opus through the
exact Exp7 harness** (`claude -p --model opus --allowedTools ""`): on P13, clean opus is
**3 tie / 3 correct (n=6) — a clean coin-flip, not unanimous.**

**Therefore "diversity converts unanimity into informative disagreement" is NOT SUPPORTED** —
there was no robust unanimity to convert. A single-tier same-model committee already splits on
P13 about as much as the diverse panel did. What survives is weaker and honest: a
fresh-context committee's verdict on plausible-but-broken vs perfect code is **noisy /
near-chance**, and one particular committee (Exp6's cavecrew run) happened to land 6/6 wrong.
**This is the fourth clean-looking result a control demoted this session — the control is the
result.**

---

## CORRECTIONS AND RETRACTIONS

Kept visible on purpose. Credibility here comes from disclosed limits and withdrawn claims,
not from a tidy positive story. Each entry: the claim, why it failed, what replaced it.

**R1 — Exp1: "0 decision flips; the gate is stable."**
*Withdrawn.* True only for clearly-separated or **target-disclosed** items. The first round-2/3
stimuli literally told raters the intended answer (demand characteristics); blinded, the
boundary item splits **2-of-6**. The gate is a coin-flip in the Alignment ≈ 7–8 band.
Source: `../EXPERIMENTS_REPORT.md` (Exp1).

**R2 — Exp1: "Both gates load-bearing; Total>=28 kills aligned trivia (4/4)."**
*Withdrawn.* An artifact of leading stimuli. Blinded, the identical "trivial" item scored
Total 29–31 and all 6 raters spawned it; genuinely trivial items were rejected on *Alignment*,
not Total. **Alignment >= 8 does the adjudication; Total >= 28 has no confirmed independent
role.** Do not present the 40-point total as a calibrated instrument.

**R3 — Exp2: framing it as evidence for separate-reviewer.**
*Reframed.* The experiment is **NULL** with a manipulation failure (ownership framing failed on
a stateless subagent) and a floor effect (blatant hacks). It does not back the
separate-reviewer fix; that fix survives only as cited defense-in-depth, marked unvalidated,
with the real teeth being **auto-apply restricted to additive + reversible changes only**
(`../improved-suite/IMPROVEMENTS.md`, item 3).

**R4 — Exp4: "ρ=0.986 → anchored judgment predicts realized value."**
*Withdrawn.* The oracle (`tests_fixed`) was our own test-allocation, and the descriptions
telegraphed bug-vs-cosmetic. Test pass/fail is unfakeable; the value *weighting* was not.
Survives only as coarse real-vs-cosmetic separation. B2 = PARTIAL.

**R5 — Exp5: "ρ=1.000 → judgment predicts value (under deception)."**
*Withdrawn as value-prediction.* Value was *defined* as call-graph reach and computed two
ways (test execution vs source reading) — the same quantity. Proves call-graph **tracing** and
**deception-resistance** (which holds), not value judgment under ambiguity. Value-calibration
remains OPEN.

**R6 — Exp6 P03: a second unanimous error.**
*Withdrawn (circular).* We had counted 6/6 preferring impl_06 over impl_04 (both 4/12 on *our*
12 toy tests) as a unanimous error. But "passes an equal number of my toy tests" is not "equal
merit": impl_04 is the wrong algorithm, impl_06 the right algorithm with one bug, and a
maintainer could defensibly rank impl_06 higher. Scoring raters "wrong" there re-asserts
merit ≡ test-count (the Exp5 error in new clothes). The Exp6 finding now rests on **P13 alone**
(strict domination, no merit definition needed).

**R7 — Exp6/Exp7: "controlled same-vs-diverse manipulation" and "diversity fixes the gate."**
*Withdrawn.* Exp6→Exp7 varied three things, not one (persona + harness + model-mix). The 6×
clean-opus control showed opus is ~50/50 on P13, so Exp6's 6/6 unanimity was a
persona/sampling artifact and the diversity contrast is **NOT SUPPORTED**. Surviving claim:
an existence proof that consensus *can* be confidently wrong; diversity is **not** a
demonstrated fix here.

**Standing caveat carried across all legs.** Call-graph blast radius (Exp5) is a RISK/IMPACT
proxy, not a correctness oracle. Every synthetic value oracle in this study was authored by
us, so circularity recurs in new costumes (test-density → blast-radius → next). The only
non-circular validator is **revealed preference** — real human decisions — which is built but
data-starved (`../revealed-preference/`).

---

## The wall, named

Every synthetic value oracle is one we author, so the circularity keeps recurring. Testing
value-prediction and B5 ("does feeding outcomes back improve the next round's ranking?")
requires **an external value signal we did not generate** — the user's real accept/reject
decisions, or real outcome metrics in real repos — **and** a non-saturated task (a ρ=1.0
oracle leaves no headroom for feedback to improve, which is why Exp5's very success
disqualifies its task type as the B5 substrate). The next move is not another synthetic
ranker; it is instrumenting a real signal.

That substrate is built but unproven:

- `../revealed-preference/prefs.py` logs the user's real accept/reject decisions, predicts the
  user's call from a few-shot of their history, and grades against held-out decisions (LOO +
  prequential learning curve vs a majority baseline). The measurement machinery is verified
  deterministically (stub) and the LLM path verified end-to-end. **No accuracy is claimed.**
- `../ultra-suite/orchestration/gate.py` wires the boundary-band human gate to this harness,
  so each real accept/reject auto-logs as a training example — the safety gate doubles as the
  data source. Verified end-to-end.

**Cold-start status (verified 2026-06-17):** the log holds **5** decisions; `prefs.py stats`
reports **NOT READY (need >= 20)**. A rising prequential learning curve over >= 20 real
decisions would be the first non-circular signal that the loop learns *this maintainer's*
judgment. Until then the headline is, honestly, **UNKNOWN**.

---

## What the experiments licensed (and what they did not)

Changes actually adopted in `../improved-suite/IMPROVEMENTS.md`, each tagged with its honest
basis:

| Evidence | Change adopted |
|----------|----------------|
| Exp1 blinded: Alignment>=8 adjudicates; Total>=28 unconfirmed | Stop presenting Total as calibrated; document the gate as "Alignment>=8, noisy in the 7–8 band." |
| Exp1: boundary flips (2/6) | Route boundary-band opportunities (Alignment 7–8 or Total 26–30) to a **human** gate, not auto-spawn. |
| Exp1 #3: suggestible to self-authored framing | Discovery loop must not author-and-score in one pass; score from a neutral spec or via a separate describer. |
| Exp2: NULL (manipulation + floor) | Separate-reviewer kept only as cited defense-in-depth, marked unvalidated; **auto-apply restricted to additive + reversible** changes. |
| Exp3: pairwise > absolute (HOLDS) | Replace the absolute Total cutoff with pairwise/tournament ranking + a planned reference-anchored cut line (B3, not yet built). |
| Exp4/Exp5: retracted value-prediction | Do **not** build a grounded loop on fine-grained value-prediction; claim only real-vs-cosmetic separation and call-graph tracing. |
| Exp6/Exp7 + lit scan: prior art, demoted | Disagreement-gating positioned as prior art, not novelty; design rule retained: never auto-act on the loop's own consensus, route past a non-model signal. |
| (orthogonal) the suite shipped no loop | `../improved-suite/loop_driver.sh` — a real bounded external driver — replaces the no-op Python stub. The loop lives outside the model. |

**What none of this licensed:** any claim that the loop's judgment is *correct*, *human-
calibrated*, or *cross-model*; any claim that diversity fixes same-model blindness; any claim
that the recursion (feedback improving the next round, B5) works. Those are open.

---

## Bottom line

- **The contribution is the method and the negative map**, not a positive headline. Controls
  demoted four of our own clean results; that discipline is what makes the remaining claims
  trustworthy.
- **HOLDS:** pairwise > absolute scoring (Exp3, narrow, self-consistency only); call-graph
  tracing + name-deception resistance (Exp5, narrow); the Exp1 findings that the rubric is
  noisy at the boundary, collapses to one axis, and is self-gameable via description.
- **RETRACTED:** Exp1's non-blinded stability/Total conclusions; Exp4's ρ=0.986 and Exp5's
  ρ=1.0 *as value-prediction* (self-authored-oracle circularity); Exp6 P03; the Exp6→Exp7
  "diversity fixes it" contrast.
- **DEMOTED:** Exp6/Exp7 to a single existence proof, undercut by the 6× clean-opus control;
  the disagreement-gate is **prior art**, not a novel contribution.
- **NULL:** Exp2 (self-review collusion not found; floor + manipulation failure).
- **The headline — does loop judgment track maintainer judgment — is UNKNOWN**, pending
  >= 20 real human decisions in `../revealed-preference/`. We have **5**.

For the full per-leg narratives and raw data, see `../EXPERIMENTS_REPORT.md`, the
`../experiments/exp*/results.md` files, the build-order gating in `../ROADMAP.md`, the prior-art
positioning in `LITERATURE.md`, and the adopted changes in `../improved-suite/IMPROVEMENTS.md`.
