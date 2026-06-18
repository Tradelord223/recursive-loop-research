# Changelog — progress toward a grounded self-recursive judgment system

Datestamped log of real progress. New milestones are appended here (and reflected on the
[live site](https://tradelord223.github.io/recursive-loop-research/) and README) as the work
advances. Honest by rule: retractions and nulls are logged alongside wins.

Build-order reference (see `ROADMAP.md`): B1 pairwise ✓ · B2/B2.5 value-prediction (narrow) ·
B3 reference gate · B4 router (prototyped) · **B9 real-repo escape ✓** · B5 recursion (in progress).

---

## 2026-06-18

- **Exp9 — the escape from the circularity wall (milestone).** Real-repo outcome harness
  (SWE-bench-lite on `python-semver`): fix real bugs, graded by the library's own held-out test
  suite. Reward-hack guard **fired on a live attempt**. **1/3 real bugs fixed** — the first
  non-circular result; cannot be demoted by a control because it *is* the control.
- **Exp6 + Exp7 — demoted by control.** "Same-model blind consensus" + "diversity fixes it" both
  collapsed under a 6×opus baseline (the unanimity was a persona/sampling artifact).
- **Exp8 — robust floor.** Self-review on subtly-wrong fixes: 0 genuine wrong fixes in 54;
  the lone apparent exception was a bug in my own oracle, caught in analysis (5th such error).
- **B5 (recursion) — at-scale run COMPLETE: no feedback benefit (honest null).** Feedback-vs-control
  retry on real semver tasks (robust Python orchestrator). attempt#1 fixed **2/4** tasks first try;
  on the 2 failures, retry with the real failure fed back scored **0/6**, plain-resample control
  **1/6** — feedback did NOT beat control (control edged it). Underpowered (2 tasks × 6 samples,
  one feedback sample a patch-apply error), but the direction is clear: **outcome-feedback did not
  improve the retry here.** The actual self-recursion remains undemonstrated; a powered test needs
  many more tasks across libraries (`mine_tasks.py` ready). Fix-capability (Exp9) stands; recursion
  does not — logged straight.
- **Literature scan** — disagreement-gating is prior art (QBC 1992 → ReDAct/Oversight 2026); not
  claimed novel.
- **Shipped:** public GitHub repo + green CI, issue templates, skills bumped to v3.1.0/2.1.0/2.1.0,
  live GitHub Pages site + bespoke artwork.

## 2026-06-17

- **Suite v3 grounded + installed.** 3 skills (recursive-loop-engineer, loop-runner,
  coding-swe-tuning) rebuilt on real Claude Code primitives; the "one prompt runs forever" claim
  removed; real `loop_driver.sh` replaces the no-op orchestrator.
- **Exp1–3.** Rubric gate (Total≥28 unsubstantiated; alignment carries it; 2 retractions after
  blinding) · self-review collusion (null) · **pairwise > absolute scoring (holds).**
- **Exp4–5 — retracted.** Two near-perfect correlations (ρ=0.986, ρ=1.0), both retracted for
  self-authored-oracle circularity.
- **Revealed-preference harness + human gate wiring.** The one non-circular path to the maintainer-
  judgment question; the gate doubles as the training-data source. (Still awaiting ≥20 real
  decisions; currently n=5.)
- **Autonomous cycle.** The loop judged 20 proposals (17 accept / 3 reject) and implemented +
  test-verified 12 — each earning an unfakeable check.
