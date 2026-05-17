#!/usr/bin/env python3
"""Compute w_E, w_D, and ratio for each model from probe accuracy curves.

Per pre-registration:
 - w_E = number of contiguous early layers (from layer 0) where
   language-identity probe test accuracy >= τ_lang. At most one
   below-threshold layer is allowed within the contiguous region.
 - w_D = number of contiguous late layers (ending at last layer)
   meeting the same criterion.
 - τ_lang = 0.70 (committed in PRE_REGISTRATION.md).

Output:
  results/widths.csv
    columns: model_name, n_layers, w_E, w_D, ratio, threshold,
             concept_peak_layer, concept_peak_layer_normalized,
             three_phase_qualitative

The qualitative three-phase check (4.5.4) is also computed here:
 - max(test_acc) in first third >= 0.70
 - min(test_acc) in middle third <= 0.50
 - max(test_acc) in last third >= 0.50
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


def log(msg: str) -> None:
    print(f"[widths] {msg}", flush=True)


def load_configs():
    return (
        yaml.safe_load((CONFIGS / "experiment.yaml").read_text()),
        yaml.safe_load((CONFIGS / "models.yaml").read_text()),
    )


def compute_bundle_widths(test_acc: np.ndarray, threshold: float, tolerance: int) -> tuple[int, int]:
    """Compute w_E and w_D from a test-accuracy curve.

    - w_E: count of contiguous early layers where acc >= threshold,
      allowing up to `tolerance` below-threshold gaps that still
      have a recovering layer adjacent.
    - w_D: same logic from the end of the curve.

    Note: with tolerance=1, we allow at most ONE layer below
    threshold within the bundle, but the bundle ends as soon as
    we see two consecutive below-threshold layers.
    """
    above = test_acc >= threshold
    n = len(above)

    # w_E: scan from the start
    w_e = 0
    consecutive_below = 0
    for i in range(n):
        if above[i]:
            w_e = i + 1
            consecutive_below = 0
        else:
            consecutive_below += 1
            if consecutive_below > tolerance:
                break

    # w_D: scan from the end
    w_d = 0
    consecutive_below = 0
    for i in range(n - 1, -1, -1):
        if above[i]:
            w_d = n - i
            consecutive_below = 0
        else:
            consecutive_below += 1
            if consecutive_below > tolerance:
                break

    return w_e, w_d


def qualitative_three_phase(test_acc: np.ndarray) -> dict:
    """Check the qualitative three-phase shape per prediction 4.5.4.

    Returns a dict with the per-third stats and a boolean for
    whether the qualitative pattern is present.
    """
    n = len(test_acc)
    third = n // 3
    early = test_acc[:third]
    middle = test_acc[third:2*third]
    late = test_acc[2*third:]

    early_max = float(early.max()) if len(early) else 0.0
    middle_min = float(middle.min()) if len(middle) else 1.0
    late_max = float(late.max()) if len(late) else 0.0

    pattern = (early_max >= 0.70) and (middle_min <= 0.50) and (late_max >= 0.50)
    return {
        "early_max": early_max,
        "middle_min": middle_min,
        "late_max": late_max,
        "three_phase_qualitative": pattern,
    }


def main() -> None:
    ecfg, mcfg = load_configs()
    threshold = ecfg["language_probe"]["threshold"]
    tolerance = ecfg["language_probe"]["contiguity_tolerance"]
    log(f"τ_lang = {threshold}, contiguity_tolerance = {tolerance}")

    rows = []
    for model_cfg in mcfg["models"]:
        model_name = model_cfg["name"]
        lang_csv = PROBES / model_name / "language_accuracy.csv"
        concept_csv = PROBES / model_name / "concept_accuracy.csv"

        if not lang_csv.exists():
            log(f"  {model_name}: language probe missing; skipping")
            continue

        lang_df = pd.read_csv(lang_csv).sort_values("layer")
        test_acc = lang_df["test_acc"].values
        n_layers = len(test_acc)

        w_e, w_d = compute_bundle_widths(test_acc, threshold, tolerance)
        ratio = (w_e / w_d) if w_d > 0 else float("inf")

        qual = qualitative_three_phase(test_acc)

        # Concept peak layer (4.5.3)
        concept_peak_layer = -1
        concept_peak_norm = -1.0
        if concept_csv.exists():
            concept_df = pd.read_csv(concept_csv).sort_values("layer")
            concept_acc = concept_df["test_acc"].values
            concept_peak_layer = int(np.argmax(concept_acc))
            concept_peak_norm = concept_peak_layer / max(len(concept_acc) - 1, 1)

        row = {
            "model_name": model_name,
            "n_layers": n_layers,
            "w_E": w_e,
            "w_D": w_d,
            "ratio": ratio if w_d > 0 else None,
            "threshold": threshold,
            "concept_peak_layer": concept_peak_layer,
            "concept_peak_layer_normalized": concept_peak_norm,
            "early_max_acc": qual["early_max"],
            "middle_min_acc": qual["middle_min"],
            "late_max_acc": qual["late_max"],
            "three_phase_qualitative": qual["three_phase_qualitative"],
        }
        rows.append(row)

        log(f"  {model_name}: n_layers={n_layers}, w_E={w_e}, w_D={w_d}, "
            f"ratio={ratio:.2f}" if w_d > 0 else
            f"  {model_name}: n_layers={n_layers}, w_E={w_e}, w_D={w_d}, ratio=inf (w_D=0)")

    df = pd.DataFrame(rows)
    out = RESULTS / "widths.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False)
    log(f"saved {out}")

    if not df.empty:
        ratios = df["ratio"].dropna()
        if len(ratios) > 0:
            log(f"\nRatio summary across {len(ratios)} models:")
            log(f"  min={ratios.min():.2f}, max={ratios.max():.2f}, "
                f"mean={ratios.mean():.2f}, spread={ratios.max() - ratios.min():.2f}")


if __name__ == "__main__":
    main()
