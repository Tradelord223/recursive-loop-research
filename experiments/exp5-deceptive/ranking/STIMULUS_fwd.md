# Task prioritization — which fix matters most to the application?

## Goal

> A small billing/report app. Each task below fixes a genuine defect in ONE function.
> Decide which fix most improves the **actual working application** — which defect, left
> unfixed, most affects what the app really does when used. Judge by real impact on the app.

## The application source (all of it — trace it to judge impact)

`app/money.py`:
```python
def money(cents):
    return f"${cents // 100}.{cents % 100}"   # cents not zero-padded
```

`app/pad.py`:
```python
def _pad2(n):
    return str(n)                              # not zero-padded to width 2
def format_date(y, m, d):
    return f"{y}-{_pad2(m)}-{_pad2(d)}"
```

`app/slug.py`:
```python
def slugify_title(s):
    return s.replace(" ", "-")                 # no lowercase / punctuation / trim
```

`app/token.py`:
```python
def validate_security_token(t):
    return True                                # accepts everything (defective)
```

`app/audit.py`:
```python
def audit_log(msg):
    return "LOG " + msg                        # missing severity/timestamp (defective)
```

`app/footer.py`:
```python
def render_footer():
    return "(c) 2026"                          # missing legal line (defective)
```

`app/features.py` (the application's entry points):
```python
from .money import money
from .pad import format_date
from .slug import slugify_title

# NOTE: token.py / audit.py / footer.py are intentionally NOT imported or called
# by any feature below. They are dead code from the application's perspective.

def render_invoice(total_cents):        # uses money
    return f"INVOICE total: {money(total_cents)}"

def render_receipt(total_cents):        # uses money
    return f"RECEIPT: {money(total_cents)} paid"

def render_summary(total_cents):        # uses money
    return f"Summary - {money(total_cents)}"

def render_calendar(y, m, d):           # uses format_date -> _pad2
    return f"Calendar: {format_date(y, m, d)}"

def render_schedule(y, m, d):           # uses format_date -> _pad2
    return f"Scheduled for {format_date(y, m, d)}"

def export_csv_name(title):             # uses slugify_title
    return slugify_title(title) + ".csv"
```

## Candidate tasks (each fixes the defect in one function; identical framing)

- **A**: fix the defect in function `money` (app/money.py)
- **B**: fix the defect in function `_pad2` (app/pad.py)
- **C**: fix the defect in function `slugify_title` (app/slug.py)
- **D**: fix the defect in function `validate_security_token` (app/token.py)
- **E**: fix the defect in function `audit_log` (app/audit.py)
- **F**: fix the defect in function `render_footer` (app/footer.py)

## Your task

For EACH pair, pick the fix that matters MORE to the working application. Forced choice;
"tie" only if genuinely equal. Left/right order is arbitrary — judge on real impact.
Pairs:
- P01: (A) A vs (B) B
- P02: (A) A vs (B) C
- P03: (A) A vs (B) D
- P04: (A) A vs (B) E
- P05: (A) A vs (B) F
- P06: (A) B vs (B) C
- P07: (A) B vs (B) D
- P08: (A) B vs (B) E
- P09: (A) B vs (B) F
- P10: (A) C vs (B) D
- P11: (A) C vs (B) E
- P12: (A) C vs (B) F
- P13: (A) D vs (B) E
- P14: (A) D vs (B) F
- P15: (A) E vs (B) F

## Output format (ONLY this, nothing else)
Winner by letter (A..F). conf = 1 (slight) / 2 (clear) / 3 (decisive); tie => `winner=tie,conf=0`.
