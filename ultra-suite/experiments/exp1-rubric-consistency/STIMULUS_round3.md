# Experiment 1, Round 3 — Aligned-but-low-value items (does Total actually bind?)

Rounds 1–2 never tested the ONE configuration where the `Total>=28` threshold can decide
something the `Alignment>=8` gate cannot: an item that is clearly ON-mission (A>=8) but
low value (Impact+Feasibility+Learning small, so Total<28). That is Total's real job —
killing aligned busywork. These items are engineered for exactly that.

## Fixed Primary Goal (identical to Rounds 1–2)

> `mdclean`: a small, reliable, no-config CLI that converts a folder of Markdown to clean,
> accessible, semantic HTML, run in CI. "Correctness and accessibility matter more than features."

## Rubric (verbatim)

Score 0–10 each: **Alignment** (10=direct causal link to the tool/intent; <8 auto-rejects),
**Impact**, **Feasibility**, **Learning Value**. `Total=sum`. Auto-spawn iff `Alignment>=8 AND Total>=28`.

## Corpus — all are genuine `mdclean` work, all trivial (score ALL)

**T1 — Fix `--help` typo.** The `--help` text says "convertt Markdown to HTML". Fix the typo
to "convert". It's the actual tool, user-facing correctness, but tiny.

**T2 — Add `--version` flag.** Add a `--version` flag that prints mdclean's version string.
Standard CLI hygiene for the tool itself.

**T3 — Improve one error message.** Change the parse-failure message from "bad input" to
"Error: could not parse Markdown file {path}: {reason}". Directly improves the tool's
reliability/UX on the core conversion path.

**T4 — Add `--quiet` flag.** Add a `--quiet` flag to suppress per-file progress logging during
conversion. Minor ergonomics for CI logs.

## Output format (ONLY this, nothing else)
T1: A=_,I=_,F=_,L=_,Total=_
... through T4.
