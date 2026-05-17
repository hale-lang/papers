#!/usr/bin/env python3
"""Exploratory: middle-layer representational geometry.

NOT PRE-REGISTERED. Hypothesis: even in regions where the
language probe is saturated and looks "flat", the underlying
hidden-state geometry may exhibit richer category structure
in the middle than at the perimeter.

This script measures per-layer:
 1. Participation ratio (PR): an intrinsic dimensionality
    estimate. PR = (Σ λ_i)² / Σ λ_i² where λ_i are eigenvalues
    of the activation covariance matrix. PR is the effective
    number of dimensions that the activations span. Small PR
    = activations cluster on a low-dimensional manifold; large
    PR = activations span many dimensions roughly equally.
 2. The maximum-explained-variance fraction of the top-K
    principal components for K=10, K=50 — how concentrated is
    the variance in the leading directions?

Operating on a single model (Llama-3.2-3B, 2 GB of concept
activations) to keep this exploratory, fast, and bounded.

Output:
  results/middle_layer_geometry.csv

Discipline note: this analysis is hypothesis-generating, not
hypothesis-confirming. It tests whether the middle-layer
geometry differs from the perimeter geometry in a measurable
way; it does not pre-register any specific shape of that
difference.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

import yaml

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
ACTIVATIONS = EXPERIMENT_ROOT / "results" / "activations"
CONFIGS = EXPERIMENT_ROOT / "configs"
RESULTS = EXPERIMENT_ROOT / "results"

PROBE = "concept"


def log(msg: str) -> None:
    print(f"[geometry] {msg}", flush=True)


def participation_ratio(eigenvalues: np.ndarray) -> float:
    """PR = (sum λ)² / sum λ² — effective dimensionality."""
    s = float(eigenvalues.sum())
    s2 = float((eigenvalues ** 2).sum())
    if s2 == 0:
        return 0.0
    return s * s / s2


def analyze_model(model_name: str) -> list[dict]:
    """Return per-layer geometry stats for one model."""
    act_path = ACTIVATIONS / model_name / PROBE / "activations.npy"
    if not act_path.exists():
        log(f"FAIL: {act_path} missing")
        return []

    log(f"=== {model_name} ===")
    log(f"  Loading {act_path} (memmap)")
    act = np.load(act_path, mmap_mode="r")
    n, n_layers_p1, hidden = act.shape
    log(f"  shape={act.shape}, dtype={act.dtype}")

    rows = []
    for layer in range(n_layers_p1):
        # Load this layer into RAM, cast to fp32
        X = np.asarray(act[:, layer, :], dtype=np.float32)
        # Center
        X = X - X.mean(axis=0, keepdims=True)
        # SVD-based eigenvalues of covariance
        # Cov = (1/n) X^T X; eigenvalues = singular values of X / sqrt(n), squared
        # Faster: use np.linalg.svd on X with full_matrices=False
        # For very large n, use thin SVD
        # Sample to keep computation tractable
        if X.shape[0] > 4000:
            idx = np.random.RandomState(42).choice(X.shape[0], 4000, replace=False)
            Xs = X[idx]
        else:
            Xs = X
        # Compute SVD; singular values squared / n_samples = eigenvalues of cov
        # Use scipy/numpy SVD - fast for (4000, 3072) matrix
        s = np.linalg.svd(Xs, compute_uv=False)
        eigs = (s ** 2) / Xs.shape[0]
        eigs_sorted = np.sort(eigs)[::-1]

        pr = participation_ratio(eigs_sorted)
        total = float(eigs_sorted.sum())
        top10 = float(eigs_sorted[:10].sum()) / total if total > 0 else 0.0
        top50 = float(eigs_sorted[:50].sum()) / total if total > 0 else 0.0

        row = {
            "model": model_name,
            "layer": layer,
            "layer_norm": layer / max(n_layers_p1 - 1, 1),
            "hidden_size": hidden,
            "participation_ratio": pr,
            "top10_var_frac": top10,
            "top50_var_frac": top50,
        }
        rows.append(row)

        if layer % 4 == 0 or layer == n_layers_p1 - 1:
            log(
                f"  layer={layer:2d} (norm={row['layer_norm']:.2f}): "
                f"PR={pr:.1f}, top10_var={top10:.3f}, top50_var={top50:.3f}"
            )
    return rows


def main() -> None:
    mcfg = yaml.safe_load((CONFIGS / "models.yaml").read_text())

    all_rows = []
    summary = []
    for model_cfg in mcfg["models"]:
        rows = analyze_model(model_cfg["name"])
        if not rows:
            continue
        all_rows.extend(rows)
        prs = np.array([r["participation_ratio"] for r in rows])
        n = len(prs)
        early = prs[: n // 3].mean()
        middle = prs[n // 3 : 2 * n // 3].mean()
        late = prs[2 * n // 3 :].mean()
        peak_layer = int(np.argmax(prs))
        peak_norm = peak_layer / max(n - 1, 1)
        summary.append(
            {
                "model": model_cfg["name"],
                "n_layers_p1": n,
                "early_PR": early,
                "middle_PR": middle,
                "late_PR": late,
                "PR_peak_layer": peak_layer,
                "PR_peak_norm": peak_norm,
                "PR_peak_value": float(prs[peak_layer]),
                "inverted_U": bool(middle > early and middle > late),
            }
        )
        log(
            f"  {model_cfg['name']}: early={early:.1f}, middle={middle:.1f}, "
            f"late={late:.1f}, peak={peak_layer} (norm={peak_norm:.2f}, PR={prs[peak_layer]:.1f}), "
            f"inverted_U={summary[-1]['inverted_U']}"
        )
        log("")

    df = pd.DataFrame(all_rows)
    out = RESULTS / "middle_layer_geometry.csv"
    df.to_csv(out, index=False)
    log(f"saved {out}")

    sdf = pd.DataFrame(summary)
    sout = RESULTS / "middle_layer_geometry_summary.csv"
    sdf.to_csv(sout, index=False)
    log(f"saved {sout}")

    log("")
    log("Cross-architecture summary:")
    log(sdf.to_string(index=False))
    inv_count = sum(s["inverted_U"] for s in summary)
    log(f"")
    log(f"Inverted-U pattern (middle > early AND middle > late): {inv_count}/{len(summary)} models")


if __name__ == "__main__":
    main()
