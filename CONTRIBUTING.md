# Contributing — evidence norms for this project

This is an honest, grounded research project on self-recursive judgment loops. Its
credibility does not come from impressive numbers; it comes from **disclosed limits, visible
retractions, and controls that demote our own clean-looking results before we trust them.**
Several headline findings here were downgraded, narrowed, or retracted after review — and we
kept every one visible. That track record *is* the contribution. Contributions are welcome,
but they must hold to the same discipline.

This document codifies how we keep ourselves honest. It is descriptive of what the existing
work already does, not a new standard imposed on it. Every norm below is tied to the
experiment that earned it, so the rules are grounded in evidence rather than asserted — which
is itself one of the norms (see *Claim → source provenance*).

If you are reviewing or extending an experiment, read the matching `results.md` first. The
verdicts there are deliberately hedged (PARTIAL / NARROW / OPEN / NULL / RETRACTED); do not
"round them up."

---

## The seven norms

### 1. Separate authoring from scoring

The agent (or person) that **proposes** work must not be the sole judge of whether it is good.
Route the decision through a separate context, and ultimately past a **non-model signal**
(a human, or an execution/test oracle).

- Earned by **`experiments/exp2-collusion/results.md`**. We tested whether same-context
  self-review rubber-stamps an author's own bad proposals. Result was **NULL** — same-context
  and separate-context review both caught 100% of the planted hacks (0/12 bad approvals each).
- **We did not claim this as a win.** It is reported as a **floor effect**: the planted
  proposals were *blatant* reward-hacks that model safety training catches regardless of who
  framed them. The real risk — subtle, plausible-but-wrong, author-biased proposals — was
  **not** tested and remains open. The separate-reviewer rule stands as defense against that
  untested case, not as something the experiment proved necessary.
- Practical rule: keep proposal-writing and proposal-scoring in different contexts; never let
  the loop auto-act on its own consensus (see norm 4).

### 2. Blinded controls — strip leading stimuli

Raters/reviewers must not be told the answer you expect, directly or by suggestive wording.
Item descriptions must be neutral and must not disclose the experiment's intent.

