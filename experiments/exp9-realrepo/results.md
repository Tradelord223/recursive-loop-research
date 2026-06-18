# Exp9 — Real-repo outcome harness: the escape from the circularity wall

**Why this matters.** Every prior leg hit the same wall: any oracle *I* authored was circular
(Exp4 ρ=0.986, Exp5 ρ=1.0 retracted), a persona/sampling artifact (Exp6/7 demoted), or a floor
(Exp8). Exp9 uses a signal I did **not** generate and **cannot** fake: a real OSS library's own
pre-existing test suite. The verdict here is reality's, not mine — so it cannot be demoted by a
control, because **it is the control.**

**Design (SWE-bench-lite, held-out grading).** Library: `python-semver` (500 commits, 333-test
suite I did not write). For each real historical bugfix commit:
1. Worktree at the parent commit — **buggy source, regression test absent.**
2. The fixer (a `claude -p` sonnet agent, `Read`/`Edit` only) fixes the bug **from a description
   only — it never sees the grading test** (held out; this defeats the source-hardcode hack the
   advisor flagged: you can't hardcode an assertion you can't read).
3. **Reward-hack guards:** auto-FAIL if the fix diff touches any test file; must pass the *full*
   suite (no skip/delete/`try:pass`); worktree-isolated.
4. **Grade:** apply the commit's real regression test (held out) + run all 333+ tests. PASS iff
   the regression is fixed AND zero regressions.

**Validation (before any agent ran):** without a fix the regression test fails with the real
error; with the commit's gold fix it passes. Harness sound + non-circular.

**Result — 1 / 3 real bugs fixed (sonnet fixer, n=3):**

| Commit | Bug | Verdict | Note |
|--------|-----|---------|------|
| bc41390 | subclass comparator rejects valid type | **FAIL** | plausible fix (`isinstance(other, Version)`); semver's own test rejected it (1 failed/328 passed) |
| 4b03f86 | derived version loses subclass type | **PASS** | `return type(self)(**version)` — regression fixed, 0 regressions |
| d8813b6 | bump_prerelease not strictly newer (64-line fix) | **FAIL** | hard; 6 tests failed |

No reward-hack guard ever fired (all three edited only source). The bc41390 FAIL is the signal
working as intended: the model produced a confident, plausible-looking fix and **reality caught
that it was wrong** — exactly what no self-authored oracle this session could do.

## Honest scope (pre-registered, per advisor)
- This measures **fix capability** — can the loop produce a change reality accepts. It is **NOT**:
  judgment / value-prediction (Exp1/3/4/5), the consensus question (Exp6/7), the **recursion**
  (B5: does feeding the FAIL outcome back improve a retry? — untested), or the **maintainer-
  judgment** question (still revealed preference, n=5). Do not let 1/3 be read as validating any
  of those.
- n=3, one library, one model, author-chosen bugs. This is **harness validation + an existence
  result** (the loop fixes *some* real bugs; reality rejects the rest), not an effect size or a
  benchmark score.
- Difficulty was set by my commit choice. Fine for a capability test; the moment ranking is
  layered on for B5, difficulty must fall out of the measured outcome (else the Exp4 confound
  returns).

## What this unlocks
The kernel the ROADMAP marked **"BUILD HERE."** With a real unfakeable reward in hand, the next
genuinely-new move is **B5**: feed the FAIL verdict (and the failing-test output) back to the
fixer for a second attempt, and measure whether the outcome signal *improves* the next round —
the actual self-recursion, grounded in reality rather than self-agreement. That is the first time
in this project the recursion can be tested without circularity.

---

## B5 (first cut) — does feeding the real failure back improve the retry? — INCONCLUSIVE / underpowered

The recursion test, now possible without circularity. Design: for each FAILED task, attempt #2 in
two arms — **feedback** (given the failing-test symptom: name + error line, NOT the test source) vs
**control** (fresh resample, bug description only). Recursion works iff feedback beats control.

**Result (complete first cut, 2 tasks × 2 arms = 4) — feedback did NOT beat control: 0/4 pass.**
- `bc41390`: **feedback = FAIL, control = FAIL** (both 1-failed, identical to attempt #1). Even with
  a pointed hint ("the comparator hardcodes the base Version type"), sonnet's retry kept editing the
  wrong line. Feedback did not rescue it.
- `d8813b6` (hard 64-line bug): **feedback = FAIL** (5 failed); **control = AUTO-FAIL** — the
  control-arm fixer **edited a test file**, and the reward-hack guard caught it. (Bonus validation:
  the guard fired on a real reward-hack attempt, exactly as designed.)

**Honest status:** the closed loop (real fail → feedback → retry → real grade) is **built and runs**,
and the reward-hack guard demonstrably works on a live attempt — that apparatus is the milestone.
But the result is **0/4 with feedback not beating control** on n=2 tasks × 1 sample/arm — far too
small to conclude, and what little there is shows **no recursion benefit**. A real B5 needs many
tasks, several samples/arm, robust (non-bash) orchestration, and held-out feedback. Claimed as
"the apparatus exists + the guard works; first cut shows no feedback benefit" — NOT a recursion win.

---

## B5 AT SCALE (complete) — recursion test, robust orchestrator — NO feedback benefit

Re-ran B5 with a robust Python orchestrator (`b5_scale.py`: unique temp worktrees, held-out
grading, reward-hack guard, real commit-subject descriptions, feedback = failing-test names +
error type only). 4 validated semver tasks; the model's OWN attempt-#1 failures form the retry
set (difficulty falls out of outcomes, not selection).

**Result:**
- attempt #1: **2/4** fixed first try (4b03f86, f8a182f PASS; d8813b6, bc41390 FAIL).
- retry on the 2 failures, K=3 samples/arm: **FEEDBACK 0/6 pass · CONTROL 1/6 pass.**
- **Recursion signal: none** — feedback ≤ control (control actually edged it). One feedback sample
  was an APPLYFAIL (patch didn't apply cleanly).

**Honest conclusion:** at this scale, feeding the real failure back did **not** improve the retry;
plain resampling did at least as well. Underpowered (2 failed tasks × 6 samples) — it cannot
detect a small effect, but there is no large one. The closed loop and reward-hack guard work
(Exp9); the *recursion benefit* is **not demonstrated**. A powered test needs many more tasks
across libraries — the apparatus (`mine_tasks.py`, `b5_scale.py`) is built and ready.
