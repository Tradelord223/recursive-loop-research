# Exp5 (B2.5) — Judgment vs an INDEPENDENT value signal, with deliberate deception

**Why this exists.** Exp4 (B2) got ρ=0.986 but was confounded: realized value was *my own
test-allocation*, and the descriptions telegraphed bug-vs-cosmetic. Adversarial review retracted
the fine-grained claim. Exp5 fixes both confounds and adds a deception trap.

**The three fixes (per review):**
1. **Value = call-graph blast radius**, not my test counts. A small billing app: each candidate
   function is reached by a different number of feature entry-points. `realized value of fixing f`
   = feature-tests repaired = how many features route through `f`. Set by architecture, and
   discoverable *only* by tracing `features.py`. Oracle: money=3, _pad2=2, slugify=1,
   token=0, audit=0, footer=0.
2. **Identical-form neutral descriptions.** Every task is "fix the defect in function `f`." No
   wording signals importance. All six are framed as genuine defects.
3. **Deception built into the names** (anti-correlated with value):
   - `validate_security_token` — critical-*sounding*, but **dead code** (no feature calls it) → value 0.
   - `_pad2` — trivial-*sounding* internal helper, but reached by 2 features → value 2.
   A label-reader inverts these; only call-graph tracing gets them right.

**Method.** 6 independent rankers (3 fwd / 3 rev, counterbalanced) saw the full app source +
the neutral task list, **no tests**, and pairwise-ranked all 15 pairs by "which fix matters more
to the working app." Aggregated by Copeland. (3 of 90 votes dropped — one rater mis-coded the
item letter on 3 pairs; immaterial.)

**Result — kernel holds against an independent signal AND deception.**
- **Spearman ρ = 1.000** between predicted ranking and the blast-radius oracle.
- Predicted: A(money) > B(_pad2) > C(slug) > D=E=F (dead). Oracle: identical.
- **Deception defeated:** every ranker flagged `validate_security_token` as dead code → ranked it
  bottom-tier (Copeland 1.0) *despite the scary name*; and ranked `_pad2` **#2** *despite the
  trivial name*, because it traced that 2 features depend on it. No position bias (52.2%).

**Verdict (NARROWED after review — name the 20% that actually passed).**
- ✅ **Banked & real:** the kernel **grounds rankings in code structure, not labels**, and
  **resists deception** — it followed the `format_date`→`_pad2` indirection to value the
  trivial-named helper, and dismissed the scary-named `validate_security_token` as dead code.
  That is genuinely worth having: salient distractors don't move it; structure does.
- ❌ **NOT shown — "judgment predicts value."** The residual tautology moved; it didn't leave.
  The oracle counts how many features route through `f` (via test execution); the rankers count
  how many features route through `f` (via reading `features.py`). **Same quantity, two methods**
  — and I *defined* value ≡ blast radius. So the model computed **reach**, on a task where value
  was defined to equal reach. That's "the model can trace a call graph" (a unique computable
  answer), not value judgment under ambiguity.
- **ρ=1.0 with 6/6 unanimity is the tell, not the triumph.** Genuine value judgment is
  contestable — it produced spread exactly where expected before (Exp1 B1 split 2/6, Exp3 ties).
  Unanimity means the task had a *right answer each rater could compute*. Real value
  (severity × reach × user-exposure × frequency) has no single computable oracle, and good
  independent raters would legitimately disagree. Exp5 never entered that regime.

**So B2.5 passes a real but NARROW sub-claim:** structure-grounding + deception-resistance.
Value-calibration on contestable, multi-dimensional value remains **OPEN**.

## Honest limits (still binding)
1. **Scale & legibility.** 6 functions, one file, a clean traceable call graph. Real codebases
   have large, obscure graphs (dynamic dispatch, framework magic, cross-module/repo) where
   tracing is hard — judgment will likely degrade. This proves the principle on a *tractable*
   graph, not at repo scale. The next stressor: a large/obfuscated call graph.
2. **Blast radius is one proxy for value** (reach). Real value also weighs severity-given-reach,
   user exposure, and frequency — not captured.
3. **Single model, self-consistency** still applies — though the oracle is now genuinely
   independent of the rater, which is the key upgrade over Exp4.
4. **The recursion is still unproven.** This validates *judgment predicts value*. It does NOT
   test *feeding outcomes back improves the next round* (B5) — the actual self-improvement loop.

## What this licenses — and the trap it exposes for B5
- Bank the narrow win: structure-grounding + deception-resistance + (from Exp3) pairwise >
  absolute. The router (B4) and reference-anchored gate (B3) can rest on this.
- **The recurring trap, now named:** every synthetic value oracle I build, *I author* — so the
  circularity keeps reappearing in new clothes (test-density → blast-radius → whatever's next).
  The only escape from "I wrote the answer key" is an **external value signal I did not generate**:
  the user's real accept/reject decisions (revealed preference), or a real-world outcome metric
  (conversion, test-pass in *their actual* repos).
- **B5 is untestable on a saturated metric.** "Does feeding outcomes back improve next-round
  ranking?" needs headroom; if round one is already ρ=1.0 there is nothing for feedback to
  improve. Exp5's very success disqualifies its task type as the B5 substrate. **B5 must be built
  on a contestable, non-computable value signal with genuine rater spread** — i.e., an external
  signal — or it will produce another clean-but-empty ρ.
