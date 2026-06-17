# Exp4 (B2, KEYSTONE) — Does anchored judgment predict REALIZED value?

**The gate.** Everything in the self-recursive-judgment plan rests on one assumption: that the
system's *predicted* worth of a task tracks the task's *realized* value, measured by an
unfakeable signal. This experiment tests it with a real test oracle.

**Setup.**
- A real Python library (`textkit`, 6 functions) with a `unittest` suite. Four functions carry
  planted defects of calibrated, *known* severity; two are correct.
- **Deterministic oracle** (`oracle.py`): for each candidate task, apply only that fix to an
  isolated copy of the buggy repo, run the suite, measure `realized_value = tests_fixed −
  regressions`. Result: **T1=5, T2=3, T3=2, T4=1, T5=0, T6=0.** This is the ground truth; the
  rankers never see it or the tests.
- **Judgment under test:** 6 independent rankers (3 forward / 3 reversed, counterbalanced) saw
  only the **buggy source + neutral task descriptions** and pairwise-ranked all 15 pairs by
  "which task most advances a reliable library." Aggregated by Copeland.

**Result — the kernel holds.**
- **Spearman ρ = 0.986** between predicted ranking and oracle realized value.
- Predicted: **T1 > T2 > T3 > T4 > T5 > T6.** Oracle: **T1 > T2 > T3 > T4 > T5 = T6.** Identical
  order.
- Top predicted (T1) = top realized value (5 tests). Zero-value tasks (T5/T6) correctly bottomed
  by every ranker.
- 11/15 pairs unanimous; no position bias (48.8% left-slot win; fwd 95% / rev 5% mirror → pure
  content-based judgment).

**Verdict (DOWNGRADED after adversarial review — see Correction below).**
- ✅ **Solid & independent:** the model robustly separates genuine bugs from cosmetic no-ops
  (T1–T4 over T5/T6, unanimous, no position bias). A crash *is* objectively worse than a rename.
- ❌ **Retracted:** "ρ=0.986 → judgment predicts realized value." The fine-grained near-perfect
  correlation is **confounded** (below); it is NOT validation of value-prediction. B2 is
  therefore **PARTIAL**, not PASSED.

## Correction (post-review) — why ρ=0.986 is inflated

1. **The oracle is not independent of my own judgment.** Realized value = `tests_fixed`, and the
   magnitudes (5/3/2/1) are simply *how many tests I chose to write per function*. Had I written
   1 test for `parse_kv` and 5 for `normalize_ws` with identical code, the oracle ranking would
   invert. So "realized value" is a property of my test-allocation, which I set to match my own
   sense of severity. ρ=0.986 is closer to "the model agrees with me" than "judgment predicts an
   independent outcome." Test pass/fail is unfakeable; the value *weighting* is not.
2. **No description-only control + telegraphing descriptions.** The task text itself signals the
   answer ("wrong length"/"unwanted whitespace" = bug; "add docstrings"/"rename" = cosmetic). A
   ranker reading only the descriptions likely reproduces the ranking — the Exp1 demand-
   characteristics failure, recurring. I cannot claim the model predicted value *from the code*.

**Honest headline:** *judgment separates real-from-cosmetic robustly; precise value-tracking
against an independent signal is still unproven.*

## Honest limits (these are not footnotes — they bound the claim)

1. **Severity was LEGIBLE from the code.** A crashing `parse_kv` obviously beats renaming a
   variable; the rankers could read that. This proves judgment works on legible cases — a floor,
   not the ceiling. It does **not** show judgment predicts value when looks ≠ value. The decisive
   follow-up (B2.5): include a **deceptive** task — one that looks trivial but breaks many tests,
   or looks important but is worthless — and see if the correlation survives. Expect it to drop.
2. **The recursion was NOT tested.** This measured "does judgment predict value" (a correlation),
   NOT "does feeding outcomes back improve the next round" (B5 — the actual self-improvement).
   The judgment kernel is validated; the *learning loop* is still unproven.
3. **One repo, 6 tasks, one model, monotonic-by-design severities.** ρ≈0.99 is partly a product
   of an easy, clean construction. Single-model self-consistency ceiling still applies.
4. **Oracle = intrinsic severity (tests fixed), not value×achievability.** Real value includes
   whether the agent can actually do the task; not captured here.

## What this licenses
- Claim only the coarse result (real-vs-cosmetic separation). Do NOT build the grounded loop on
  fine-grained value-prediction yet — it is unproven.
- The redesigned gate (**B2.5**) must fix the confounds, in order: (1) realized value from a
  signal I did **not** hand-set — e.g. **downstream-caller / feature blast radius** set by the
  code's call graph, not by per-function test counts; (2) **identical-form neutral descriptions**
  so only the artifact carries signal; (3) **deceptive items** — one that looks trivial but has
  large blast radius, one that looks important but is dead code. If anchored judgment still tracks
  realized value when apparent-importance is decoupled from blast-radius, *that* is real evidence.
- Test/build pass-fail remains the right reward *substrate*; the open question is whether judgment
  predicts it when the artifact, not the wording, must carry the signal.