- Earned by **`experiments/exp1-rubric-consistency/`** (see `EXPERIMENTS_REPORT.md` Exp1).
  The first round-2/3 stimuli literally told raters the target ("engineered so Alignment is
  high but Total falls below 28"). Raters complied — one wrote verbatim that they would "score
  so honest judgment lands there." That was a **demand-characteristics** error in our own
  method.
- We caught it mid-experiment, **disclosed it in full**, and re-ran blinded. The blinded data
  is primary; the non-blinded data is retained only to *quantify the bias it introduced*. The
  blinded re-run **reversed two conclusions we had already written down** (see norm 5).
- The superseded leading-stimulus files are kept in-tree on purpose
  (`STIMULUS_round{2,3}.md` alongside the `_blinded` versions) — see norm 6.
- Practical rule: write neutral, identical-form item descriptions; strip any purpose header a
  rater would see; if only the wording (not the artifact) could carry the signal, the result
  is confounded.

### 3. Counterbalanced order — cancel position bias

When raters compare A vs B, half must see each pair forward and half reversed, and you must
**report the left-slot win rate** as a position-bias check.

- Earned across **`experiments/exp3-pairwise/`**, **`experiments/exp4-closedloop/`**, and
  **`experiments/exp5-deceptive/`**. Each ran raters split forward/reverse and verified the
  aggregate left-slot win rate sat near 50% (Exp3: 50.0%; Exp5: 52.2%), with a forward/reverse
  mirror confirming choices were content-based, not slot-based.
- Without this check, an apparent ranking can be an artifact of which item was shown first.
- Practical rule: counterbalance order, aggregate by a position-symmetric method (we use
  Copeland win-counts), and publish the position-bias number alongside the result.

### 4. Controls before declaring results

Run the baseline/control that could demote your finding **before** you declare it — not after a
reviewer asks. A clean-looking result with no control is a hypothesis, not a result.

This is the norm the project paid the most to learn. In the **Exp6/Exp7 session**, controls
demoted **four** clean-looking results we had written down
(`research/LITERATURE.md`; `experiments/exp7-diverse/results.md`):

1. **Exp6's same-model 6/6 unanimity, as a *robust* property** → **demoted.** A 6×opus control
   through the clean Exp7 harness showed clean opus is **~50/50 on P13 (3 tie / 3 correct), not
   unanimous.** Exp6's unanimity was largely a persona/sampling artifact
   (`cavecrew-builder` = opus + caveman persona), not robust same-model blindness.
2. **Exp7's "diversity breaks the blindness" claim** → **NOT SUPPORTED.** With no robust
   unanimity to convert, the same-vs-diverse contrast collapsed; single-tier opus already
   disagrees about as much as the diverse panel.
3. **P03 as a second unanimous-error datapoint** → **retracted.** "Passes an equal number of
   *my* toy tests" is not "equal merit"; counting the raters wrong there just re-asserts
   `merit ≡ test-count` (the recurring circularity).
4. **The Exp6→Exp7 "controlled manipulation" framing** → **retracted.** It varied *three*
   things (persona, harness, model-mix), not one — so it was never the clean single-variable
   manipulation the original write-up claimed.

**What survived** is much weaker and stated as such: an *existence proof* that a fresh-context
committee *can* be confidently wrong on plausible-but-broken code, and the unchanged design
rule (justified independently): **never auto-act on the loop's own consensus; route past a
non-model signal.** See `experiments/exp6-disjointness/results.md` and
`experiments/exp7-diverse/results.md`.

These four sit alongside — and are **distinct from** — the project's other disclosed
demotions: Exp1's two reversed conclusions (norm 5), Exp4's retracted ρ=0.986 (norm 6), Exp5's
narrowing of ρ=1.0 (norm 6), and Exp2's NULL/floor result (norm 1). Do not fold them all into
"the four"; each is its own honest accounting.

Practical rule: ask "what control would demote this?" and run it first. If a result is
unanimous and clean, treat that as a flag to look for the confound, not a trophy.

### 5. No overclaiming — claim only what the construction licenses

State the **narrowest** claim the evidence supports. If value was *defined* to equal something
the rater can compute, you proved computation, not judgment. Carry the limits in the headline,
not in a footnote.

- Earned by **`experiments/exp4-closedloop/results.md`** and
  **`experiments/exp5-deceptive/results.md`**. Exp5 hit **ρ = 1.000, 6/6 unanimous** — and we
  wrote that **"ρ=1.0 with 6/6 unanimity is the tell, not the triumph."** Because value was
  *defined* as call-graph blast radius and the raters computed reach two ways, the result
  proves **structure-grounding + deception-resistance** (a real, narrow win) — **not**
  value-judgment under ambiguity, which remains **OPEN**.
- The honest kernel status, carried everywhere:
  - **B1 ✓** pairwise > absolute scoring (Exp3).
  - **B2 PARTIAL** — judgment separates real bugs from cosmetic no-ops robustly; precise
    value-prediction against an independent signal is **not** established.
  - **B2.5 ✓ NARROW** — structure-grounding + deception-resistance only; value-calibration on
    contestable, multi-dimensional value is **OPEN**.
  - **B5 — awaiting real data.** The measurement machinery (`revealed-preference/prefs.py`) and
    the capture gate (`ultra-suite/orchestration/gate.py`) are built and verified, but **no
    accuracy is claimed** until ≥20 real human accept/reject decisions accrue.
- Practical rule: every verdict gets an explicit scope line. Words like *narrow*, *partial*,
  *open*, *null*, *existence-proof*, *one toy domain*, *single-model self-consistency* are
  features, not hedging to be edited out. See `ROADMAP.md` for the named wall (every synthetic
  value oracle is one we authored → circularity recurs; the only non-circular validator is an
  external signal we did not generate).

### 6. Disclosed retractions kept visible

When a claim is wrong, **retract it in place and leave the retraction visible.** Do not delete
the original, silently edit it away, or bury it. The retraction is evidence of the discipline
working.

- Earned by the literal patterns already in-tree:
  - **`experiments/exp7-diverse/results.md`** opens with a `VERDICT ... NOT SUPPORTED` banner,
    then preserves the original framing under a **`(RETRACTED original framing, kept visible)`**
    section with the superseded text struck through. That is the template.
  - **`experiments/exp4-closedloop/results.md`** keeps ρ=0.986 on the page with a full
    `Correction (post-review)` explaining why it is inflated, rather than deleting the number.
  - **`experiments/exp1-rubric-consistency/`** retains the superseded leading-stimulus stimuli
    (`STIMULUS_round{2,3}.md`) next to the blinded ones so the bias can be re-measured.
- Practical rule: when reviewing your own or others' work and you find an overclaim, add a
  dated/explained correction in place, downgrade the verdict, and keep the original text
  visible and clearly marked as superseded.

### 7. Claim → source provenance

Every factual or numerical claim must point to where it can be checked — a `results.md`, a raw
CSV/stimulus file, a script, or a cited paper. Claims with no traceable source do not ship.

- Earned by **`research/LITERATURE.md`**, which exists specifically so the project **never
  claims as novel** what is prior art. It records per-facet verdicts and names the closest work
  (Query-by-Committee 1992; deep ensembles 2017; self-consistency 2022; ReDAct and "Oversight
  Has a Capacity" 2026; the correlated-error result 2605.29800). The Exp6/Exp7 findings are
  explicitly framed as *illustrations of established principles*, not discoveries.
- Reinforced by the raw-data norm: experiments ship their stimuli and per-rater CSVs
  (`experiments/exp1-rubric-consistency/raw_round*_blinded.csv`, the `PAIRS_*`/`STIMULUS_*`
  files), so any number in a `results.md` can be recomputed.
- Practical rule: cite the file or paper next to the claim. Before calling something novel,
  scan `research/LITERATURE.md`; if it is prior art, say so and cite it.

---

## Submitting a contribution

Additive and reversible by default. The project's auto-apply discipline only trusts
**additive + reversible** changes; anything else is gated to a human (see `ROADMAP.md` on
safety scaling up with autonomy).

A contribution that adds or revises an experiment should:

1. **State the claim narrowly** and name the control that could demote it (norm 4).
2. **Run that control first** and report it, demotion or not.
3. **Blind the stimuli** and **counterbalance order**, reporting the position-bias number
   (norms 2–3).
4. **Keep authoring separate from scoring**, and never let a model auto-act on its own
   consensus (norm 1).
5. **Ship the raw data** (stimuli + per-rater results) so every number is recomputable
   (norm 7).
6. **Carry the limits in the verdict** — use the PARTIAL / NARROW / OPEN / NULL vocabulary
   honestly (norm 5).
7. **If you overturn a prior claim, retract it in place and keep it visible** (norm 6).

A contribution that disagrees with a finding is welcome — the strongest contribution you can
make here is a **control that demotes one of our surviving claims.** That is exactly how the
four results in norm 4 were demoted, and it is the kind of result this project most wants.

## Pointers

- `ROADMAP.md` — the build order, the keystone gate, and the named wall (authored-oracle
  circularity).
- `README.md` — how the headline verdict changed after the work was actually run.
- `EXPERIMENTS_REPORT.md` — Exp1 and Exp2 in full, with the disclosed methodology error.
- `research/LITERATURE.md` — prior-art positioning; what is **not** ours to claim.
- `improved-suite/IMPROVEMENTS.md` — the structural fix (the loop must live outside the model).
- `experiments/*/results.md` — per-experiment verdicts, limits, and retractions.
- `revealed-preference/prefs.py`, `ultra-suite/orchestration/gate.py` — the B5 substrate
  (built; awaiting real data).
