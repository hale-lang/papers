#!/usr/bin/env python3
"""Exploratory: does the optimal number of clusters k* vary with depth?

NOT PRE-REGISTERED. Hypothesis (motivated by Section 2.6
sub-classification of P_3): if perimeter layers are
P_3-rich-style (small number of dominant axes, e.g. language
identity at k=6) and middle layers are P_3-chunked or higher
(many distinguishable concept axes simultaneously), then the
*optimal* cluster count k* should differ between layer
regions:

- Perimeter: optimal k ~ 6 (one cluster per language)
- Middle: optimal k ~ 10-30 (many distinguishable concept axes)

Operationalize via silhouette score across k ∈ {6, 12, 20, 50}:
the k that maximizes silhouette is k*. Plot k* vs layer depth.

Output:
  results/optimal_cluster_k.csv

Discipline note: hypothesis-generating. Confirming this as a
formal forward prediction requires fresh pre-registration on a
held-out set of models.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
ACTIVATIONS = EXPERIMENT_ROOT / "results" / "activations"
CONFIGS = EXPERIMENT_ROOT / "configs"
RESULTS = EXPERIMENT_ROOT / "results"

PROBE = "concept"
N_SAMPLES = 2000  # smaller subsample because silhouette is O(n^2)
SEED = 42
K_VALUES = [6, 12, 20, 50]


def log(msg: str) -> None:
    print(f"[opt-k] {msg}", flush=True)


def analyze_model(model_name: str) -> list[dict]:
    act_path = ACTIVATIONS / model_name / PROBE / "activations.npy"
    if not act_path.exists():
        log(f"FAIL: {model_name} missing")
        return []

    log(f"=== {model_name} ===")
    act = np.load(act_path, mmap_mode="r")
    n, n_layers_p1, hidden = act.shape

    rng = np.random.RandomState(SEED)
    idx = rng.choice(n, min(N_SAMPLES, n), replace=False)

    rows = []
    for layer in range(n_layers_p1):
        X = np.asarray(act[idx, layer, :], dtype=np.float32)
        X = X - X.mean(axis=0, keepdims=True)
        # Standardize for k-means stability
        scale = X.std(axis=0)
        scale[scale < 1e-6] = 1.0
        X = X / scale

        sils = {}
        for k in K_VALUES:
            km = KMeans(n_clusters=k, random_state=SEED, n_init=3)
            cl = km.fit_predict(X)
            try:
                sil = silhouette_score(X, cl, sample_size=min(1000, len(X)),
                                       random_state=SEED)
            except Exception:
                sil = float("nan")
            sils[k] = sil

        # Optimal k* among the tested values
        valid = {k: s for k, s in sils.items() if not np.isnan(s)}
        k_star = max(valid, key=valid.get) if valid else None

        row = {
            "model": model_name,
            "layer": layer,
            "layer_norm": layer / max(n_layers_p1 - 1, 1),
            **{f"sil_k{k}": sils[k] for k in K_VALUES},
            "k_star": k_star,
        }
        rows.append(row)

        if layer % 4 == 0 or layer == n_layers_p1 - 1:
            log(
                f"  layer={layer:2d} (norm={row['layer_norm']:.2f}): "
                f"sil(k=6/12/20/50)={sils[6]:.3f}/{sils[12]:.3f}/{sils[20]:.3f}/{sils[50]:.3f}; "
                f"k*={k_star}"
            )
    return rows


def main() -> None:
    mcfg = yaml.safe_load((CONFIGS / "models.yaml").read_text())
    log("Optimal cluster k* by layer (NON-PRE-REGISTERED)")
    log(f"k values tested: {K_VALUES}; subsample n={N_SAMPLES}")

    all_rows = []
    summary = []
    for model_cfg in mcfg["models"]:
        rows = analyze_model(model_cfg["name"])
        if not rows:
            continue
        all_rows.extend(rows)

        df = pd.DataFrame(rows)
        n = len(df)
        early_kstar = df["k_star"].iloc[: n // 3].mode().iloc[0]
        middle_kstar = df["k_star"].iloc[n // 3 : 2 * n // 3].mode().iloc[0]
        late_kstar = df["k_star"].iloc[2 * n // 3 :].mode().iloc[0]
        summary.append(
            {
                "model": model_cfg["name"],
                "early_k_star_mode": int(early_kstar),
                "middle_k_star_mode": int(middle_kstar),
                "late_k_star_mode": int(late_kstar),
                "middle_higher_than_perimeter": bool(
                    middle_kstar > early_kstar and middle_kstar > late_kstar
                ),
            }
        )
        log(f"  {model_cfg['name']}: k*-mode early={early_kstar}, "
            f"middle={middle_kstar}, late={late_kstar}")
        log("")

    df_full = pd.DataFrame(all_rows)
    df_full.to_csv(RESULTS / "optimal_cluster_k.csv", index=False)
    log(f"saved {RESULTS / 'optimal_cluster_k.csv'}")

    sdf = pd.DataFrame(summary)
    sdf.to_csv(RESULTS / "optimal_cluster_k_summary.csv", index=False)
    log(f"saved {RESULTS / 'optimal_cluster_k_summary.csv'}")

    log("")
    log("Cross-architecture summary:")
    log(sdf.to_string(index=False))
    matches = sum(s["middle_higher_than_perimeter"] for s in summary)
    log(f"")
    log(f"Middle k* higher than both perimeters: {matches}/{len(summary)}")


if __name__ == "__main__":
    main()
