#!/usr/bin/env python3
"""plot_curve.py — ASCII renderer for the revealed-preference prequential curve.

Reads a prefs log (default ./prefs_log.jsonl), calls into prefs.py's eval_prequential
to get the bucketed accuracy curve, calls majority_baseline for the reference line, and
draws an ASCII bar chart (one bar per bucket, with a baseline marker) to stdout AND to a
.txt file. Stdlib only — no matplotlib.

HONESTY (read this — it is load-bearing):
  This script only DRAWS what prefs.py measures. It proves nothing about judgment on its own.
  The default predictor is `stub` (predict-the-majority): it verifies the MEASUREMENT
  MACHINERY with no `claude` CLI and no spend. A stub curve is NOT a result and must never be
  reported as one (see ./prefs.py, ./README.md "Cold-start honesty", and the REJECTED proposal
  P5.3 in ./prefs_log.jsonl — promoting a number to a "validated finding" was declined). A real
  prediction curve needs `--predictor llm` on >= 20 REAL, non-fabricated decisions; with too few
  decisions the curve is uninformative by construction. The caveat below is printed on every
  chart so the picture can't be screenshotted free of its disclaimer.

prefs.py lives in this same hyphenated directory, so it is imported via importlib (the dir name
`revealed-preference` is not a legal package identifier).

Usage:
  python3 plot_curve.py                          # default log, stub predictor, write ./prefs_curve.txt
  python3 plot_curve.py --log /path/log.jsonl --out /path/curve.txt
  python3 plot_curve.py --predictor llm          # real predictor (costs tokens; needs real data)
"""
import argparse
import importlib.util as iu
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREFS_PATH = HERE / "prefs.py"


def _load_module(path: Path, name: str):
    """Import a .py file by path (the dir is hyphenated, so a normal import won't work)."""
    spec = iu.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        sys.exit(f"[plot_curve] cannot load {path}")
    mod = iu.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


prefs = _load_module(PREFS_PATH, "prefs")


def render_chart(curve, baseline, *, predictor, n_recs, n_preds, warmup, width=40):
    """Build the ASCII chart as a list of text lines on a fixed [0.0, 1.0] accuracy axis.

    One bar per bucket; a '|' baseline marker shows majority-class accuracy in the same axis so
    bars above it = signal beyond the class ratio, bars below = worse than guessing the majority.
    """
    lines = []
    lines.append("Revealed-preference prequential curve (ASCII)")
    lines.append(f"  predictor : {predictor}")
    lines.append(f"  log size  : {n_recs} decisions   warmup : {warmup}   predicted : {n_preds}")
    lines.append(f"  baseline  : majority-class accuracy = {baseline:.1%}")
    lines.append("")

    if not curve:
        lines.append("  (no buckets — not enough decisions past warmup to plot a curve)")
        lines.append("")
    else:
        # axis runs 0.0..1.0 across `width` cells; baseline drawn as a '|' at its position.
        base_col = max(0, min(width - 1, round(baseline * (width - 1))))
        for i, acc in enumerate(curve):
            filled = max(0, min(width, round(acc * width)))
            cells = list("#" * filled + "-" * (width - filled))
            # overlay the baseline marker (don't let it vanish under the fill)
            cells[base_col] = "|" if cells[base_col] != "#" else "+"
            bar = "".join(cells)
            lines.append(f"  b{i:<2d} [{bar}] {acc:.1%}")
        lines.append("")
        # legend for the axis and the markers
        ruler = list("-" * width)
        ruler[base_col] = "|"
        lines.append(f"      0%{''.join(ruler)}100%")
        lines.append(f"        # = bucket accuracy   | = baseline ({baseline:.1%})   + = bar meets baseline")
        lines.append("")
        lines.append("  early -> late buckets; a RISING curve would be the B5 signal (more history -> better")
        lines.append("  prediction). It does not saturate by construction (early predictions are uninformed).")
        lines.append("")

    # the disclaimer travels with the chart, always.
    if predictor == "stub":
        lines.append("  NOTE: predictor=stub only verifies the eval MACHINERY (no LLM, no spend). This curve is")
        lines.append("  NOT a judgment result and must not be reported as one. Real curves need --predictor llm")
        lines.append("  on >= 20 REAL decisions (see ./README.md, ./prefs.py).")
    else:
        lines.append(f"  NOTE: predictor={predictor}. A curve is only meaningful on REAL, non-fabricated decisions")
        lines.append("  (rule of thumb >= 20; see ./README.md). Few decisions => uninformative by construction.")
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Render the prequential learning curve from a prefs log as an ASCII chart."
    )
    ap.add_argument("--log", type=Path, default=prefs.DEFAULT_LOG,
                    help="prefs log to read (default: revealed-preference/prefs_log.jsonl)")
    ap.add_argument("--out", type=Path, default=None,
                    help="text file to write the chart to (default: <log dir>/prefs_curve.txt)")
    ap.add_argument("--predictor", choices=tuple(prefs.PREDICTORS), default="stub",
                    help="stub (default; verifies machinery, no spend) | llm (real, costs tokens)")
    ap.add_argument("--warmup", type=int, default=5,
                    help="decisions to skip before the first prediction (matches prefs.py default)")
    args = ap.parse_args(argv)

    recs = prefs.load(args.log)
    if not recs:
        sys.exit(f"[plot_curve] no decisions in {args.log} — nothing to plot. Log real decisions first.")

    predictor_fn = prefs.PREDICTORS[args.predictor]
    _overall, curve, n_preds = prefs.eval_prequential(recs, predictor_fn, warmup=args.warmup)
    baseline = prefs.majority_baseline(recs)

    lines = render_chart(
        curve, baseline,
        predictor=args.predictor, n_recs=len(recs), n_preds=n_preds, warmup=args.warmup,
    )
    text = "\n".join(lines) + "\n"

    out = args.out if args.out is not None else args.log.resolve().parent / "prefs_curve.txt"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")

    sys.stdout.write(text)
    print(f"[plot_curve] wrote {out}")


if __name__ == "__main__":
    main()
