# PROGRESS — recursive-loop-research (living dashboard)

_Updated by loop-runner each major phase. Original Intent: an honest, grounded study of whether
an agent can learn a maintainer's judgment; credibility from disclosed limits, not hype._

## Current phase
**BLOCKED at human gate** — awaiting Caiden's accept/reject decisions (the dataset signal). The
next loop step (B5 prequential measurement) cannot run until ≥20 real decisions exist. Decisions
must be the maintainer's; auto-deciding them is forbidden (Master spec §2 — it would rebuild the
circularity the whole study exists to escape).

## Primary status
- Master spec ✓ · workspace/git/LICENSE ✓ · discovery batch (25 scored, author≠scorer) ✓
- Human-gate dataset: **5 / 20 decisions** logged (`prefs.py stats`: 3 reject / 2 accept).
- 20 candidates pending at the gate (`state/GATE_QUEUE.jsonl`).

## Recent learnings (durable, incl. retractions)
- Exp3: pairwise > absolute scoring (lower noise). Holds.
- Exp4 (ρ=0.986) / Exp5 (ρ=1.0): **retracted** — self-authored-oracle circularity.
- Exp6/Exp7: tested same-model "blind unanimity" + "diversity fixes it" → **both demoted by a
  6×opus control** (clean opus ~50/50 on P13; Exp6's 6/6 was a cavecrew-persona/sampling artifact).
  Surviving: existence proof only. 4 controls demoted 4 clean-looking results this session.
- Lit scan: the disagreement-gate idea is **prior art**; not claimed as novel.

## Queued opportunities
- 20 pending (research / harness / oss / docs / mixed). Scores in `state/OPPORTUNITIES_QUEUE.md`
  (model suggestions, hidden from decision time).

## Resource / safety
- External caps unused this turn (no driver run). No git push (human-gated). 4 files uncommitted
  (Exp6/Exp7 + research/ — awaiting human commit decision).

## Next action (for the next invocation)
Caiden decides ≥15 of the 20 pending → cross n=20 → `prefs.py evaluate --mode prequential` →
the first non-circular result. Accepted additive+reversible items → commits/PRs (no push w/o human).
