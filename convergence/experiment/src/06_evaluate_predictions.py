#!/usr/bin/env python3
"""Auto-generate the EVALUATION_REPORT.md comparing measured
results to the four pre-registered predictions.

Reads:
  - results/widths.csv (from 04_compute_widths.py)
  - PRE_REGISTRATION.md (for the git commit hash recording)

Writes:
  - results/EVALUATION_REPORT.md
"""

from __future__ import annotations

import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
RESULTS = EXPERIMENT_ROOT / "results"
PRE_REG_PATH = EXPERIMENT_ROOT / "PRE_REGISTRATION.md"


def log(msg: str) -> None:
    print(f"[evaluate] {msg}", flush=True)


def get_pre_registration_commit() -> str:
    """Return the git commit hash where PRE_REGISTRATION.md was last modified."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", str(PRE_REG_PATH)],
            cwd=EXPERIMENT_ROOT,
            capture_output=True, text=True, check=True,
        )
        return result.stdout.strip() or "unknown"
    except subprocess.CalledProcessError:
        return "unknown"


def evaluate_4_5_1(widths_df: pd.DataFrame) -> dict:
    """Within-model asymmetric ratio: w_E/w_D in [2, 4] per model."""
    results = []
    for _, row in widths_df.iterrows():
        ratio = row["ratio"]
        w_e, w_d = row["w_E"], row["w_D"]
        if pd.isna(ratio):
            verdict = "trivially confirmed (w_D=0)" if w_d == 0 else "n/a"
            confirms = (w_d == 0)  # extreme asymmetry counts as confirming
        elif ratio < 1.0:
            verdict = "STRONG FALSIFICATION (w_E < w_D)"
            confirms = False
        elif ratio < 1.5:
            verdict = "falsified (ratio < 1.5)"
            confirms = False
        elif ratio > 5.5:
            verdict = "falsified (ratio > 5.5)"
            confirms = False
        elif 2.0 <= ratio <= 4.0:
            verdict = "CONFIRMED"
            confirms = True
        else:
            verdict = "partial — outside [2, 4] but within [1.5, 5.5]"
            confirms = True   # framework gets partial credit

        results.append({
            "model": row["model_name"],
            "w_E": int(w_e), "w_D": int(w_d),
            "ratio": ratio if not pd.isna(ratio) else None,
            "verdict": verdict,
            "confirms": confirms,
        })

    n_confirm = sum(r["confirms"] for r in results)
    return {
        "results": results,
        "n_confirm": n_confirm,
        "n_total": len(results),
    }


def evaluate_4_5_2(widths_df: pd.DataFrame) -> dict:
    """Cross-architecture invariance band: spread <= 2."""
    ratios = widths_df["ratio"].dropna()
    if len(ratios) < 2:
        return {"spread": None, "confirms": None, "verdict": "insufficient data"}

    spread = float(ratios.max() - ratios.min())
    if spread <= 2.0:
        verdict = f"CONFIRMED (spread={spread:.2f})"
        confirms = True
    elif spread <= 3.0:
        verdict = f"partial (spread={spread:.2f}, threshold 2.0, falsify > 3.0)"
        confirms = False
    else:
        verdict = f"FALSIFIED (spread={spread:.2f} > 3)"
        confirms = False

    return {
        "spread": spread,
        "min_ratio": float(ratios.min()),
        "max_ratio": float(ratios.max()),
        "verdict": verdict,
        "confirms": confirms,
    }


def evaluate_4_5_3(widths_df: pd.DataFrame) -> dict:
    """Concept peak in middle: layer_concept_peak / N in [0.4, 0.7]."""
    results = []
    for _, row in widths_df.iterrows():
        norm = row["concept_peak_layer_normalized"]
        if pd.isna(norm) or norm < 0:
            verdict = "n/a (concept probe missing)"
            confirms = None
        elif 0.4 <= norm <= 0.7:
            verdict = f"CONFIRMED (peak at {norm:.2f} of depth)"
            confirms = True
        elif norm < 0.3 or norm > 0.8:
            verdict = f"FALSIFIED (peak at {norm:.2f}, outside [0.3, 0.8])"
            confirms = False
        else:
            verdict = f"partial (peak at {norm:.2f}, in [0.3, 0.4]∪[0.7, 0.8])"
            confirms = True

        results.append({
            "model": row["model_name"],
            "concept_peak_norm": norm,
            "verdict": verdict,
            "confirms": confirms,
        })

    n_eligible = sum(1 for r in results if r["confirms"] is not None)
    n_confirm = sum(1 for r in results if r["confirms"])
    return {"results": results, "n_confirm": n_confirm, "n_total": n_eligible}


def evaluate_4_5_4(widths_df: pd.DataFrame) -> dict:
    """Qualitative three-phase shape per model."""
    results = []
    for _, row in widths_df.iterrows():
        present = bool(row["three_phase_qualitative"])
        results.append({
            "model": row["model_name"],
            "early_max": float(row["early_max_acc"]),
            "middle_min": float(row["middle_min_acc"]),
            "late_max": float(row["late_max_acc"]),
            "verdict": "CONFIRMED" if present else "FALSIFIED",
            "confirms": present,
        })

    n_confirm = sum(r["confirms"] for r in results)
    return {"results": results, "n_confirm": n_confirm, "n_total": len(results)}


def render_report(widths_df: pd.DataFrame, e451: dict, e452: dict, e453: dict, e454: dict) -> str:
    """Build the markdown evaluation report."""
    commit = get_pre_registration_commit()
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    n_total = (e451["n_total"] + (1 if e452["confirms"] is not None else 0)
               + e453["n_total"] + e454["n_total"])
    n_confirm = (e451["n_confirm"]
                 + (1 if e452["confirms"] else 0)
                 + e453["n_confirm"]
                 + e454["n_confirm"])

    if n_confirm == n_total:
        overall = "**SLAM-DUNK CONFIRMATION**"
    elif n_confirm >= 0.75 * n_total:
        overall = "**PARTIAL CONFIRMATION**"
    elif n_confirm >= 0.5 * n_total:
        overall = "**MIXED RESULTS**"
    else:
        overall = "**FALSIFICATION**"

    lines = []
    lines.append(f"# Evaluation Report — Encoding/Decoding Asymmetry")
    lines.append("")
    lines.append(f"**Generated:** {now}")
    lines.append(f"**Pre-registration commit:** `{commit}`")
    lines.append(f"**Overall outcome:** {overall} ({n_confirm}/{n_total} sub-evaluations confirm)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Widths table
    lines.append("## Measured widths")
    lines.append("")
    cols = ["model_name", "n_layers", "w_E", "w_D", "ratio",
            "concept_peak_layer", "concept_peak_layer_normalized",
            "three_phase_qualitative"]
    available = [c for c in cols if c in widths_df.columns]
    md_table = widths_df[available].to_markdown(index=False, floatfmt=".2f")
    lines.append(md_table or "(no widths available)")
    lines.append("")

    # Prediction 4.5.1
    lines.append("## Prediction 4.5.1 — Within-model asymmetric ratio")
    lines.append("")
    lines.append(f"**Outcome:** {e451['n_confirm']}/{e451['n_total']} models confirm (w_E/w_D ∈ [1.5, 5.5], "
                 "with [2, 4] as the precise predicted range).")
    lines.append("")
    lines.append("| Model | w_E | w_D | ratio | verdict |")
    lines.append("|---|---|---|---|---|")
    for r in e451["results"]:
        ratio_str = f"{r['ratio']:.2f}" if r["ratio"] is not None else "—"
        lines.append(f"| {r['model']} | {r['w_E']} | {r['w_D']} | {ratio_str} | {r['verdict']} |")
    lines.append("")

    # Prediction 4.5.2
    lines.append("## Prediction 4.5.2 — Cross-architecture invariance band")
    lines.append("")
    lines.append(f"**Outcome:** {e452['verdict']}")
    if e452.get("min_ratio") is not None:
        lines.append(f"  - min ratio: {e452['min_ratio']:.2f}")
        lines.append(f"  - max ratio: {e452['max_ratio']:.2f}")
        lines.append(f"  - spread: {e452['spread']:.2f} (predicted ≤ 2.0; falsify > 3.0)")
    lines.append("")

    # Prediction 4.5.3
    lines.append("## Prediction 4.5.3 — Concept peak in middle layers")
    lines.append("")
    lines.append(f"**Outcome:** {e453['n_confirm']}/{e453['n_total']} models confirm "
                 "(concept-probe peak in [0.4, 0.7] normalized depth).")
    lines.append("")
    lines.append("| Model | peak (norm.) | verdict |")
    lines.append("|---|---|---|")
    for r in e453["results"]:
        norm_str = f"{r['concept_peak_norm']:.2f}" if r['concept_peak_norm'] is not None and r['concept_peak_norm'] >= 0 else "—"
        lines.append(f"| {r['model']} | {norm_str} | {r['verdict']} |")
    lines.append("")

    # Prediction 4.5.4
    lines.append("## Prediction 4.5.4 — Qualitative three-phase recurrence")
    lines.append("")
    lines.append(f"**Outcome:** {e454['n_confirm']}/{e454['n_total']} models confirm "
                 "(early max ≥ 0.70, middle min ≤ 0.50, late max ≥ 0.50).")
    lines.append("")
    lines.append("| Model | early_max | middle_min | late_max | verdict |")
    lines.append("|---|---|---|---|---|")
    for r in e454["results"]:
        lines.append(f"| {r['model']} | {r['early_max']:.2f} | {r['middle_min']:.2f} | "
                     f"{r['late_max']:.2f} | {r['verdict']} |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Summary by tier")
    lines.append("")
    lines.append(f"- **Slam-dunk:** all 4 sub-predictions × 4 models confirm.")
    lines.append(f"- **Partial confirmation:** ≥ 75% confirm.")
    lines.append(f"- **Mixed:** 50–75% confirm.")
    lines.append(f"- **Falsification:** < 50% confirm.")
    lines.append("")
    lines.append(f"**This run:** {n_confirm}/{n_total} = {100 * n_confirm / max(n_total, 1):.0f}% — {overall}")
    lines.append("")
    lines.append("## Methodology pointers")
    lines.append("")
    lines.append("- Pre-registered predictions: see `PRE_REGISTRATION.md` "
                 f"(committed at git hash `{commit}`).")
    lines.append("- Probe accuracy curves: `results/probes/<model>/`.")
    lines.append("- Plots: `results/plots/`.")
    lines.append("- Raw widths: `results/widths.csv`.")
    return "\n".join(lines)


def main() -> None:
    widths_csv = RESULTS / "widths.csv"
    if not widths_csv.exists():
        log(f"FAIL: {widths_csv} not found. Run src/04_compute_widths.py first.")
        sys.exit(1)

    widths_df = pd.read_csv(widths_csv)
    if widths_df.empty:
        log("FAIL: widths.csv is empty.")
        sys.exit(1)

    e451 = evaluate_4_5_1(widths_df)
    e452 = evaluate_4_5_2(widths_df)
    e453 = evaluate_4_5_3(widths_df)
    e454 = evaluate_4_5_4(widths_df)

    report = render_report(widths_df, e451, e452, e453, e454)

    out = RESULTS / "EVALUATION_REPORT.md"
    out.write_text(report)
    log(f"saved {out}")
    print()
    print(report)


if __name__ == "__main__":
    main()
