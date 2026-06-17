# ALIGNMENT_CHECK

**Purpose**: Periodic explicit re-anchoring of all activity (Primary work, improvements, discovered opportunities) back to the immutable Original User Intent. Prevents drift in long-running recursive systems.

**Schema** (the scheduler triggers this check every N turns or at major milestones — via `/loop`, `ScheduleWakeup`, or a cron routine through `/schedule`; the model does not self-schedule):

```markdown
## Alignment Check [Date] - Turn/Milestone: [X]

**Original Sacred Intent** (restated):
- [Copy verbatim from Master Spec section 1 — immutable anchor]

**Current Primary Work**:
- What is the system currently executing?

**Recent Improvements & Opportunities**:
- List top 3-5 recent proposals (`IMPROVEMENT_PROPOSALS.md`) or queued items (`OPPORTUNITIES_QUEUE.md`).

**Alignment Assessment**:
- Do all active items still clearly serve the original intent? (Yes / Partial / No)
- Specific concerns or drift risks identified:

**Opportunity Drift Spot-Check**:
- Pick recently spawned or auto-spawned opportunities from `OPPORTUNITIES_QUEUE.md` and re-score them from their **Neutral spec** (not the original wording). Flag any where the re-score disagrees with the spawn decision — that is scoring drift or a self-gaming wording effect, and the item should be paused and re-routed (boundary band → human gate).

**Re-Alignment Actions** (if needed):
- Adjustments to scoring practice, new filters, or de-prioritization of drifting items. Note: tightening a gate is a gate-change — propose it through `IMPROVEMENT_PROPOSALS.md` under a human gate, do not silently apply.

**Confidence**:
- High / Medium / Low that the system remains well-aligned.

**Next Scheduled Check**:
- After X more turns or at next major goal completion.
```

**Usage**:
- The scheduler triggers this check automatically; the driver does not rely on the model re-prompting itself.
- If alignment drops, pause non-essential discovery and focus on re-grounding or human consultation.
- This file serves as the audit trail for long-running autonomy.
