#!/usr/bin/env python3
"""Generate the three-measurements summary figure.

For each of the four probed models, plot per-layer:
 - Top: language probe accuracy (saturated at >0.99 from layer 1)
 - Middle: language-cluster NMI (inverted-U; drops in middle)
 - Bottom: participation ratio (inverted-U; high in middle)

Single figure, 4 columns (one per model), 3 rows (one per
measurement). Demonstrates the mutual consistency of the
three orthogonal geometric measurements of the mechanism-2/3
transition.

Output:
  results/plots/three_measurements_summary.png
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import yaml

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS = EXPERIMENT_ROOT / "configs"
PROBES = EXPERIMENT_ROOT / "results" / "probes"
RESULTS = EXPERIMENT_ROOT / "results"
PLOTS = RESULTS / "plots"


def log(msg: str) -> None:
    print(f"[plot] {msg}", flush=True)


def main() -> None:
    matplotlib.rcParams.update({"font.size": 9})

    mcfg = yaml.safe_load((CONFIGS / "models.yaml").read_text())
    models = [m["name"] for m in mcfg["models"]]

    # Load per-model data
    geo_df = pd.read_csv(RESULTS / "middle_layer_geometry.csv")
    cp_df = pd.read_csv(RESULTS / "cluster_purity.csv")

    fig, axes = plt.subplots(3, len(models), figsize=(4 * len(models), 8), sharex="col")

    for col, model in enumerate(models):
        # Language probe (pre-registered measurement)
        lang_csv = PROBES / model / "language_accuracy.csv"
        lang = pd.read_csv(lang_csv).sort_values("layer")
        lang_norm = lang["layer"].values / max(len(lang) - 1, 1)
        lang_acc = lang["test_acc"].values

        # Geometry: participation ratio
        gd = geo_df[geo_df["model"] == model].sort_values("layer")
        # Cluster purity: NMI vs language
        cd = cp_df[cp_df["model"] == model].sort_values("layer")

        ax_top = axes[0, col]
        ax_top.plot(lang_norm, lang_acc, "o-", color="#444", markersize=3)
        ax_top.axhline(0.7, color="#888", linestyle=":", linewidth=0.7, label="τ=0.70")
        ax_top.set_ylim(0, 1.05)
        ax_top.set_title(model)
        if col == 0:
            ax_top.set_ylabel("Language probe\n(accuracy)")

        ax_mid = axes[1, col]
        ax_mid.plot(cd["layer_norm"].values, cd["nmi_lang_k6"].values, "s-",
                    color="#1f77b4", markersize=3)
        ax_mid.set_ylim(0, 1.05)
        if col == 0:
            ax_mid.set_ylabel("Cluster NMI vs\nlanguage (k=6)")

        ax_bot = axes[2, col]
        ax_bot.plot(gd["layer_norm"].values, gd["participation_ratio"].values, "^-",
                    color="#d62728", markersize=3)
        if col == 0:
            ax_bot.set_ylabel("Participation\nratio")
        ax_bot.set_xlabel("Normalized layer depth")

    fig.suptitle(
        "Three orthogonal geometric measurements of the mechanism-2/3 transition\n"
        "Top: probe accuracy (uniform from layer 1). "
        "Middle: NMI inverted-U (4/4 dip). "
        "Bottom: PR inverted-U (4/4 middle peak).",
        fontsize=10
    )
    plt.tight_layout(rect=[0, 0, 1, 0.93])

    PLOTS.mkdir(parents=True, exist_ok=True)
    out = PLOTS / "three_measurements_summary.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    log(f"saved {out}")


if __name__ == "__main__":
    main()
