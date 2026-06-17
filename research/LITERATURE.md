# Literature scan — disagreement-gated autonomous loops (prior-art positioning)

Honest finding: the core idea is **largely prior art**. Recorded so the project never claims it as novel. Verdicts per facet: committee-disagreement=partially-done, selective-prediction=partially-done, recursive-self-improvement=genuine-gap, llm-judge=genuine-gap, agent-gating=partially-done.

## Closest prior art
- **Incoherence as Oracle-less Measure of Error in LLM Code Gen** (arXiv:2507.00057) — disagreement among independent LLM programs lower-bounds error (PAC), tracks pass@1. The INVERSE of our angle (oracle-LESS by design).
- **Cross-Model Disagreement / Cross-Model Perplexity** (arXiv:2603.25450) — independent-model disagreement for selective prediction / abstention / routing; validated on benchmarks, not a structural oracle, not in a loop.
- **ReDAct** (arXiv:2604.07036) — uncertainty-aware deferral for agent ACTION steps in loops (single-model uncertainty).
- **Oversight Has a Capacity** (arXiv:2606.08919) — selective per-action gating for a coding agent; measures inter-rater LLM disagreement (Fleiss κ=0.52).
- Foundations: Query-by-Committee (Seung 1992); Deep Ensembles (Lakshminarayanan 2017); Self-Consistency (Wang 2022); Semantic Entropy (Farquhar/Gal, Nature 2024); Selective classification (Chow 1970; Geifman & El-Yaniv 2017); 'Know Your Limits' abstention survey (2407.18418); Trust-or-Escalate / Cascaded Selective Evaluation (ICLR 2025).

## What is NOT ours to claim
Disagreement-as-uncertainty; abstain/escalate gating; independent-rater disagreement; blast-radius risk gating; disagreement→code-error. All established.

## What Exp6/Exp7 actually showed (honest — heavily demoted)
NOT new research, and weaker than first written. Exp6 observed *one* committee (cavecrew-builder =
opus + caveman persona) go 6/6 unanimous-WRONG on P13 (a strictly-dominated 4/12 impl rated tied
with a perfect 12/12). Exp7 tried to show **diversity** fixes it — but a **6×opus controlled
baseline** (clean harness) found clean opus is **~50/50 on P13, not unanimous**. So the unanimity was
a **persona/sampling artifact**, not robust same-model blindness; the diversity contrast is **not
supported**. Surviving claim: an *existence* proof that a fresh-context committee CAN be confidently
wrong on plausible-but-broken code — consistent with the established correlated-error literature
(2605.29800) — but it does not replicate as a stable phenomenon here. Three retractions logged
(P03 circular; "controlled manipulation" framing; the diversity claim). The durable lesson: controls
demoted four clean-looking results this session — that discipline is the contribution, not any ρ.

## Honest caveat carried from the scan
Call-graph blast radius (Exp5) is a RISK/IMPACT oracle, not a correctness oracle; Exp5's ρ=1.0 was circular (value≡reach, computed two ways). The only non-circular validator is revealed preference (real human decisions).
