# Improvements to the Claude Recursive Loop System

Delivered as reviewable recommendations against your originals (in
`~/Downloads/claude-recursive-loop-system_extracted/`). Nothing of yours is overwritten.
Ordered by leverage. Each is tagged with its basis: **[evidence]** (an experiment in
`EXPERIMENTS_REPORT.md`), **[primitive]** (a real Claude Code feature the suite ignores),
or **[source]** (a verified citation).

---

## 1. HEADLINE — the suite is not executable; the core claim is false. **[primitive]**

> README: *"one well-crafted starter command launches the entire self-sustaining,
> evolving process … runs as a self-improving … loop structure indefinitely."*

This is false. Claude Code does **not** autonomously re-prompt itself across context
windows; a single prompt runs one turn-loop and stops. Boris Cherny (Head of Claude Code)
is explicit: *"I don't prompt Claude anymore. I have loops that are running. They're the
ones prompting Claude. My job is to write loops."* **The loop lives outside the model.**
The suite describes the loop's *contents* beautifully but never ships the loop itself —
and `orchestration/python_state_orchestrator.py` is a no-op (it counts the substring
"Cycle" in a markdown file and exits).

**Fix (shipped): `loop_driver.sh`** — a real bounded external driver using `claude -p`
(headless), a `SHARED_TASK_NOTES.md` context bridge, hard cost/iteration ceilings, a
completion-signal streak, per-cycle state backups, and a separate-context reviewer pass.
Replace the Python stub with it (or delete the stub — a no-op that looks like a guardrail
is worse than none).

**Map every loop in the spec to the real primitive that runs it:**

| Suite concept | Real primitive that actually drives it | Source |
|---|---|---|
| "single starter command, runs indefinitely" | `loop_driver.sh` / `continuous-claude` / GitHub Actions | `autonomous-loops` skill |
| periodic Meta-Improvement / Discovery | `/loop <interval>`, `ScheduleWakeup`, or a cron routine | Osmani **[source]** |
| pre/post-cycle test + state updates | Claude Code **hooks** (PreToolUse/Stop) | `autonomous-loops` |
| parallel discovery/testing sub-agents | the `Task`/subagent tool, or the `Workflow` tool | `autonomous-loops` §3,§6 |
| isolated self-modification | git **worktrees** (`using-git-worktrees` skill) | coding-swe-tuning |
| destructive-action protection in full-auto | the **`safety-guard`** skill (it already exists) | shipping skill |
| cost ceiling / model routing | the **`cost-aware-llm-pipeline`** skill + `--max-cost` | shipping skill |

## 2. Reconcile with the skills that already ship alongside it. **[primitive]**

Your environment already has `autonomous-loops` (canonical name now
`continuous-agent-loop`), `safety-guard`, and `cost-aware-llm-pipeline`. The recursive
suite reinvents weaker versions of all three. Recommended framing: **position this suite
as the *governance/“what to think about” layer* that sits on top of those execution
skills, and delegate mechanics to them** rather than re-describing them. Concretely:
- Drop the suite's hand-rolled cost language; point at `cost-aware-llm-pipeline`.
- Drop the suite's prose guardrails for destructive actions; require `safety-guard guard`
  in any full-auto run.
- Reference `autonomous-loops` for the loop architecture instead of implying the model
  self-loops.

## 3. Enforce evaluator-optimizer SEPARATION. **[source]**, honestly **[evidence]**-qualified

Anthropic's evaluator-optimizer pattern is *one LLM generates, another evaluates*; the
`autonomous-loops` skill states *"the reviewer should never be the author."* The suite's
Meta-Improvement loop violates this — the same context proposes and auto-approves its own
changes. `loop_driver.sh` fixes this with a separate `claude -p` reviewer turn each cycle.

**But report it honestly:** Exp2 tried to demonstrate the collusion failure and **could
not** (null result — modern safety training caught all blatant reward-hacks regardless of
authorship). So keep the separation as cheap, cited *defense-in-depth*, and **add a real
teeth** the experiment *does* support: restrict `auto-apply` to **additive and reversible**
changes only (new tests, new files, pinned deps). Anything that deletes a test, weakens a
gate, or edits a skill → human gate, no exceptions, no "high-confidence" bypass. (Note:
proposal P3 in Exp2 — "skip the human gate when self-confidence is High" — is a self-
granted permission escalation; the rubric/guardrails must name this as always-HOLD.)

## 4. Rubric: the `Total≥28` cutoff is unsubstantiated; `Alignment≥8` carries the gate, and it's noisy at the boundary. **[evidence]**

Exp1's *blinded* re-run (see report — the non-blinded numbers were contaminated by leading
stimuli, disclosed in full) shows:
- The adjudication is done almost entirely by **Alignment≥8**. In 60 blinded ratings, the
  `Total≥28` threshold independently killed an aligned item in only 3, never at consensus.
  I could not produce a single blinded *aligned-but-Total-killed* item — the case that would
  justify Total as a second gate.
- At the boundary the gate is a **coin-flip**: a borderline item (A 7–9, Total 27–31) drew a
  2-of-6 spawn/reject split.
- Raters are **strongly suggestible to how the opportunity is described** — the same item
  reversed its verdict when its description was reworded. Since the Discovery loop *writes*
  the description it then scores, this is a self-gaming vector.

Concrete edits to `opportunity-scoring-rubric.md`:
- Drop the precise `Total ≥ 28` claim or relabel it explicitly as a heuristic, not a
  calibrated cutoff. Lead with the Alignment gate.
- **Route the boundary band (Alignment 7–8, or Total 26–30) to a human gate** rather than
  auto-spawning — that band is exactly where the rubric can't decide reliably.
- **Separate authoring from scoring:** the agent that scores an opportunity must not be the
  one that wrote its description (score from a neutral one-line spec, or have a second agent
  re-describe first). Same evaluator-optimizer-separation principle as item 3.
- Add the caveat: *"validated only for single-model self-consistency, and only outside the
  borderline band; not cross-model or human-calibrated. Spot-check spawned items at each
  scheduled Alignment Check."*

## 5. Smaller corrections

- **Citations check out — say so.** All four README citations (Runkle's LangChain 4-layer
  model, Anthropic evaluator-optimizer, Cherny, Osmani) are real and accurately
  characterized (verified June 2026). The suite's "Research & Accuracy Notes" are honest;
  no change needed there. Osmani's *"Self-Improving Coding Agents"* post is worth adding as
  a direct reference.
- **Map the suite's 3 loops onto LangChain's 4 layers** (the cited model): Primary =
  Agent Loop; verification/checker = Verification Loop; the missing Event-Driven Loop is
  exactly the cron/hook/ScheduleWakeup trigger from item 1; Meta-Improvement = Hill-
  Climbing Loop. This makes the cited framework do real explanatory work instead of being
  name-dropped.
- **`SHARED_TASK_NOTES.md` is the cross-iteration bridge** the suite is missing. Its many
  state files assume one long context; in reality each `claude -p` turn is fresh, so a
  compact notes file read at turn-start / written at turn-end is what actually carries
  state. Add it to the state-file list.
