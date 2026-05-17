#!/usr/bin/env python3
"""Generate publication-quality plots from probe accuracy curves.

Plots produced:
 1. results/plots/probe_curves_<model>.png    — per-model
    layer-wise probe accuracy (language + concept curves
    overlaid; threshold line at τ_lang).
 2. results/plots/probe_curves_grid.png       — 2x2 grid of all
    four models for direct comparison.
 3. results/plots/widths_summary.png          — bar plot of w_E
    vs w_D across models, with predicted-range shading.
 4. results/plots/ratio_vs_prediction.png     — scatter of
    measured w_E/w_D ratios against pre-registered range [2, 4].
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS = EXPERIMENT_ROOT / "configs"
PROBES = EXPERIMENT_ROOT / "results" / "probes"
RESULTS = EXPERIMENT_ROOT / "results"
PLOTS = RESULTS / "plots"


def log(msg: str) -> None:
    print(f"[plot] {msg}", flush=True)


def load_configs():
    return (
        yaml.safe_load((CONFIGS / "experiment.yaml").read_text()),
        yaml.safe_load((CONFIGS / "models.yaml").read_text()),
    )


def plot_per_model(model_name: str, threshold: float) -> None:
    lang_csv = PROBES / model_name / "language_accuracy.csv"
    concept_csv = PROBES / model_name / "concept_accuracy.csv"
    if not lang_csv.exists():
        return

    lang_df = pd.read_csv(lang_csv).sort_values("layer")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(lang_df["layer"], lang_df["test_acc"], marker="o", markersize=4,
            label="language ID probe", color="C0")
    if concept_csv.exists():
        concept_df = pd.read_csv(concept_csv).sort_values("layer")
        ax.plot(concept_df["layer"], concept_df["test_acc"], marker="s", markersize=4,
                label="concept (NLI) probe", color="C1")

    ax.axhline(threshold, linestyle="--", color="gray", alpha=0.6,
               label=f"τ_lang = {threshold}")

    ax.set_xlabel("Layer index")
    ax.set_ylabel("Probe test accuracy")
    ax.set_title(f"{model_name}: per-layer probe accuracy")
    ax.set_ylim(-0.02, 1.02)
    ax.legend(loc="lower center")
    ax.grid(True, alpha=0.3)

    out = PLOTS / f"probe_curves_{model_name}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)
    log(f"saved {out}")


def plot_grid(model_names: list[str], threshold: float) -> None:
    n = len(model_names)
    if n == 0:
        return
    cols = 2
    rows = (n + 1) // 2
    fig, axes = plt.subplots(rows, cols, figsize=(12, 4 * rows), sharey=True)
    axes_flat = axes.flatten() if rows > 1 or cols > 1 else [axes]

    for ax, model_name in zip(axes_flat, model_names):
        lang_csv = PROBES / model_name / "language_accuracy.csv"
        concept_csv = PROBES / model_name / "concept_accuracy.csv"
        if not lang_csv.exists():
            ax.set_visible(False)
            continue

        lang_df = pd.read_csv(lang_csv).sort_values("layer")
        ax.plot(lang_df["layer"], lang_df["test_acc"], marker="o", markersize=3,
                label="language", color="C0")
        if concept_csv.exists():
            concept_df = pd.read_csv(concept_csv).sort_values("layer")
            ax.plot(concept_df["layer"], concept_df["test_acc"], marker="s", markersize=3,
                    label="concept", color="C1")
        ax.axhline(threshold, linestyle="--", color="gray", alpha=0.5)
        ax.set_title(model_name)
        ax.set_xlabel("layer")
        ax.set_ylim(-0.02, 1.02)
        ax.grid(True, alpha=0.3)

    axes_flat[0].set_ylabel("test accuracy")
    if rows > 1:
        axes_flat[2].set_ylabel("test accuracy")
    axes_flat[0].legend(loc="lower center")

    # Hide any unused panels
    for j in range(n, len(axes_flat)):
        axes_flat[j].set_visible(False)

    fig.suptitle("Per-layer probe accuracy across models", y=1.02)
    out = PLOTS / "probe_curves_grid.png"
    fig.tight_layout()
    fig.savefig(out, dpi=130, bbox_inches="tight")
    plt.close(fig)
    log(f"saved {out}")


def plot_widths_summary(widths_df: pd.DataFrame) -> None:
    if widths_df.empty:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.arange(len(widths_df))
    width = 0.35
    ax.bar(x - width/2, widths_df["w_E"], width, label="w_E (encoding)", color="C0")
    ax.bar(x + width/2, widths_df["w_D"], width, label="w_D (decoding)", color="C2")

    ax.set_xticks(x)
    ax.set_xticklabels(widths_df["model_name"], rotation=15, ha="right")
    ax.set_ylabel("Bundle width (layers)")
    ax.set_title("Encoding vs decoding bundle widths")
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")

    out = PLOTS / "widths_summary.png"
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)
    log(f"saved {out}")


def plot_ratio_vs_prediction(widths_df: pd.DataFrame) -> None:
    df = widths_df.dropna(subset=["ratio"])
    if df.empty:
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    # Predicted range shading
    ax.axhspan(2.0, 4.0, color="C2", alpha=0.15, label="predicted [2, 4]")
    # Falsification thresholds
    ax.axhline(1.5, linestyle=":", color="C3", alpha=0.7, label="falsification < 1.5")
    ax.axhline(5.5, linestyle=":", color="C3", alpha=0.7, label="falsification > 5.5")
    ax.axhline(1.0, linestyle="-", color="C3", alpha=0.4,
               label="strong falsification ≤ 1.0 (decoding ≥ encoding)")

    x = np.arange(len(df))
    ax.scatter(x, df["ratio"], s=80, color="C0", zorder=3)
    for xi, (_, r) in zip(x, df.iterrows()):
        ax.annotate(f"{r['ratio']:.2f}", (xi, r["ratio"]),
                    xytext=(8, 0), textcoords="offset points", va="center")

    ax.set_xticks(x)
    ax.set_xticklabels(df["model_name"], rotation=15, ha="right")
    ax.set_ylabel("w_E / w_D ratio")
    ax.set_title("Measured w_E/w_D ratios vs pre-registered prediction")
    ax.set_ylim(0, max(6.5, float(df["ratio"].max()) + 1.0))
    ax.legend(loc="upper right", fontsize=8)
    ax.grid(True, alpha=0.3)

    out = PLOTS / "ratio_vs_prediction.png"
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    plt.close(fig)
    log(f"saved {out}")


def main() -> None:
    ecfg, mcfg = load_configs()
    threshold = ecfg["language_probe"]["threshold"]
    PLOTS.mkdir(parents=True, exist_ok=True)

    model_names = [m["name"] for m in mcfg["models"]]
    for name in model_names:
        plot_per_model(name, threshold)

    plot_grid(model_names, threshold)

    widths_csv = RESULTS / "widths.csv"
    if widths_csv.exists():
        widths_df = pd.read_csv(widths_csv)
        plot_widths_summary(widths_df)
        plot_ratio_vs_prediction(widths_df)
    else:
        log("widths.csv not found; skipping summary plots")

    log("Plotting complete.")


if __name__ == "__main__":
    main()
