# Exp7 — Does committee DIVERSITY break the correlated blindness?

> **VERDICT after a controlled baseline: NOT SUPPORTED. The contrast collapses.** Read the
> "Control" section first — the headline below was my initial (over)read and is retracted.

## Control (the decisive check — added after advisor review)

The advisor flagged that Exp6 (the "same-model" committee) used `cavecrew-builder` — which has **no
`model:` line, so it inherits the session model (opus)** but runs a *caveman surgical-editor persona*
and reads files, whereas Exp7's raters are clean `claude -p` with inlined source. Exp6→Exp7 varied
**three** things (persona, harness, model-mix), not one. And the within-tier data already betrayed
the confound: the two opus raters **disagreed with each other** on P13 (fwd=correct, rev=tie), as did
the two sonnet raters.

So I ran the missing control: **6× opus through the EXACT Exp7 harness** (`claude -p --model opus
--allowedTools ""`). On P13, clean opus is **exactly 3 tie / 3 correct (n=6) — a clean coin-flip,
NOT unanimous.** 

**Therefore Exp6's 6/6 unanimous-tie was largely a cavecrew-persona + small-sample artifact, not a
robust property of a same-model committee.** Clean single-tier opus already splits on P13 about as
much as the diverse panel did. **The "diversity converts unanimity into informative disagreement"
claim is not supported** — there was no robust unanimity to convert.

**What actually survives (much weaker, honest):** a fresh-context committee's verdict on a
plausible-but-broken vs perfect implementation is **noisy / near-chance** (opus ≈ 50% on P13), and
*one particular committee* (Exp6's cavecrew run) happened to land 6/6 wrong. That is an existence
proof that consensus *can* be confidently wrong — but it does **not** replicate as a stable
same-model phenomenon, and diversity is **not** a demonstrated fix. This is the 4th clean-looking
result this session that a control demoted; the control is the point.

---

## (RETRACTED original framing, kept visible)
*Below is what I wrote before the control. It overclaimed a controlled same-vs-diverse manipulation
that did not exist. Preserved for honesty; superseded by the Control section above.*

### ~~Does committee DIVERSITY break the correlated blindness? (the fix for Exp6)~~

**Question.** Exp6 found a same-model fresh-context committee fails as a correctness gate: on P13
(impl_01 = 12/12 perfect vs impl_06 = 4/12 strictly-dominated) it went **6/6 unanimous "tie" —
confidently wrong**, because all raters shared the same blind spot (impl_06's double-count bug
*looks* like correct subtractive logic). Prior art says **diverse** committees work. This re-runs
the **identical** oracle/pairs/reason-only protocol with a tier-diverse committee (opus + sonnet +
haiku, via `claude -p --model <tier> --allowedTools ""`, counterbalanced) and compares head-to-head.

**Result — diversity converts confident-wrong unanimity into informative disagreement.**

| | P13 (dominated vs perfect) | pairs unanimous | pairs split |
|---|---|---|---|
| **Exp6 same-model (6)** | **6/6 "tie" — WRONG**, zero spread | 12/15 | 3/15 |
| **Exp7 diverse (5: opus×2/sonnet×2/haiku×1)** | **3 correct / 2 tie — SPLIT** (spread 0.4) | 6/15 | 9/15 |

Two things, both the point:
1. **The false unanimity broke.** Where the same-model committee was 6/6 confidently-wrong on P13,
   the diverse committee splits 3–2. A disagreement-gate ("auto-act on consensus, escalate on
   split") therefore **flips from failing to working** on this pair: same-model → rubber-stamps the
   wrong answer; diverse → escalates it to a human. The gate's validity is **conditional on
   committee diversity**.
2. **The new disagreement is informative, not just noisier.** The diverse committee's extra splits
   concentrate on the genuinely hard/contestable pairs (the gap-0 ties, the small-gap pairs, and the
   plausible-but-broken P13) while it stays **unanimous-correct on every clear large-gap pair**
   (P06, P10, P12, P14, P15 — all 5/5 correct). That is the calibration the same-model committee
   lacked: it agreed on easy AND (wrongly) on hard.

**Mechanism.** Tier-diversity partially de-correlates the shared blind spot — different tiers don't
all miss impl_06's bug identically, so the committee surfaces the uncertainty instead of burying it
in false consensus.

**Conclusion.** Exp6 + Exp7 together are a controlled same-vs-diverse manipulation on one fixed
execution oracle: **a same-model committee's agreement does not certify correctness; tier-diversity
restores the disagreement signal the gate needs.** This both confirms Exp6's correlated-blindness
mechanism and demonstrates the (partial) fix — and it matches, with a concrete controlled demo, the
prior-art consensus that disagreement signals require independent/diverse raters.

## Honest limits
- **Partial, not a cure.** 2 of 5 diverse raters still mis-tied P13. Diversity reduced the
  correlated error; it did not eliminate it.
- **Same family.** opus/sonnet/haiku are all Claude — shared-family blind spots remain. True
  cross-vendor independence (e.g. a non-Claude rater) was NOT tested and is the real next step.
- **Tiny + imbalanced.** 5 raters (opus×2, sonnet×2, haiku×1; haiku_rev pending), 15 pairs, one toy
  domain, one synthetic (self-authored) oracle. Existence-level evidence, not an effect size.
- Still an *illustration* of the established independence-matters principle, demonstrated in the
  loop-gating venue against an execution oracle — not a new phenomenon.
- The only non-circular validator remains revealed preference (real human decisions), pending ≥20.
