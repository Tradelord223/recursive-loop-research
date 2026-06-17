# Recursive Loop System — research, experiments & improvements

Self-directed work on your `claude-recursive-loop-system.zip`. Your originals were not
touched; everything here is new and reviewable.

## Start here
- **`EXPERIMENTS_REPORT.md`** — two backed experiments with raw data, run with blinded
  controls. Headline findings:
  - **Exp1 (rubric):** the `Total≥28` cutoff is unsubstantiated; `Alignment≥8` carries the
    gate, and it's a coin-flip in the A≈7–8 band (a borderline item split 2-of-6). The same
    item reverses verdict when its description is reworded — a self-gaming vector since the
    discovery loop writes *and* scores opportunities. Includes a disclosed methodology error
    (leading stimuli) and two retractions after blinded re-runs.
  - **Exp2 (self-review collusion):** NULL — same-context review did *not* rubber-stamp
    blatant bad proposals. Reported as a manipulation+floor failure, not as evidence.
- **`improved-suite/IMPROVEMENTS.md`** — concrete, leverage-ordered fixes. Headline: the
  suite isn't executable and the README's "one command → self-sustaining loop forever" is
  false; the loop must live outside the model.
- **`improved-suite/loop_driver.sh`** — a real bounded external driver (`claude -p`,
  cost/iteration caps, context bridge, separate reviewer) that replaces the no-op Python
  stub. Syntax-checked, and its cost-cap JSON contract (`total_cost_usd`) verified against a
  live `claude -p --output-format json` run.

## Layout
```
EXPERIMENTS_REPORT.md
improved-suite/
  IMPROVEMENTS.md          # recommendations vs your originals (grounded in evidence/primitives/sources)
  loop_driver.sh           # the missing real loop  (syntax-checked; needs claude CLI + jq to run)
experiments/
  exp1-rubric-consistency/
    STIMULUS_round{2,3}_blinded.md + raw_round{2,3}_blinded.csv  # PRIMARY (blinded)
    STIMULUS.md + raw_round1.csv                                  # baseline (header disclosed purpose; not fully blinded)
    STIMULUS_round{2,3}.md + raw_round{2,3}.csv                   # SUPERSEDED — leading stimuli, retained to quantify the bias
  exp2-collusion/          # PROPOSALS.md, results.md
```

## How the verdict changed from my first read
First read: "rubric thresholds are made-up; self-improvement loops drift; citations may be
fabricated." After running it: citations are real; I could not reproduce the collusion
failure; and the rubric is partly defensible but its `Total≥28` cutoff is unsubstantiated
and it's noisy at the boundary — a conclusion I only reached after catching and correcting
a leading-stimulus error in my own experiment (two retractions, all disclosed). The durable
problem is the one orthogonal to all the safety theater — **there is no loop**, just a
description of one. That's what `loop_driver.sh` fixes.
