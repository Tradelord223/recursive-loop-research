# Pairwise opportunity comparison

## Goal (judge every comparison against this)

> `mdclean`: a small, reliable, no-config CLI that converts a folder of Markdown to clean,
> accessible, semantic HTML, run in CI. "Correctness and accessibility matter more than features."

## The six candidate opportunities

- **B1** — Ship a built-in default stylesheet (readable typography, spacing, responsive width) so output looks polished with no configuration.
- **B2** — Generate a table of contents from the heading structure and insert it at the top of each page.
- **B3** — Add a `--strict` mode that treats Markdown structural problems (skipped heading levels, duplicate H1s, malformed tables) as build-failing errors.
- **B4** — Emit a `sitemap.xml` and a per-page `<meta name="description">` for the generated site.
- **B5** — Add an optional `mdclean.toml` config file for output directory, theme choice, and which files to include.
- **B6** — Compress and resize referenced local images during conversion.

## Your task

For EACH of the 15 pairs below, decide which single opportunity is **more worth spawning as the
next autonomous work cycle**, judged by how well it serves the goal above. Forced choice — pick
the better one. Use "tie" ONLY if they are genuinely indistinguishable in merit.

The left/right order within a pair is arbitrary and carries no meaning; judge on merit only.

Pairs:
- P01: (A) B1  vs  (B) B2
- P02: (A) B1  vs  (B) B3
- P03: (A) B1  vs  (B) B4
- P04: (A) B1  vs  (B) B5
- P05: (A) B1  vs  (B) B6
- P06: (A) B2  vs  (B) B3
- P07: (A) B2  vs  (B) B4
- P08: (A) B2  vs  (B) B5
- P09: (A) B2  vs  (B) B6
- P10: (A) B3  vs  (B) B4
- P11: (A) B3  vs  (B) B5
- P12: (A) B3  vs  (B) B6
- P13: (A) B4  vs  (B) B5
- P14: (A) B4  vs  (B) B6
- P15: (A) B5  vs  (B) B6

## Output format (ONLY this, nothing else)
Report the winner by its item label (B1..B6), not by A/B position. conf = 1 (slight), 2 (clear), 3 (decisive); for a tie write `winner=tie,conf=0`.
P01: winner=B?,conf=?
P02: winner=B?,conf=?
... through P15.
