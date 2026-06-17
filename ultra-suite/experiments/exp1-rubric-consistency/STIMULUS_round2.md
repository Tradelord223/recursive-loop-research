# Experiment 1, Round 2 — Borderline opportunities (threshold stress test)

Round 1 showed the rubric is consistent on obvious items. But the gate `Alignment>=8 AND
Total>=28` only *decides* anything for items near the boundary. Round 2 uses opportunities
deliberately engineered to sit near Alignment≈7–8 and Total≈26–30, where one rater's +/-1
flips the auto-spawn verdict. If verdicts flip here, the threshold is noise where it is used.

## Fixed Primary Goal (identical to Round 1)

> Build and ship a small open-source CLI tool, `mdclean`, that converts a folder of Markdown
> files into clean, accessible, semantic HTML. Original user intent: "I want a reliable,
> no-config tool my team can run in CI to publish our docs as accessible HTML. Correctness
> and accessibility matter more than features."

## Rubric (verbatim)

Score 0–10 each: **Alignment** (10=direct causal link; <8 auto-rejects), **Impact**,
**Feasibility**, **Learning Value**. `Total = sum`. Auto-spawn iff `Alignment>=8 AND Total>=28`.

## Borderline Corpus (score ALL)

**B1 — Default CSS theme.** Ship a built-in default stylesheet (readable typography, spacing,
responsive width) so output looks polished with zero config. Affects "clean" but not
correctness or accessibility per se.

**B2 — Auto table-of-contents.** Generate a TOC from the heading structure and insert it at
the top of each page. A common docs feature.

**B3 — `--strict` lint mode.** Treat Markdown structural problems (skipped heading levels,
duplicate H1s, malformed tables) as build-failing errors. Correctness-adjacent, helps
accessibility (heading order), but is a new opinionated behavior.

**B4 — Sitemap + meta descriptions.** Emit `sitemap.xml` and a `<meta name="description">`
per page for the generated site. Publishing/SEO value, not correctness/accessibility.

**B5 — Config file support.** Add an optional `mdclean.toml` for output dir, theme, and file
globs. Users expect configurability — but the stated intent says "no-config."

**B6 — Image optimization.** Compress and resize referenced local images during conversion to
speed up the published site. Tangential to the core conversion job.

## Output format (ONLY this, nothing else)
B1: A=_,I=_,F=_,L=_,Total=_
... through B6.
