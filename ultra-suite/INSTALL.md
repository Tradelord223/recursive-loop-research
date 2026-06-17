# Install — Ultra Recursive Loop Suite

## 1. Install the skills

Copy the three skills into your Claude Code skills directory:

```bash
cp -r skills/recursive-loop-engineer  ~/.claude/skills/
cp -r skills/loop-runner              ~/.claude/skills/
cp -r skills/coding-swe-tuning        ~/.claude/skills/
```

(Or place them in a project-local `.claude/skills/`, or upload to a Claude Project.)

## 2. Create an evolving-agent workspace

```bash
mkdir my-evolving-agent && cd my-evolving-agent
mkdir -p state loops opportunities improvements
cp /path/to/ultra-suite/state-templates/*.md state/
cp /path/to/ultra-suite/orchestration/loop_driver.sh .
cp /path/to/ultra-suite/orchestration/state_orchestrator.py .
chmod +x loop_driver.sh
```

## 3. Generate your Master Recursive Architecture

In Claude Code, invoke the `recursive-loop-engineer` skill with your detailed goal prompt.
It writes `state/MASTER_RECURSIVE_ARCH.md`.

## 4. Launch — via the EXTERNAL driver (not a magic prompt)

```bash
# bounded autonomous run: hard caps on iterations AND dollars
./loop_driver.sh --project . --max-iters 10 --max-cost 5.00
```

Requirements: the `claude` CLI on PATH and `jq`. For periodic Meta-Improvement / Discovery
instead of a continuous run, schedule it with `/loop <interval>`, `ScheduleWakeup`, or a
cron routine (`/schedule`). See `orchestration/claude-code-commands.md` for all patterns.

## 5. Run it safely (strongly recommended for full-auto)

- Enable the `safety-guard` skill: `/safety-guard guard --dir . --allow-read-all`
  (blocks destructive commands; confines writes).
- Keep self-modification in a **git worktree** until verification passes.
- Route model/budget decisions through the `cost-aware-llm-pipeline` skill.

## 6. Resume later

```
Resume from latest state in state/. Read state/SHARED_TASK_NOTES.md and state/PROGRESS.md,
determine the next action from the last recorded phase, and continue the loop.
```

## Safety defaults baked in

- All stop conditions are **external and hard**: `--max-iters`, `--max-cost`, max duration,
  completion-signal streak. The model is never trusted to stop itself.
- A **separate-context reviewer** runs each cycle (reviewer ≠ author).
- **Auto-apply is additive + reversible only.** Skill edits, destructive changes, and any
  human-gate change pause for you.
- Boundary-band opportunities (Alignment 7–8 or Total 26–30) pause for you, not auto-spawn.
