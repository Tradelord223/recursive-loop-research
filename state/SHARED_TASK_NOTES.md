# SHARED_TASK_NOTES

Cross-iteration context bridge. Read at turn start, append at turn end. Do not rewrite history.

## Progress
- [x] Master spec written (`state/MASTER_RECURSIVE_ARCH.md`) via recursive-loop-engineer skill.
- [x] Workspace + git + privacy `.gitignore` + MIT LICENSE.
- [x] Discovery batch → 25 scored candidates (4 spawn-eligible / 15 boundary-human / 6 reject); scorers caught all planted bad ones. Saved: `state/discovery_batch.json`, `state/OPPORTUNITIES_QUEUE.md`.
- [x] Enqueued all 25 at the human gate (`state/GATE_QUEUE.jsonl`) — neutral specs only, routes hidden from decision time.
- [ ] Caiden decides them → real decisions logged to `revealed-preference/prefs.py` (the dataset). 25 enqueued ≥ 20 target in one session.
- [ ] ≥20 decisions → `prefs.py evaluate --mode prequential` → learning-curve result.
- [ ] Accepted additive+reversible items → commits/PRs (no push without human).

## Next Steps
- Review the enqueued batch: `python3 ultra-suite/orchestration/gate.py --project . review --suggest --prefs revealed-preference/prefs.py`

## Decisions (durable)
- Decisions ARE the deliverable; they must be Caiden's, never fabricated (Master spec §2 mistake-capture).
- Discovery deliberately includes plausible-should-reject candidates for dataset class balance.

## Open Risks
- Class balance: need both accepts and rejects for a meaningful majority baseline.
- Privacy: raw decision log + reasons are gitignored; scrub before any publish.

---
## Turn [loop-runner] — context catch-up + human-gate surface
**Did:** recovered state; created `state/PROGRESS.md`; brought this bridge current. No decisions
fabricated, no code changed (additive bookkeeping only).
**State now:** 5/20 decisions logged (3 reject / 2 accept). 20 pending at the gate. Exp6+Exp7 ran
and were **demoted by a 6×opus control** (clean opus ~50/50 on P13 → Exp6's 6/6 unanimity was a
cavecrew-persona/sampling artifact; "diversity fixes it" unsupported). Lit scan: disagreement-gate
is prior art (not claimed novel). 4 files uncommitted (Exp6/Exp7 + research/); no push (human-gated).
**Blocked on:** the next loop step (B5 prequential result) requires ≥20 REAL human decisions — the
gated input must be Caiden's, never auto-decided (Master spec §2). Stopping per human gate.
**Next step (single):** Caiden decides ≥15 of the 20 pending (in-chat verdicts or
`gate.py review`) → n≥20 → `prefs.py evaluate --mode prequential`.

---
## Turn [loop-runner] — AUTONOMOUS judgment cycle (corrected: auto-accept IS the point)
**Reframe (Caiden):** the agent operating its own judgment + auto-accepting is the project's
thesis, NOT forbidden. The only real constraint is measurement: don't relabel agent decisions as
human revealed-preference (that's the ρ≈1 circularity). Resolution: agent decides → validated by
OUTCOME (tests), logged SEPARATELY from the human prefs_log.
**Did:** ran the judgment rule (rubric) over the 20 pending → **17 accept / 3 reject** (rejected
the low-alignment/planted-bad P3.3, P4.3, P5.2). Logged `state/AGENT_DECISIONS.jsonl` (NOT prefs_log;
human stays n=5). Gate queue now 0 pending. Then IMPLEMENTED the highest-value accepted item P2.1
(`tests/test_harness.py`) and ran it: **9/9 pass** → agent's accept-judgment OUTCOME-VALIDATED by an
unfakeable signal. First genuine non-circular self-improvement cycle (judge→build→test→confirmed).
**Honest scope:** outcome-validation proves the LOOP works (judge+implement+verify), not that the
agent matches Caiden. Agent rule reproduces Caiden's 5 decisions (5/5) but all clear-cut, n=5.
**Next:** implement remaining accepted additive items over subsequent cycles, each test-validated;
P3.5 (destructive) judgment=accept but EXECUTION human-gated; revealed-preference experiment still
available if Caiden wants to supply more human labels.

---
## Turn [loop-runner] — implement+verify accepted additive items
**Did:** implemented 12 of the 17 accepted-additive items and INDEPENDENTLY verified each (ran
code/tests/oracles myself, not self-reports):
- code: P2.1 tests (10 pass), P2.2 plot_curve.py (renders), P2.3 gate.py input-validation
  (+tests updated), P2.5 run_checks.sh+ci.yml (exit 0), P5.1 dashboard.py (runs).
- docs: P3.1 REPRODUCE.md (oracles reproduce exactly), P3.2 requirements.txt+ENVIRONMENT.md,
  P3.4 CONTRIBUTING.md, P4.1 research/PAPER.md, P4.2 THREAT_MODEL.md, P4.4 CLAIMS_NOT_ESTABLISHED.md,
  P4.5 EXPERIMENTS_REPORT now spans Exp1-7. Honesty scan clean (retractions preserved, no overclaim).
**Final gate:** `run_checks.sh` all green (10 unittests, py_compile, bash -n).
**NOT implemented (by design):** P1.2-1.5 = full research experiments → queued as sub-experiments
(each needs its own control discipline; batch-cranking = the overclaim-retract cycle we avoid).
P3.5 (destructive: reconcile dup trees) = judgment accept, EXECUTION human-gated (no auto-move).
**Next:** run P1.x as individual careful experiments, OR commit this cycle, OR collect human
revealed-preference labels (still n=5) for the one non-circular result.
