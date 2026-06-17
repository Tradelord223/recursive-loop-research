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
