# Evidence — provenance for every non-obvious claim in this suite

Full report: `EXPERIMENTS_REPORT.md`. Raw data: `experiments/`.

## Verified external research (real, checked June 2026)

| Claim | Source |
|-------|--------|
| The loop lives outside the model; you write loops, not prompts | Boris Cherny (Head of Claude Code): "I don't prompt Claude anymore. I have loops… My job is to write loops." |
| Real primitives: `/loop`, cron, hooks, GitHub Actions; watch token cost | Addy Osmani, *Loop Engineering* (June 2026); *Self-Improving Coding Agents* |
| 4-layer loop model (Agent / Verification / Event-Driven / Hill-Climbing) | Sydney Runkle, *The Art of Loop Engineering*, LangChain blog (2026-06-16) |
| Evaluator-optimizer = one LLM generates, another evaluates (separation) | Anthropic, *Building Effective Agents* |
| Executable loop patterns (`claude -p` chains, `continuous-claude`, RFC-DAG), "reviewer ≠ author", `SHARED_TASK_NOTES` bridge | the shipping `autonomous-loops` skill |

All four of the original v2 README citations were checked and found real and accurately
characterized. No correction was needed to the research notes — only to the engineering.

## Backed experiments (this project)

**Exp1 — opportunity rubric (6 independent raters, blinded controls).** Result: `Alignment
≥ 8` carries the gate and does nearly all adjudication; the `Total ≥ 28` cutoff is
unsubstantiated (it independently changed a verdict in 3 of 60 blinded ratings, never at
consensus); the gate is a coin-flip in the A≈7–8 band (one borderline item split 2-of-6
raters); raters reverse a verdict when the *same* item is reworded; and the four dimensions
are not scored independently. → drives the corrected `opportunity-scoring-rubric.md`
(Alignment-first, Total-as-heuristic, boundary-band-to-human, scoring-separated-from-
authoring). Two earlier conclusions were retracted after blinding — disclosed in the report.

**Exp2 — same-context vs separate-context self-review (blinded conditions).** Result: NULL —
the same-context "author reviews its own proposals" agent rejected blatant reward-hacks
(skip flaky tests, lower coverage gate, `try/except: pass`, self-skip the human gate) just
as well as an independent reviewer (0/12 bad approved in both). → the separate-reviewer
requirement is kept as **cited, principled defense-in-depth that this experiment did not
prove necessary**, never claimed as validated. The teeth the data *does* support: restrict
auto-apply to additive + reversible changes.

## Honest scope

Every experimental number above measures **one model's self-consistency** across fresh
subagent contexts — not agreement across different models or humans, and not whether the
gate's verdicts are correct in any absolute sense. Treat thresholds as defensible defaults
to tune, not as proven constants.
