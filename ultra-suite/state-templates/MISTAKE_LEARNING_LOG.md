# MISTAKE_LEARNING_LOG

**Purpose**: Structured capture of mistakes, bugs, verification failures, and sub-optimal decisions so the Meta-Improvement loop can turn them into concrete, testable improvements.

**Schema** (append new entries at the bottom):

```markdown
## Entry [YYYY-MM-DD HH:MM] - Cycle/Phase: [e.g. Primary-3 or Meta-Improvement]

**What Happened / Symptom**:
- Brief description of the failure or issue.

**Root Cause Analysis**:
- Why did it happen? (Prompt weakness, missing verification, context issue, tool limitation, assumption error, etc.)

**Why Verification Missed It** (if applicable):
- What should the checker/rubric/tests have caught?

**Impact**:
- Low / Medium / High on goal progress or future reliability.

**Lesson / Proposed Fix**:
- Concrete, actionable improvement (e.g., "Add rule X to RUBRIC.md", "Update executor prompt to include Y check", "Create new state field for Z").

**Status**:
- Proposed / Applied / Deferred / Rejected

**Related Files**:
- Links to traces, code, or state files.
```

**Usage Rules**:
- The system must create at least one entry after every failed verification or significant unexpected behavior.
- Meta-Improvement loop reads the latest entries and prioritizes high-impact patterns, promoting them into `IMPROVEMENT_PROPOSALS.md`.
- The `Cycle/Phase` field is an ordering label only — diagnostic metadata, not a counter to optimize. Never treat accumulating entries as progress.
- Keep entries concise but diagnostic.
