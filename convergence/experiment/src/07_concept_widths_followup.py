#!/usr/bin/env python3
"""Exploratory follow-up: concept-based w_E / w_D.

NOT PRE-REGISTERED. This analysis is a non-pre-registered
exploratory follow-up motivated by the result of the
pre-registered analysis (see EVALUATION_REPORT.md and
ADDENDUM_003.md): the language-identity probe is saturated by
the first transformer block in all four models, so w_E ≈ w_D ≈
n_layers and the asymmetry test cannot distinguish α_E from
α_D for that signal.

The concept probe (XNLI 3-class entailment / neutral /
contradiction), by contrast, exhibits the predicted middle-peak
shape in 4/4 models (4.5.3 confirmed). This script
operationalizes w_E and w_D using the concept probe instead:

  w_E (concept) = number of contiguous *late*-side layers from
    the concept peak going backwards toward layer 0 where
    concept-probe accuracy stays within Δ = 0.1 of the peak.
  w_D (concept) = number of contiguous *early*-side layers
    from the peak going forward toward the final layer where
    concept-probe accuracy stays within Δ = 0.1 of the peak.

Naming: encoding bundle is the lead-in to the concept-peak;
decoding bundle is the lead-out. Both measured around the
empirically observed peak rather than around an absolute
threshold, because concept-probe baseline differs across
models.

Output:
  results/concept_widths.csv
  results/CONCEPT_FOLLOWUP_REPORT.md

Discipline note: this analysis is run AFTER seeing the
pre-registered result. It is a hypothesis-generating analysis,
not a hypothesis-confirming one. We report it explicitly as
exploratory; any quantitative claim built on it would need
fresh pre-registration on a separate experimental run with
different models or different probes to confirm.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml
import numpy as np
import pandas as pd

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS = EXPERIMENT_ROOT / "configs"
PROBES = EXPERIMENT_ROOT / "results" / "probes"
RESULTS = EXPERIMENT_ROOT / "results"

# Tolerance for "near peak" — concept-probe accuracy must stay
# within DELTA of the peak to count as bundle interior.
DELTA = 0.10


def log(msg: str) -> None:
    print(f"[concept-widths] {msg}", flush=True)


def load_configs():
    return (
        yaml.safe_load((CONFIGS / "experiment.yaml").read_text()),
        yaml.safe_load((CONFIGS / "models.yaml").read_text()),
    )


def compute_concept_widths(test_acc: np.ndarray, delta: float) -> tuple[int, int, int, float]:
    """Find peak layer; return (w_E, w_D, peak_layer, peak_acc).

    w_E (concept) = layers BEFORE peak that stay within delta
                    of peak accuracy.
    w_D (concept) = layers AFTER peak that stay within delta
                    of peak accuracy.
    Both inclusive of the peak layer for symmetry.
    """
    peak_layer = int(np.argmax(test_acc))
    peak_acc = float(test_acc[peak_layer])
    threshold = peak_acc - delta

    # Walk backward from peak toward layer 0
    w_e = 1  # peak layer itself counts
    for i in range(peak_layer - 1, -1, -1):
        if test_acc[i] >= threshold:
            w_e += 1
        else:
            break

    # Walk forward from peak toward final layer
    w_d = 0  # peak layer already counted in w_e
    for i in range(peak_layer + 1, len(test_acc)):
        if test_acc[i] >= threshold:
            w_d += 1
        else:
            break

    return w_e, w_d, peak_layer, peak_acc


def render_concept_report(rows: list[dict], delta: float) -> str:
    lines = []
    lines.append("# Concept-Based Bundle Widths — Exploratory Follow-up")
    lines.append("")
    lines.append("**STATUS: NON-PRE-REGISTERED EXPLORATORY ANALYSIS.**")
    lines.append("")
    lines.append("This analysis is a hypothesis-generating follow-up to the")
    lines.append("pre-registered evaluation in `EVALUATION_REPORT.md`. It")
    lines.append("operationalizes w_E and w_D using the concept probe instead")
    lines.append("of the language probe, motivated by the observation that")
    lines.append("the language probe is saturated and the concept probe")
    lines.append("exhibits the predicted middle-peak shape (4.5.3 confirmed,")
    lines.append("4/4 models).")
    lines.append("")
    lines.append("Pre-registration (commit `708f13f`) committed to")
    lines.append("language-probe operationalization with τ_lang = 0.70. This")
    lines.append("script is *not* part of that pre-registration. Quantitative")
    lines.append("claims surfaced here are hypothesis-generating; confirming")
    lines.append("any of them requires fresh pre-registration on a different")
    lines.append("experimental run.")
    lines.append("")
    lines.append(f"**Bundle definition:** concept-probe accuracy stays within")
    lines.append(f"Δ = {delta} of the empirical peak. w_E counts layers from")
    lines.append("peak backward toward layer 0 (encoding bundle); w_D counts")
    lines.append("layers from peak forward toward the final layer (decoding")
    lines.append("bundle).")
    lines.append("")
    lines.append("## Measured concept-based widths")
    lines.append("")
    lines.append("| Model | n_layers | peak_layer | peak_acc | w_E (concept) | w_D (concept) | ratio |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in rows:
        ratio = r["w_E_concept"] / r["w_D_concept"] if r["w_D_concept"] > 0 else float("inf")
        lines.append(
            f"| {r['model_name']} | {r['n_layers']} | {r['concept_peak_layer']} | "
            f"{r['concept_peak_acc']:.3f} | {r['w_E_concept']} | {r['w_D_concept']} | "
            f"{ratio:.2f} |"
        )
    lines.append("")
    lines.append("## Interpretation")
    lines.append("")
    lines.append("The concept-based bundle widths capture the structural")
    lines.append("region around the format-agnostic semantic middle — the")
    lines.append("layers where concept information is held at near-peak")
    lines.append("accuracy. w_E is the lead-in (concept structure forming);")
    lines.append("w_D is the lead-out (concept structure being projected")
    lines.append("back to format-specific representations).")
    lines.append("")
    lines.append("This operationalization is consistent with the framework's")
    lines.append("per-direction prediction in spirit but not in pre-registered")
    lines.append("operational form: the bundle is now anchored to the *narrow*")
    lines.append("interior signal (concept) rather than the *saturated*")
    lines.append("perimeter signal (language identity). The cross-architecture")
    lines.append("distribution of concept w_E / w_D ratios surfaces here as a")
    lines.append("hypothesis worth pre-registering on a separate run.")
    lines.append("")
    lines.append("## What this analysis does and does not establish")
    lines.append("")
    lines.append("*Establishes:*")
    lines.append("- The concept signal exhibits a structurally non-trivial")
    lines.append("  shape across all four models, with measurable bundle")
    lines.append("  widths around the peak.")
    lines.append("- The concept-bundle widths are concrete numbers that")
    lines.append("  could be the target of a future pre-registered prediction.")
    lines.append("")
    lines.append("*Does not establish:*")
    lines.append("- The framework's per-direction asymmetry prediction (1′)")
    lines.append("  is **not confirmed** by this analysis. Confirmation")
    lines.append("  requires a pre-registered prediction on a separate run.")
    lines.append("- Non-pre-registered analyses are subject to garden-of-")
    lines.append("  forking-paths concerns; we report this analysis once,")
    lines.append("  honestly labeled, without iterating on the bundle")
    lines.append("  definition until the numbers look favorable.")
    lines.append("")
    lines.append("## Methodology pointers")
    lines.append("")
    lines.append("- Pre-registered predictions: see `PRE_REGISTRATION.md`")
    lines.append("  (committed at git hash `708f13f`).")
    lines.append(f"- Pre-registered evaluation: `EVALUATION_REPORT.md`.")
    lines.append("- Addenda: ADDENDUM_001 (pre-data dataset switch),")
    lines.append("  ADDENDUM_002 (pre-data probe convergence fix),")
    lines.append("  ADDENDUM_003 (post-data interpretive disclosure).")
    lines.append("- Probe accuracy curves: `results/probes/<model>/`.")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    _, mcfg = load_configs()

    log(f"Concept-bundle width tolerance Δ = {DELTA}")
    log("(NON-PRE-REGISTERED EXPLORATORY FOLLOW-UP)")

    rows = []
    for model_cfg in mcfg["models"]:
        model_name = model_cfg["name"]
        concept_csv = PROBES / model_name / "concept_accuracy.csv"

        if not concept_csv.exists():
            log(f"  {model_name}: concept probe missing; skipping")
            continue

        concept_df = pd.read_csv(concept_csv).sort_values("layer")
        test_acc = concept_df["test_acc"].values
        n_layers = len(test_acc)

        w_e, w_d, peak_layer, peak_acc = compute_concept_widths(test_acc, DELTA)
        ratio = (w_e / w_d) if w_d > 0 else float("inf")

        row = {
            "model_name": model_name,
            "n_layers": n_layers,
            "concept_peak_layer": peak_layer,
            "concept_peak_acc": peak_acc,
            "w_E_concept": w_e,
            "w_D_concept": w_d,
            "ratio_concept": ratio if w_d > 0 else None,
        }
        rows.append(row)

        log(
            f"  {model_name}: n_layers={n_layers}, peak={peak_layer} "
            f"(acc={peak_acc:.3f}), w_E={w_e}, w_D={w_d}, ratio={ratio:.2f}"
        )

    df = pd.DataFrame(rows)
    out_csv = RESULTS / "concept_widths.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    log(f"saved {out_csv}")

    out_md = RESULTS / "CONCEPT_FOLLOWUP_REPORT.md"
    out_md.write_text(render_concept_report(rows, DELTA))
    log(f"saved {out_md}")

    if not df.empty:
        ratios = df["ratio_concept"].dropna()
        if len(ratios) > 0:
            log(f"\nConcept-based ratio summary across {len(ratios)} models:")
            log(
                f"  min={ratios.min():.2f}, max={ratios.max():.2f}, "
                f"mean={ratios.mean():.2f}, spread={ratios.max() - ratios.min():.2f}"
            )


if __name__ == "__main__":
    main()
