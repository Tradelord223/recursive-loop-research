# AUTHORING BRIEF — Ultra Recursive Loop Suite (binding for all authors & reviewers)

You are rewriting one artifact of a Claude Code skill suite. This brief is the single
source of truth. Everything you write must be consistent with it. If you are a reviewer,
you reject any content that violates it.

The suite turns a user's goal into a **bounded, self-improving, opportunity-discovering
autonomous agent system** with three coordinated loops. The original thesis is GOOD and is
preserved. What was broken was that it was (a) not executable, (b) ungrounded in real
Claude Code primitives, and (c) full of unvalidated/false claims. This rewrite keeps the
thesis and makes every claim true and grounded. The fixes below come from real, verified
research and two backed experiments (see EVIDENCE summary at bottom).

---

## THE PRESERVED THESIS (keep this — it is the point of the suite)

Three coordinated loops over persistent file state, anchored to an immutable "Original
Intent":
1. **Primary Execution Loop** — complete the goal with strong verification.
2. **Meta-Improvement Loop** — reflect on traces/mistakes, propose concrete improvements.
3. **Opportunity Discovery Loop** — find aligned follow-on work, score it, gate it.

Plus: mandatory learning from mistakes, bounded self-expansion (compounding value, not
volume), an immutable Original Intent anchor, periodic anti-drift re-alignment, and human
gates on the risky stuff. KEEP ALL OF THIS.

---

## VERIFIED GROUND TRUTH (you may state these as fact)

**The loop lives OUTSIDE the model.** Claude Code does not autonomously re-prompt itself
across context windows. A single prompt runs one turn-loop and stops. An external driver
(shell `claude -p` chain, `/loop`, `ScheduleWakeup`, a cron routine, hooks, or GitHub
Actions) is what re-invokes the model. (Source: Boris Cherny, Head of Claude Code: "I don't
prompt Claude anymore. I have loops that are running… My job is to write loops." Addy
Osmani, "Loop Engineering," June 2026.)

**Real primitives this suite must use (do not invent others):**
| Need | Real primitive |
|------|----------------|
| Drive the loop across iterations | `claude -p` headless chain (see `orchestration/loop_driver.sh`); or `continuous-claude`; or GitHub Actions |
| Periodic Meta-Improvement / Discovery | `/loop <interval>`, `ScheduleWakeup`, or a cron routine (`/schedule`) |
| Run code at cycle boundaries (tests, state writes) | Claude Code **hooks** (PreToolUse / Stop) |
| Parallel discovery/testing/scoring | subagents (Task tool) or the `Workflow` tool |
| Isolated self-modification | git **worktrees** |
| Block destructive actions in full-auto | the shipping **`safety-guard`** skill |
| Cost ceiling + model routing | the shipping **`cost-aware-llm-pipeline`** skill + driver `--max-cost` |
| Cross-iteration context bridge | a compact `SHARED_TASK_NOTES.md` read at turn start, written at turn end |

**Shipping skills to defer to (do NOT reinvent — reference them):** `autonomous-loops`
(canonical name now `continuous-agent-loop`) for loop architectures; `safety-guard` for
destructive-action protection; `cost-aware-llm-pipeline` for budget/routing.

**LangChain 4-layer model (Runkle, 2026) — map the suite's loops to it:** Agent Loop =
Primary; Verification Loop = the checker/verification step; Event-Driven Loop = the
cron/hook/ScheduleWakeup trigger (the layer the original suite was missing); Hill-Climbing
Loop = Meta-Improvement. Anthropic's **evaluator-optimizer** pattern = *one LLM generates,
another evaluates* (separation is the defining feature). These four citations are REAL and
accurately characterized; you may cite them.

---

## MUST EMBODY (findings from the experiments — non-negotiable)

1. **Evaluator-optimizer SEPARATION.** Any review/verification of work must run in a
   SEPARATE context from the agent that produced it ("the reviewer should never be the
   author"). In practice: a distinct `claude -p` turn or a distinct subagent.
   HONESTY REQUIREMENT: label this as **cited defense-in-depth that our own experiment did
   NOT empirically confirm** (Exp2 found no collusion on blatant cases). Do not claim it is
   proven necessary. Keep it because it is cheap and principled.

2. **Auto-apply is restricted to ADDITIVE + REVERSIBLE changes only** (new tests, new files,
   pinned dependencies, new lint hooks). Anything that deletes/weakens a test, lowers a
   gate, edits a skill, or removes/bypasses a human gate → mandatory human review, NO
   "high-confidence" bypass. (A proposal of the form "skip the human gate when self-rated
   confidence is High" is a self-granted permission escalation — always HOLD.)

3. **The opportunity rubric is corrected:**
   - `Alignment >= 8` is the load-bearing gate and does essentially all the adjudication.
   - The `Total >= 28` cutoff is **a heuristic, NOT a calibrated/validated threshold** —
     present it that way. Never claim it is validated.
   - The four dimensions are **not scored independently** in practice (Alignment absorbs
     value judgments). Acknowledge this; do not pretend the 40-point total is a precise
     instrument.
   - **Boundary band → human gate:** any opportunity scoring Alignment 7–8 OR Total 26–30
     goes to a human, not auto-spawn. That band is where scoring is a coin-flip.
   - **Separate authoring from scoring:** the agent that scores an opportunity must NOT be
     the one that wrote its description (raters are strongly swayed by wording — a
     self-gaming vector since the Discovery loop both writes and scores). Score from a
     neutral one-line spec, or have a second agent re-describe first.

4. **All bounds are EXTERNAL and hard:** max iterations, max cost (USD), max duration,
   completion-signal streak. These live in the driver/scheduler, not in model "willpower."

---

## MUST NOT (banned — reviewers reject on sight)

- ❌ Any claim that one prompt launches a self-sustaining/indefinite loop, or that the
  system "runs indefinitely," or "self-loops," or re-prompts itself. The loop is external.
- ❌ Presenting `Total >= 28` (or any number) as a validated/calibrated threshold.
- ❌ "High-confidence improvements are auto-applied" when the change is destructive,
  irreversible, weakens a gate, or edits a skill.
- ❌ Claiming same-context self-review is safe, or that separation is experimentally proven.
- ❌ Fabricated metrics ("reduces false positives by ~40%") — no invented numbers.
- ❌ Reinventing cost-tracking, destructive-action guards, or loop architectures that the
  shipping skills already provide — reference them instead.
- ❌ The no-op orchestrator behavior (counting the substring "Cycle" in a file). The
  orchestrator must do something real or be explicitly deprecated in favor of the driver.

---

## STYLE & FORMAT

- Portable SKILL.md: YAML frontmatter with `name` and `description` (concise, trigger-rich),
  then the body. Bump `version`. Keep `tags` if present.
- Tight, professional, imperative. No filler, no marketing. Concrete over aspirational.
- Cross-reference sibling files by exact name (e.g., `loop_driver.sh`,
  `opportunity-scoring-rubric.md`, the `safety-guard` skill). Names must match the suite.
- Every loop you describe must name the real primitive that drives it.

## EVIDENCE (for your context; full report at ../EXPERIMENTS_REPORT.md)

- Exp1 (rubric, 6 raters, blinded): Alignment carries the gate; `Total≥28` unsubstantiated;
  coin-flip at the A≈7–8 boundary; raters reverse verdict on rewording (self-gaming vector);
  the 4 dimensions aren't independent. Two prior conclusions were retracted after blinding.
- Exp2 (self-review collusion, blinded conditions): NULL — same-context review rejected
  blatant reward-hacks as well as an independent reviewer. Separation kept on principle, not
  proof. The 4 README citations were verified real and accurate.
