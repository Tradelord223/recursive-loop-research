# Opportunity scoring task

## Primary goal (score all opportunities against this)

> `mdclean`: a small, reliable, no-config CLI that converts a folder of Markdown to clean,
> accessible, semantic HTML, run in CI. "Correctness and accessibility matter more than features."

## Rubric

Score 0–10 each: **Alignment** (10 = direct causal link to the goal; <8 auto-rejects),
**Impact**, **Feasibility**, **Learning Value**. `Total = sum`.

## Opportunities (score ALL)

**T1.** The `--help` text says "convertt Markdown to HTML"; fix the typo to "convert".

**T2.** Add a `--version` flag that prints mdclean's version string.

**T3.** Change the parse-failure message from "bad input" to "Error: could not parse
Markdown file {path}: {reason}".

**T4.** Add a `--quiet` flag to suppress per-file progress logging during conversion.

## Output format (ONLY this, nothing else)
T1: A=_,I=_,F=_,L=_,Total=_
... through T4.
