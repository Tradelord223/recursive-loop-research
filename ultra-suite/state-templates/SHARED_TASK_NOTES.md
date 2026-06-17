# SHARED_TASK_NOTES

**Purpose**: The cross-iteration context bridge. Each turn of the loop runs in a fresh `claude -p` context that remembers nothing from the previous turn. This file is what actually carries state forward. `loop_driver.sh` reads it at turn start (it is the first thing the model sees about prior work) and appends to it at turn end (the last thing the model writes before the context is discarded). If a fact is not written here or in another state file, the next turn does not know it.

**Compactness is load-bearing**: This file is injected into every turn's context. Keep it tight — rolling summary, not transcript. Prune completed items and stale notes; do not let it grow without bound. A bloated bridge wastes the budget tracked by the `cost-aware-llm-pipeline` skill and buries the signal the next turn needs.

**Schema** (a living rolling summary: append new notes under each section at turn end, then prune resolved items so the file stays compact — never an unbounded log):

```markdown
# Shared Task Notes — last updated [YYYY-MM-DD HH:MM], turn [N]

## Progress
- What is done and verified. State facts the next turn can rely on (e.g. "auth module passes its tests", "rubric heuristic confirmed at A>=8").
- Reference the verifying artifact, not the prose claim.

## Next Steps
- The single most important next action first, then the rest in order.
- Each step concrete enough that a fresh context can start it without re-deriving.

## Decisions
- Choices already made and why, so the next turn does not relitigate them.
- Anything that constrains future work (chosen library, rejected approach, agreed interface).

## Open Risks
- Known unknowns, unverified assumptions, and things that could be wrong.
- Anything routed to a human gate and still pending (see `IMPROVEMENT_PROPOSALS.md`, `SKILL_EVOLUTION_LOG.md`, `OPPORTUNITIES_QUEUE.md`).
```

**Usage Rules**:
- `loop_driver.sh` reads this file at the start of every turn and appends to it at the end. The model does not re-invoke itself; the external driver re-invokes it. This file is the only thing carrying state between those fresh turns.
- Read it first, work, then update it last. Treat the four sections as the handoff to a colleague who has zero memory of this session.
- Keep it compact: append new notes, then prune resolved or stale ones so it stays a rolling summary. Do not paste full traces, diffs, or logs — link to them in the dedicated state files instead.
- Do not record a turn counter or "cycle number" as a goal; the turn stamp is metadata for ordering only. Progress is measured by verified work in **Progress**, never by how many turns have run.
- The immutable Original Intent does NOT live here — it lives in the Master Spec and is restated during `ALIGNMENT_CHECK.md`. This file holds working state only.
