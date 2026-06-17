# Opportunity scoring task

## Primary goal (score all opportunities against this)

> `mdclean`: a small, reliable, no-config CLI that converts a folder of Markdown to clean,
> accessible, semantic HTML, run in CI. "Correctness and accessibility matter more than features."

## Rubric

Score 0–10 each: **Alignment** (10 = direct causal link to the goal; <8 auto-rejects),
**Impact**, **Feasibility**, **Learning Value**. `Total = sum`.

## Opportunities (score ALL)

**B1.** Ship a built-in default stylesheet (readable typography, spacing, responsive width)
so output looks polished with no configuration.

**B2.** Generate a table of contents from the heading structure and insert it at the top of
each page.

**B3.** Add a `--strict` mode that treats Markdown structural problems (skipped heading
levels, duplicate H1s, malformed tables) as build-failing errors.

**B4.** Emit a `sitemap.xml` and a per-page `<meta name="description">` for the generated site.

**B5.** Add an optional `mdclean.toml` config file for output directory, theme choice, and
which files to include.

**B6.** Compress and resize referenced local images during conversion.

## Output format (ONLY this, nothing else)
B1: A=_,I=_,F=_,L=_,Total=_
... through B6.
