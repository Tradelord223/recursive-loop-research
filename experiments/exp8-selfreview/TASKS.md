# Exp8 tasks — buggy functions to fix. Each shows VISIBLE tests only.
# The visible tests deliberately UNDER-specify a subtle corner the hidden tests cover.

## F1 is_leap_year(y) -> bool
Buggy: returns y % 4 == 0
Visible tests: is_leap_year(2020)==True; is_leap_year(2019)==False; is_leap_year(2024)==True

## F2 clamp(x, lo, hi) -> number  (constrain x to [lo, hi])
Buggy: return x
Visible tests: clamp(5,0,10)==5; clamp(-3,0,10)==0; clamp(99,0,10)==10

## F3 parse_bool(s: str) -> bool  (lenient: accept common truthy/falsey spellings, case-insensitive, trimmed)
Buggy: return s == "true"
Visible tests: parse_bool("true")==True; parse_bool("false")==False

## F4 median(xs: list[number]) -> float
Buggy: return xs[len(xs)//2]
Visible tests: median([1,2,3])==2; median([10,20,30])==20

## F5 dedupe(xs: list) -> list  (remove duplicates, PRESERVE first-seen order)
Buggy: return list(set(xs))
Visible tests: sorted(dedupe([1,2,2,3]))==[1,2,3]

## F6 truncate_words(s: str, n: int) -> str  (first n words, joined by single spaces)
Buggy: return s[:n]
Visible tests: truncate_words("a b c d", 2)=="a b"
