# Exp6 — Does same-model rater agreement certify correctness? (the disagreement-gate, stress-tested)

**Origin.** A literature scan (`../../research/LITERATURE.md`) found the obvious idea — "disagreement
among raters → abstain/escalate" — is **well-established prior art** (Query-by-Committee 1992;
deep ensembles 2017; LLM self-consistency 2022; ReDAct & "Oversight Has a Capacity" 2026). It is
NOT novel. The narrow, untested slice: prior positive results use **independent/diverse** models;
a recursive loop in practice uses the cheapest committee — **N fresh-context calls of the SAME
model**. Does *that* committee's agreement certify correctness? This experiment tests it against an
unfakeable execution oracle, in the loop's pairwise-selection venue.

**Design (confounds from Exp4/Exp5 fixed).**
- Domain: `roman_to_int`. A separate agent (blind to the tests) generated a pool of 12
  implementations. A **hidden execution oracle** (12 graded tests the raters never see) scored each
  — outcome-based, *not* reach, and information the raters cannot read off. Scores: 6×correct(12),
  8,6,6,4,4,2.
- **Difficulty is oracle-MEASURED, not author-assigned** (the Exp4 fix): 15 pairs span measured
  oracle-gaps 0→10, including **3 genuine ties (gap 0)**.
- 6 raters, **reason-only** (no execution — `cavecrew-builder`, no Bash; the pilot's general-purpose
  raters with Bash just *ran* the code, collapsing the prediction task — see Methodology note).
  Counterbalanced order (3 fwd / 3 rev). They predict "which is more correct" from source + spec.
- **Pre-registered discriminator:** on small-gap pairs, does majority beat chance? And on gap-0
  ties, do raters correctly abstain or falsely distinguish?

**Result — consensus is NOT a safe correctness gate. The clean evidence is ONE pair (P13).**

- **P13 (impl_01 = 12/12, fully correct, vs impl_06 = 4/12, fails every subtractive case): all 6
  raters unanimously said "tie."** impl_06 is **strictly dominated** — no merit standard, lenient or
  strict, calls a broken implementation equal to a perfect one. Yet the same-model committee, reading
  the source, could not see impl_06's double-count bug (`if v < next: add (next−v)`, but never skips
  the consumed symbol → IX = 19) and rated it equal to impl_01. **Unanimous, confident, wrong.** This
  single pair is sufficient: zero inter-rater disagreement here certifies nothing.

**Mechanism: correlated blindness.** Same-model raters share the same blind spot ("has a
subtractive-looking branch ⇒ correct"), so they agree *because* they make the same mistake, not
because they are right. This is the cheapest-committee, worst-case instance of the well-documented
"Nine Judges, Two Effective Votes" correlated-error problem (2605.29800) — illustrated concretely
against an execution oracle, not a new phenomenon.

**P03 — RETRACTED as evidence (circularity, disclosed).** I initially counted P03 (impl_04 vs
impl_06, both 4/12 on my tests) as a second unanimous error: 6/6 preferred impl_06 on an oracle
"tie." That is the project's recurring sin in a new costume — "passes an equal number of *my* 12 toy
tests" is **not** "equal merit." impl_04 is the *wrong algorithm* (pure sum); impl_06 is the *right
algorithm with one bug*. A maintainer could defensibly rank impl_06 higher ("right idea, one fix
away") and not be blind at all. Scoring the raters "wrong" there just re-asserts merit ≡ test-count
(the Exp5 error). P03 is dropped; the finding rests on P13, which needs no merit definition — only
domination.

**Conclusion (scoped).** For a same-model fresh-context committee — the realistic, cheap loop setup —
**inter-rater agreement does not certify correctness** (P13). "Trust consensus, escalate disagreement"
would have auto-acted on P13 (unanimous, wrong). Empirical illustration justifying the suite's
existing rule: **do not auto-act on the loop's own consensus; route past a non-model signal
(human / execution).** Counterpoint to the optimistic disagreement-gating literature, which relies on
*independent/diverse* models, not a same-model committee.

## Honest limits
- **This is an illustration of a KNOWN principle, not new research.** Correlated errors in
  same-model panels are already documented (2605.29800). Exp6 demonstrates it concretely on a toy
  against an execution oracle; it does not discover it.
- Tiny: the clean claim rests on **one pair (P13)**; 15 pairs, 6 raters, ONE model, ONE toy domain.
  Existence-proof ("unanimity *can* be confidently wrong"), not an effect size.
- No spread-vs-difficulty trend is claimed: the per-bucket spreads are non-monotonic
  (0.17, 0.28, 0.06, 0, 0, 0), n=3/bucket, and the decisive failure (P13) had **zero** spread. The
  headline does not need a trend and does not assert one.
- A diverse-model committee was not tested and may behave differently (prior art suggests better).
- The oracle is correctness here (hidden execution), real but still a synthetic task I built. The
  only non-circular external signal remains the human's revealed preference
  (`../../revealed-preference/`), pending ≥20 real decisions.

## Methodology note (a finding in itself)
The pilot used general-purpose raters (with Bash). 2 of 6 **executed** the implementations over all
3999 numerals (computing the oracle directly); 3 idle-timed-out attempting it. Lesson: give a code
rater execution access and the disagreement signal is moot — it just measures ground truth. The
disagreement-gate is a *black-box / no-execution* construct; the experiment must deny execution to
test reasoning-based prediction, which the reason-only re-run did.
