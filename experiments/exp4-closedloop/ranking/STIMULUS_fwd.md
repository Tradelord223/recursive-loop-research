# Task prioritization — which work item is most worth doing?

## Goal

> `textkit`: a small, **reliable** text-utility library. Reliability and correctness are what
> matter most — it should never crash on reasonable input, and its functions should behave
> correctly. Judge every comparison by how much the task advances *that* goal.

## Candidate tasks (and the current code of each target function)

**T1 — `parse_kv` (parse.py): make it parse key/value text correctly.**
```python
def parse_kv(text):
    result = {}
    for line in text.splitlines():
        key, value = line.split(":")
        result[key] = value
    return result
```

**T2 — `slugify` (slug.py): produce clean slugs for all inputs.**
```python
def slugify(s):
    return s.replace(" ", "-")
```

**T3 — `truncate` (truncate.py): it returns strings of the wrong length in some cases; fix it.**
```python
def truncate(s, n):
    if len(s) <= n:
        return s
    return s[:n] + "…"
```

**T4 — `normalize_ws` (normalize.py): it leaves some unwanted whitespace; fix it.**
```python
import re
def normalize_ws(s):
    return re.sub(r"\s+", " ", s)
```

**T5 — `word_count` (wordcount.py): add docstrings.**
```python
def word_count(s):
    return len(s.split())
```

**T6 — `title_case` (titlecase.py): rename the internal variable for readability.**
```python
def title_case(s):
    words = s.split()
    return " ".join(w.capitalize() for w in words)
```

## Your task

For EACH pair below, pick the single task **more worth doing** to advance the goal. Forced
choice; "tie" only if genuinely indistinguishable. Left/right order is arbitrary — judge on merit.

Pairs:
- P01: (A) T1 vs (B) T2
- P02: (A) T1 vs (B) T3
- P03: (A) T1 vs (B) T4
- P04: (A) T1 vs (B) T5
- P05: (A) T1 vs (B) T6
- P06: (A) T2 vs (B) T3
- P07: (A) T2 vs (B) T4
- P08: (A) T2 vs (B) T5
- P09: (A) T2 vs (B) T6
- P10: (A) T3 vs (B) T4
- P11: (A) T3 vs (B) T5
- P12: (A) T3 vs (B) T6
- P13: (A) T4 vs (B) T5
- P14: (A) T4 vs (B) T6
- P15: (A) T5 vs (B) T6

## Output format (ONLY this, nothing else)
Report the winner by task label (T1..T6). conf = 1 (slight) / 2 (clear) / 3 (decisive); tie => `winner=tie,conf=0`.
