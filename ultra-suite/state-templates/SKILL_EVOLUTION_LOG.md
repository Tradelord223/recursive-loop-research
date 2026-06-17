# SKILL_EVOLUTION_LOG

**Purpose**: Track all proposed and applied changes to the core skills (RecursiveLoopEngineer, domain tunings) and Master Specifications. Enables safe, auditable self-evolution of the system itself.

**Schema**:

```markdown
## Evolution [Date] - [Skill/File Name] v[Old] → v[New or Proposed]

**Trigger**:
- Which learning pattern (`MISTAKE_LEARNING_LOG.md`) or opportunity (`OPPORTUNITIES_QUEUE.md`) drove this proposal.

**Proposed Changes**:
- Summary of diff or key modifications (attach or link full diff when possible).

**Rationale & Expected Benefit**:
- How this improves the recursive system long-term. State it qualitatively or as a testable check; do not invent metrics.

**Verification Performed**:
- Tests, manual review, or simulation done before proposal. Review must run in a SEPARATE context from the author (a distinct `claude -p` turn or subagent) — the reviewer is never the author (cited defense-in-depth; see the honesty note in `IMPROVEMENT_PROPOSALS.md` — not empirically confirmed necessary, kept because it is cheap and principled).

**Status**:
- Proposed / Human Review Pending / Applied (backup created: filename.bak-YYYYMMDD) / Rejected

**Backup Location**:
- Path to previous version.

**Impact on Running Loops**:
- None / Minor / Requires restart or state migration.
```

**Strict Rules**:
- **Every skill edit is human-gated. No exceptions.** A skill edit is never additive-reversible for auto-apply purposes (see `IMPROVEMENT_PROPOSALS.md`, Change class `skill-edit`). High self-rated confidence does NOT unlock auto-apply; there is no "high-confidence" or "low-risk" bypass.
- Never modify a live core skill file without first creating a dated backup, and isolate the edit in a git worktree so the running system is untouched until a human approves.
- All changes to `RecursiveLoopEngineer.md` or equivalent Master specs require explicit human approval before they go live.
- Destructive file operations during an edit are additionally blocked at execution time by the `safety-guard` skill.
- This log itself is versioned and backed up periodically. It is the audit trail for who changed which skill, when, and on whose approval.
