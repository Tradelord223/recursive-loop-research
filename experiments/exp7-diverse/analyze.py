#!/usr/bin/env python3
"""Exp7 analysis: diverse-model committee vs Exp6 same-model committee, identical oracle/pairs.

Key question: does tier-diversity break the correlated blindness Exp6 found?
Clean test = P13 (impl_01=12/12 vs impl_06=4/12, strictly dominated): Exp6 same-model = 6/6 "tie"
(wrong). Does the diverse committee catch that impl_06 is broken?
"""
import json, re, glob, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
meta = json.load(open(f"{HERE}/pairs_meta.json"))
pos = json.load(open(f"{HERE}/posmap.json"))
pids = [f"P{i:02d}" for i in range(1, 16)]

# Exp6 same-model baseline (from exp6 analysis): correct-vote counts per pair, 6 raters.
EXP6 = {  # pair -> (correct_votes, note)
 "P13": (0, "6/6 said TIE — WRONG (impl_06 strictly dominated)"),
}

def parse(fp):
    d = {}
    for line in open(fp):
        m = re.match(r"\s*(P\d{2}):\s*winner=(\w+)", line)
        if m: d[m.group(1)] = m.group(2)
    return d

def tier_order(fp):
    b = os.path.basename(fp)
    _, tier, order = b.replace(".txt","").split("_")
    return tier, order

def chosen(order, pid, v):
    if v == "tie": return "tie"
    return pos[order][pid].get(v, "?")

raters = {}
for fp in sorted(glob.glob(f"{HERE}/r_*.txt")):
    tier, order = tier_order(fp)
    raters[f"{tier}_{order}"] = (order, parse(fp))

print(f"raters loaded: {list(raters)}\n")
print(f"{'pair':5}{'gap':4}{'oracleW':9} diverse-votes(correct/incorrect/tie)  spread")
for pid in pids:
    m = meta[pid]; ow = m["oracle_winner"]; gap = m["gap"]
    picks = [chosen(o, pid, d.get(pid,"?")) for o,(o2,d) in [(r[0],(r[0],r[1])) for r in raters.values()]]
    picks = [chosen(o, pid, d.get(pid,"?")) for (o,d) in raters.values()]
    c = Counter(picks)
    if gap == 0:
        correct = c["tie"]; incorrect = sum(v for k,v in c.items() if k not in ("tie","?"))
    else:
        correct = c[ow]; incorrect = sum(v for k,v in c.items() if k not in (ow,"tie","?"))
    tie = c["tie"]
    spread = round(1 - max(c.values())/sum(c.values()), 3) if sum(c.values()) else 0
    flag = ""
    if pid in EXP6:
        flag = f"   <<< Exp6 same-model: {EXP6[pid][0]}/6 correct ({EXP6[pid][1]})"
    print(f"{pid:5}{gap:<4}{ow:9} c={correct} x={incorrect} t={tie}   spread={spread}{flag}")

# P13 focus
print("\n=== P13 (the clean correlated-blindness test) ===")
p13 = [(t, chosen(o, 'P13', d.get('P13','?'))) for t,(o,d) in raters.items()]
for t, pick in p13:
    verdict = "TIE(wrong)" if pick=="tie" else ("CORRECT(impl_01)" if pick=="impl_01" else f"{pick}(wrong)")
    print(f"  {t}: {verdict}")
caught = sum(1 for _,p in p13 if p=="impl_01")
print(f"  diverse committee caught impl_01>impl_06: {caught}/6   (Exp6 same-model: 0/6)")
print("  => diversity BREAKS the blindness" if caught>3 else
      "  => diversity does NOT rescue it (shared family blind spot)" if caught<2 else
      "  => partial")
