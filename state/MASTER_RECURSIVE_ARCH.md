# Master Recursive Architecture Specification: Maintainer-Judgment Study (recursive-loop-research)

## 1. Original User Intent (Sacred Anchor)
An **honest, grounded study of whether an agent can learn a maintainer's judgment** — where
credibility comes from disclosed limits and retractions, not hype — packaged as a usable
bounded autonomous-loop skill suite, and published as an open-source GitHub research project.
Concretely: discover genuine candidate improvements to this project, gate each through the
human (Caiden) for a REAL accept/reject decision, accumulate ≥20 real decisions as the research
dataset, produce the prequential learning-curve result, and ship accepted additive+reversible
changes. All future work aligns here; Anti-Drift re-reads this section.

## 2. Primary Goal Completion Loop (Agent Loop)
**Driven by**: `ultra-suite/orchestration/loop_driver.sh` (headless `claude -p` chain;
`--max-iters`/`--max-cost`). Not self-triggered by the model.
- **Loop type**: discovery-and-curation over a real repo (this one), not feature-build. Each
  cycle surfaces candidate improvements and routes them to the human gate — the gate decisions
  ARE the deliverable (the dataset), accepted changes are a bonus.
- **Core cycle**: read `SHARED_TASK_NOTES.md` + this spec → identify the next slice of repo to
  examine (experiments, harness, docs, packaging, scale-stressor) → produce candidate proposals
  → score (Section 4) → enqueue gated items via `orchestration/gate.py`.
- **Minimal persistent state**: Section 5 files under `state/`.
- **Verification rubric + SEPARATE checker**: a proposal "counts" only if a distinct reviewer
  turn confirms it is (a) real (not fabricated/trivial-padding), (b) correctly classified
  additive-reversible vs gated, (c) free of reward-hack shape. Reviewer ≠ author.
- **External stop conditions**: `--max-iters`, `--max-cost`, completion-signal
  (`STUDY_BATCH_COMPLETE`) streak — all in the driver, not model judgment.
- **Pre-loaded mistake-capture (this domain's failure modes)**: (i) fabricating decisions to
  hit "20" — FORBIDDEN, decisions must be the human's; (ii) re-introducing a self-authored value
  oracle (the recurring circularity — see EXPERIMENTS_REPORT Exp4/Exp5); (iii) proposal
  descriptions that telegraph the verdict (demand characteristics, Exp1); (iv) padding the queue
  with aligned-but-trivial busywork (Total's job to kill); (v) leaking raw decision reasons into
  a publishable artifact (privacy).

## 3. Meta-Improvement Loop (Hill-Climbing Loop)
**Driven by**: the Event-Driven layer — `/loop` interval, `ScheduleWakeup`, or a Stop hook.
**Process**:
1. Load trace + `MISTAKE_LEARNING_LOG.md`.
2. Critique recent cycles: were proposals genuine? did the gate capture cleanly? is the dataset
   class-balanced enough for `prefs.py evaluate`?
3. Emit small, concrete, testable improvement proposals (e.g., add a harness unit test, a
   dataset-scrub check, a learning-curve plotter).
4. SEPARATE reviewer evaluates each + runs `prefs.py`/oracle tests.
5. Auto-apply only additive+reversible; everything else → human gate.
**Output**: `IMPROVEMENT_PROPOSALS.md`; per-cycle state backup (driver). Separation is cited
defense-in-depth, not proven (Exp2 null).

## 4. Opportunity Discovery & Expansion Loop
**Driven by**: the same Event-Driven layer.
**Process**:
1. Research/brainstorm aligned extensions (more experiments, harness hardening, packaging,
   docs, the scale-stressor follow-up).
2. For each candidate, write a **neutral one-line spec**; a **DIFFERENT agent scores it** via
   `opportunity-scoring-rubric.md` (author ≠ scorer — Exp5 self-gaming vector).
3. Gate on **Alignment**; treat any Total only as a heuristic.
4. **Boundary band (Alignment 7–8 OR Total 26–30) → human gate** via `gate.py enqueue`.
5. Clearly-above-band items may spawn (capped 2–3/run); others park in `OPPORTUNITIES_QUEUE.md`.
6. Anti-drift re-check against Section 1.
**Output**: `OPPORTUNITIES_QUEUE.md` + enqueued gate items.

## 5. Unified Persistent State Architecture
- `state/MASTER_RECURSIVE_ARCH.md` (this), `state/SHARED_TASK_NOTES.md` (cross-iteration bridge),
  `state/MISTAKE_LEARNING_LOG.md`, `state/IMPROVEMENT_PROPOSALS.md`,
  `state/OPPORTUNITIES_QUEUE.md`, `state/SKILL_EVOLUTION_LOG.md`, `state/ALIGNMENT_CHECK.md`,
  `state/GATE_QUEUE.jsonl` (pending), `state/GATE_RESOLVED.jsonl` (audit, gitignored),
  `revealed-preference/prefs_log.jsonl` (the dataset, gitignored).
- Self-modification in a git **worktree**; driver backs up `state/` each cycle.

## 6. Global Guardrails & Safety Layer (External + Hard)
- **External bounds** (driver/scheduler): `--max-iters`, `--max-cost`, max duration, completion streak.
- **Cost/routing**: `cost-aware-llm-pipeline` + `--max-cost`.
- **Destructive-action protection**: `safety-guard` required in full-auto.
- **Alignment gate**: no task without `Alignment ≥ 8` + written justification.
- **Human gates (mandatory)**: ALL accept/reject decisions (that's the dataset); skill edits;
  gate-weakening/test-deleting changes; boundary-band items; **`git push` (never without human)**;
  publishing the dataset (privacy scrub first).
- **Anti-drift**: every N cycles re-align to Section 1; spot-check.
- **Test-driven**: SEPARATE reviewer verifies before anything counts.

## 7. Self-Recursion & Skill Evolution Protocol
Loop designs and the suite's skills are improvable artifacts via the same Meta-Improvement +
separate-reviewer + test path. Skill edits are never auto-applied — always human-gated, logged
in `SKILL_EVOLUTION_LOG.md`.

## 8. Master Execution Instructions (Launched and Re-Invoked EXTERNALLY)
- **Discovery batch (now)**: a bounded discovery pass generates candidate proposals and enqueues
  gated ones (`gate.py enqueue`). No model self-looping.
- **Human decision session**: `python3 ultra-suite/orchestration/gate.py --project . review --suggest
  --prefs revealed-preference/prefs.py` → Caiden decides → auto-logs to `prefs.py`.
- **Repeat** across sessions until `prefs.py stats` shows ≥20 real decisions, then
  `prefs.py evaluate --mode prequential` → the learning-curve result.
- **Ship**: accepted additive+reversible items become commits/PRs (`github` skill; no push without human).
- Each turn reads `SHARED_TASK_NOTES.md` at start, appends at end.

## 9. Notes on Risks Mitigated & Honest Limits
- Original-Intent anchor + Alignment gate + external caps + human gates keep expansion to value.
- Separation is cited defense-in-depth; Exp2 did NOT confirm collusion. No fabricated metrics.
- The rubric is one-model-consistent, not human-calibrated, noisy at the boundary → boundary-band
  human gate. The maintainer-judgment result itself is UNKNOWN until ≥20 real decisions exist;
  this spec sets up the honest measurement, it does not presuppose the outcome.
