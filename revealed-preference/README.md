# Revealed-Preference Harness

The first **non-circular** brick of the self-recursive judgment system. Every prior experiment
scored proposals against a value signal *I authored* (a rubric, test counts, call-graph reach) —
so "judgment predicts value" kept collapsing into "the model agrees with my answer key." This
harness removes me from the loop: it learns to predict **your real accept/reject decisions**,
and grades itself against **your own held-out decisions**. The ground truth is external.

## Why this is the honest next step

- Exp3: pairwise beats absolute scoring (lower noise). ✅
- Exp5: judgment grounds in code structure, resists label-deception — but only proved
  call-graph *tracing*, because I defined value ≡ reach (a computable answer). ρ=1.0 was the tell.
- The wall: I cannot test *value judgment under ambiguity* with any oracle I write. The escape is
  a value signal I did not generate — **your decisions.** That is what this logs and learns.

## Commands

```bash
# 1) Capture a real decision (do this every time you accept/reject a proposal)
python3 prefs.py log --proposal "Add a golden-file test for HTML output" --decision accept \
    --reason "additive, reversible, real regression cover" --context "mdclean"

# 2) See where you stand
python3 prefs.py stats          # count, class balance, majority baseline, eval readiness

# 3) Predict your decision on a new proposal (uses your history as few-shot)
python3 prefs.py predict --proposal "Lower the coverage gate to 50%" --context "mdclean"

# 4) Measure how well it predicts YOU (once you have real data)
python3 prefs.py evaluate --mode prequential   # learning curve: does more history help?
python3 prefs.py evaluate --mode loo           # leave-one-out accuracy vs majority baseline
```

## What it measures (and the baseline that keeps it honest)

- **LOO accuracy** — hide one decision, predict it from the rest, compare to your real call.
- **Prequential accuracy + learning curve** — process decisions in time order, predict each from
  ONLY prior ones, report accuracy across early→late buckets. **A rising curve is the real B5
  signal**: more of *your* history → better prediction = the system actually learning your
  judgment. It cannot saturate (early predictions are uninformed), so unlike the synthetic ρ=1.0
  oracles it has room to show learning.
- **Majority-class baseline** — beating it is the bar. Matching it means the model learned only
  your accept/reject ratio, not your *preferences*.

## Cold-start honesty (read this)

- With 0 decisions it predicts nothing useful, and `stats` says NOT READY.
- Rule of thumb: **≥ 20 real decisions** before any accuracy number is worth reading; a learning
  curve wants more. Log them as you actually work — don't batch-fabricate, that rebuilds the
  circularity this exists to escape.
- The `stub` predictor (predict-the-majority) exists only to unit-test the eval math with no LLM
  and no cost. It is **not** a judgment; never report a stub number as a result.

## Wiring it to the loop (BUILT — `ultra-suite/orchestration/gate.py`)

The boundary-band human gate is now wired to this harness, so capture is automatic:

```bash
# headless loop hits a gate -> parks the proposal (action_router.sh escalate calls this):
python3 gate.py --project ./agent enqueue --proposal "..." --context "<goal>" --class boundary-band

# you, later -> decide pending items; each accept/reject AUTO-LOGS here:
python3 gate.py --project ./agent review --prefs /path/to/prefs.py --suggest
```

`review --suggest` shows the predictor's guessed verdict + confidence BEFORE you decide; you
correct it, and the correction is logged as the next training example. The safety gate thus
*doubles as the training-data source* — using the system safely is the same act as teaching it
your judgment. Decisions are also captured to `state/GATE_RESOLVED.jsonl` fail-safe, so a human
call is never lost even if prefs.py can't be found. Verified end-to-end (enqueue → review →
auto-log → resolve).

## Status

Harness built; measurement machinery verified deterministically (stub) and the LLM predictor
path verified end-to-end. **No accuracy is claimed — that awaits your real decisions.** This is
the substrate for B5 (does feedback improve next-round prediction?), which can only be answered
once the log holds your real, non-saturated data.
