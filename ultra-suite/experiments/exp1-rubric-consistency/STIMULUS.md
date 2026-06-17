# Experiment 1 — Rubric Inter-Rater Consistency

**Question under test:** The suite's Opportunity Discovery loop gates every new task on a rubric:
`Alignment >= 8 AND Total >= 28` (out of 40). These thresholds are asserted, never
calibrated. If independent raters applying the *same* rubric to the *same* opportunity
disagree enough that the auto-spawn decision flips, the threshold is noise, not a gate.

**Method:** N independent scorers (separate contexts) each score the identical opportunity
corpus below using the identical rubric. We measure, per opportunity:
- spread of Total score (max − min) across raters
- spread of Alignment score across raters
- **decision flip rate**: fraction of opportunities where raters disagree on the
  auto-spawn verdict (Alignment≥8 AND Total≥28).

A robust gate => low spread, no flips. A noisy gate => high spread, flips on borderline items.

---

## Fixed Primary Goal (the "Sacred Intent" all opportunities are scored against)

> Build and ship a small open-source CLI tool, `mdclean`, that converts a folder of
> Markdown files into clean, accessible, semantic HTML. The original user's stated intent:
> "I want a reliable, no-config tool my team can run in CI to publish our docs as
> accessible HTML. Correctness and accessibility matter more than features."

---

## The Rubric (verbatim from the suite)

Score each dimension 0–10:
1. **Alignment** — How directly it advances the core original intent. (10 = direct causal link; <8 = auto-reject)
2. **Impact** — User/business value if completed.
3. **Feasibility** — Can it be done with current tools/state in a small number of cycles.
4. **Learning Value** — How much the system itself improves by doing it.

`Total = sum`. Auto-spawn iff `Alignment >= 8 AND Total >= 28`.

---

## Opportunity Corpus (score ALL of these)

**O1 — WCAG accessibility audit pass.** Add an automated check that every generated HTML
page passes WCAG 2.1 AA (alt text required, heading order, color contrast on default theme,
landmark regions). Fail the build if violations found.

**O2 — Syntax highlighting for fenced code blocks.** Detect language on ``` fences and emit
highlighted `<pre><code>` with a bundled CSS theme.

**O3 — Live-reload dev server.** Add `mdclean serve` that watches the folder and hot-reloads
a browser preview as you edit Markdown.

**O4 — Broken-link checker.** Validate that all internal `[text](./other.md)` links resolve
to files that exist and will be converted, and that anchor links point to real headings.

**O5 — Publish a hosted SaaS dashboard.** Build a web app where users upload Markdown, we
convert server-side, and they manage doc sites with accounts and billing.

**O6 — Plugin system / extensibility API.** Design a plugin architecture so third parties can
add custom Markdown directives and output transforms.

**O7 — Golden-file regression test harness.** Add a test suite of input-Markdown →
expected-HTML golden files, run in CI, so future changes can't silently alter output.

**O8 — AI-powered "improve my writing" feature.** Integrate an LLM that rewrites the user's
Markdown prose to be clearer before converting it to HTML.
