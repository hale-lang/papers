#!/usr/bin/env python3
"""M2 — Effective rank at multiple variance thresholds, raw + cosine.

NOT PRE-REGISTERED. Method-calibration follow-up to the
cluster-k* test (see results/OPTIMAL_K_REPORT.md M2 entry).
The cluster-k* test had no power in high-PR regimes; this
test uses an operationalization specifically designed for
high-PR continuous-manifold representations.

For each layer:
 1. PCA on raw activations; record the number of components
    needed to explain p of total variance for p ∈ {0.50, 0.75,
    0.90, 0.95, 0.99}.
 2. PCA on L2-row-normalized activations (cosine geometry);
    same.

Hypothesis (refines participation-ratio finding): middle
layers should require MORE components to reach high variance
fractions than perimeter layers, with the gap WIDENING at
higher variance thresholds. The participation ratio captures
the integrated signal; this method asks "how many distinct
directions of structure live in this layer at each level of
fidelity."

Cosine vs raw matters because magnitude information may be
dominating the raw PR. If the inverted-U is preserved (or
sharpened) under cosine geometry, the dimensionality
inversion is about *direction*-counts, which is what the
P_3-chunked sub-class predicts.

Output:
  results/effective_rank.csv
  results/plots/effective_rank_curves.png
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import yaml
import matplotlib.pyplot as plt
import matplotlib

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
ACTIVATIONS = EXPERIMENT_ROOT / "results" / "activations"
CONFIGS = EXPERIMENT_ROOT / "configs"
RESULTS = EXPERIMENT_ROOT / "results"
PLOTS = RESULTS / "plots"

PROBE = "concept"
N_SAMPLES = 4000
SEED = 42
THRESHOLDS = [0.50, 0.75, 0.90, 0.95, 0.99]


def log(msg: str) -> None:
    print(f"[m2] {msg}", flush=True)


def components_for_variance(eigenvalues_sorted: np.ndarray, threshold: float) -> int:
    """Number of components needed to reach `threshold` of total variance."""
    total = float(eigenvalues_sorted.sum())
    if total <= 0:
        return 0
    csum = np.cumsum(eigenvalues_sorted) / total
    return int(np.searchsorted(csum, threshold) + 1)


def analyze_layer(X: np.ndarray) -> dict:
    """Returns components-needed for each threshold under raw and cosine."""
    # Raw: center, get singular values
    Xc = X - X.mean(axis=0, keepdims=True)
    s_raw = np.linalg.svd(Xc, compute_uv=False)
    eigs_raw = (s_raw ** 2)
    eigs_raw.sort()
    eigs_raw = eigs_raw[::-1]

    # Cosine: row-normalize first, then center, then SVD
    norms = np.linalg.norm(X, axis=1, keepdims=True)
    norms[norms < 1e-9] = 1.0
    Xn = X / norms
    Xnc = Xn - Xn.mean(axis=0, keepdims=True)
    s_cos = np.linalg.svd(Xnc, compute_uv=False)
    eigs_cos = (s_cos ** 2)
    eigs_cos.sort()
    eigs_cos = eigs_cos[::-1]

    out = {}
    for t in THRESHOLDS:
        out[f"raw_n_for_{int(t*100)}"] = components_for_variance(eigs_raw, t)
        out[f"cos_n_for_{int(t*100)}"] = components_for_variance(eigs_cos, t)
    return out


def analyze_model(model_name: str) -> list[dict]:
    act_path = ACTIVATIONS / model_name / PROBE / "activations.npy"
    if not act_path.exists():
        log(f"FAIL: {model_name}")
        return []

    log(f"=== {model_name} ===")
    act = np.load(act_path, mmap_mode="r")
    n, n_layers_p1, hidden = act.shape
    rng = np.random.RandomState(SEED)
    idx = rng.choice(n, min(N_SAMPLES, n), replace=False)

    rows = []
    for layer in range(n_layers_p1):
        X = np.asarray(act[idx, layer, :], dtype=np.float32)
        per = analyze_layer(X)
        per["model"] = model_name
        per["layer"] = layer
        per["layer_norm"] = layer / max(n_layers_p1 - 1, 1)
        rows.append(per)
        if layer % 4 == 0 or layer == n_layers_p1 - 1:
            log(
                f"  layer={layer:2d} (norm={per['layer_norm']:.2f}): "
                f"raw n@90%={per['raw_n_for_90']:3d}, "
                f"cos n@90%={per['cos_n_for_90']:3d}; "
                f"raw n@99%={per['raw_n_for_99']:4d}, "
                f"cos n@99%={per['cos_n_for_99']:4d}"
            )
    return rows


def plot_curves(df: pd.DataFrame, out_path: Path) -> None:
    matplotlib.rcParams.update({"font.size": 9})
    models = sorted(df["model"].unique())
    fig, axes = plt.subplots(2, len(models), figsize=(4 * len(models), 6),
                              sharex="col")

    for col, model in enumerate(models):
        sub = df[df["model"] == model].sort_values("layer")

        ax_top = axes[0, col]
        for t in THRESHOLDS:
            ax_top.plot(sub["layer_norm"], sub[f"raw_n_for_{int(t*100)}"],
                        marker="o", markersize=3, label=f"{int(t*100)}%")
        ax_top.set_yscale("log")
        ax_top.set_title(f"{model}\nRaw activations")
        if col == 0:
            ax_top.set_ylabel("# PCs needed\n(raw)")
        if col == len(models) - 1:
            ax_top.legend(fontsize=7, title="variance", loc="lower right")
        ax_top.grid(True, alpha=0.3)

        ax_bot = axes[1, col]
        for t in THRESHOLDS:
            ax_bot.plot(sub["layer_norm"], sub[f"cos_n_for_{int(t*100)}"],
                        marker="s", markersize=3, label=f"{int(t*100)}%")
        ax_bot.set_yscale("log")
        ax_bot.set_xlabel("Normalized layer depth")
        ax_bot.set_title("L2-normalized (cosine)")
        if col == 0:
            ax_bot.set_ylabel("# PCs needed\n(cosine)")
        ax_bot.grid(True, alpha=0.3)

    fig.suptitle(
        "M2 — Effective rank at variance thresholds, raw vs cosine\n"
        "Number of PCA components needed to explain {50, 75, 90, 95, 99}% of variance per layer.",
        fontsize=10
    )
    plt.tight_layout(rect=[0, 0, 1, 0.93])
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    log(f"saved {out_path}")


def main() -> None:
    mcfg = yaml.safe_load((CONFIGS / "models.yaml").read_text())
    log("M2 effective-rank-at-thresholds analysis")

    all_rows = []
    summary = []
    for m in mcfg["models"]:
        rows = analyze_model(m["name"])
        if not rows:
            continue
        all_rows.extend(rows)
        df = pd.DataFrame(rows).sort_values("layer")
        n = len(df)

        # Inverted-U test at each threshold under each metric
        for prefix in ("raw", "cos"):
            for t in (90, 95, 99):
                col = f"{prefix}_n_for_{t}"
                vals = df[col].values
                early = vals[: n // 3].mean()
                middle = vals[n // 3 : 2 * n // 3].mean()
                late = vals[2 * n // 3 :].mean()
                summary.append(
                    {
                        "model": m["name"],
                        "metric": prefix,
                        "threshold": t,
                        "early": early,
                        "middle": middle,
                        "late": late,
                        "inverted_U": bool(middle > early and middle > late),
                        "ratio_mid_late": middle / late if late > 0 else float("inf"),
                    }
                )

    df_full = pd.DataFrame(all_rows)
    df_full.to_csv(RESULTS / "effective_rank.csv", index=False)
    log(f"saved {RESULTS / 'effective_rank.csv'}")

    sdf = pd.DataFrame(summary)
    sdf.to_csv(RESULTS / "effective_rank_summary.csv", index=False)
    log(f"saved {RESULTS / 'effective_rank_summary.csv'}")

    log("")
    log("Inverted-U replication count by metric × threshold:")
    pivot = sdf.groupby(["metric", "threshold"])["inverted_U"].sum()
    log(pivot.to_string())

    log("")
    log("Mean middle/late ratio by metric × threshold (across 4 models):")
    pivot2 = sdf.groupby(["metric", "threshold"])["ratio_mid_late"].mean()
    log(pivot2.to_string())

    plot_curves(df_full, PLOTS / "effective_rank_curves.png")


if __name__ == "__main__":
    main()
