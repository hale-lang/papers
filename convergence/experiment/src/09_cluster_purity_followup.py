#!/usr/bin/env python3
"""Exploratory: per-layer cluster purity for language vs concept structure.

NOT PRE-REGISTERED. Hypothesis (motivated by Ng 2026
"LLM Neuroanatomy III: Sapir-Whorf"): early and late layers
organize representations by *language identity* (format-
specific surface), while middle layers organize by *concept*
(format-agnostic semantic manifold). Ng establishes this
qualitatively via cosine-similarity comparisons and 2D PCA.

This script complements Ng with a *quantitative cross-
architecture* measurement of the same transition. For each
model and each layer, run k-means clustering on the activation
space and compute two cluster-quality metrics:

- NMI(clusters, language_code): how well do unsupervised
  clusters in activation space recover the language label?
- NMI(clusters, xnli_label): how well do they recover the
  semantic concept label?

The framework's prediction: NMI_lang should be high at the
perimeter (where format-specificity dominates) and lower in
the middle; NMI_concept should peak in the middle (where
semantic abstraction is happening). The cross-over pattern
would be the framework's mechanism-2/3 transition signature
made visible through unsupervised cluster structure.

Output:
  results/cluster_purity.csv
  results/CLUSTER_PURITY_REPORT.md

Discipline note: this is exploratory follow-up, not pre-
registered. Status: complementary quantitative measurement of
a phenomenon Ng (2026) established qualitatively.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import yaml
from sklearn.cluster import KMeans
from sklearn.metrics import normalized_mutual_info_score
from sklearn.preprocessing import LabelEncoder

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
ACTIVATIONS = EXPERIMENT_ROOT / "results" / "activations"
CONFIGS = EXPERIMENT_ROOT / "configs"
RESULTS = EXPERIMENT_ROOT / "results"

PROBE = "concept"  # XNLI activations include both language and label metadata
N_SAMPLES = 4000   # subsample for k-means tractability
SEED = 42


def log(msg: str) -> None:
    print(f"[cluster-purity] {msg}", flush=True)


def analyze_model(model_name: str) -> list[dict]:
    """Return per-layer cluster-purity stats for one model."""
    act_dir = ACTIVATIONS / model_name / PROBE
    act_path = act_dir / "activations.npy"
    meta_path = act_dir / "metadata.parquet"

    if not act_path.exists() or not meta_path.exists():
        log(f"FAIL: {model_name} activations or metadata missing")
        return []

    log(f"=== {model_name} ===")
    act = np.load(act_path, mmap_mode="r")
    meta = pd.read_parquet(meta_path)
    n, n_layers_p1, hidden = act.shape
    log(f"  shape={act.shape}, dtype={act.dtype}")

    # Subsample
    rng = np.random.RandomState(SEED)
    idx = rng.choice(n, min(N_SAMPLES, n), replace=False)
    lang_le = LabelEncoder()
    y_lang = lang_le.fit_transform(meta["language_code"].values[idx])
    y_concept = meta["label"].values[idx].astype(int)
    n_lang = len(lang_le.classes_)
    n_concept = len(np.unique(y_concept))
    log(f"  sample n={len(idx)}, n_lang={n_lang}, n_concept={n_concept}")

    rows = []
    for layer in range(n_layers_p1):
        X = np.asarray(act[idx, layer, :], dtype=np.float32)
        X = X - X.mean(axis=0, keepdims=True)

        # k-means at k = n_lang (6) — competing with language structure
        km_lang = KMeans(n_clusters=n_lang, random_state=SEED, n_init=4)
        cl_lang = km_lang.fit_predict(X)
        nmi_lang_k6 = normalized_mutual_info_score(y_lang, cl_lang)
        nmi_concept_k6 = normalized_mutual_info_score(y_concept, cl_lang)

        # k-means at k = n_concept (3) — competing with concept structure
        km_concept = KMeans(n_clusters=n_concept, random_state=SEED, n_init=4)
        cl_concept = km_concept.fit_predict(X)
        nmi_lang_k3 = normalized_mutual_info_score(y_lang, cl_concept)
        nmi_concept_k3 = normalized_mutual_info_score(y_concept, cl_concept)

        row = {
            "model": model_name,
            "layer": layer,
            "layer_norm": layer / max(n_layers_p1 - 1, 1),
            "nmi_lang_k6": nmi_lang_k6,
            "nmi_concept_k6": nmi_concept_k6,
            "nmi_lang_k3": nmi_lang_k3,
            "nmi_concept_k3": nmi_concept_k3,
        }
        rows.append(row)

        if layer % 4 == 0 or layer == n_layers_p1 - 1:
            log(
                f"  layer={layer:2d} (norm={row['layer_norm']:.2f}): "
                f"NMI_lang(k=6)={nmi_lang_k6:.3f}, NMI_concept(k=3)={nmi_concept_k3:.3f}"
            )
    return rows


def main() -> None:
    mcfg = yaml.safe_load((CONFIGS / "models.yaml").read_text())

    log("Per-layer cluster purity (NON-PRE-REGISTERED EXPLORATORY)")
    log(f"k=6 against language_code; k=3 against XNLI label; subsample n={N_SAMPLES}")

    all_rows = []
    summary = []
    for model_cfg in mcfg["models"]:
        rows = analyze_model(model_cfg["name"])
        if not rows:
            continue
        all_rows.extend(rows)

        # Summary stats per model
        df = pd.DataFrame(rows)
        n = len(df)
        # Cross-over signature: where does NMI_lang dominate vs NMI_concept?
        # Use the more informative pairing: NMI_lang(k=6) vs NMI_concept(k=3).
        df_sorted = df.sort_values("layer")
        lang_vals = df_sorted["nmi_lang_k6"].values
        concept_vals = df_sorted["nmi_concept_k3"].values

        early_lang = lang_vals[: n // 3].mean()
        middle_lang = lang_vals[n // 3 : 2 * n // 3].mean()
        late_lang = lang_vals[2 * n // 3 :].mean()
        early_concept = concept_vals[: n // 3].mean()
        middle_concept = concept_vals[n // 3 : 2 * n // 3].mean()
        late_concept = concept_vals[2 * n // 3 :].mean()

        # Layer at which concept NMI peaks
        concept_peak_layer = int(np.argmax(concept_vals))
        concept_peak_norm = concept_peak_layer / max(n - 1, 1)
        concept_peak_value = float(concept_vals[concept_peak_layer])

        summary.append(
            {
                "model": model_cfg["name"],
                "n_layers_p1": n,
                "early_NMI_lang": early_lang,
                "middle_NMI_lang": middle_lang,
                "late_NMI_lang": late_lang,
                "early_NMI_concept": early_concept,
                "middle_NMI_concept": middle_concept,
                "late_NMI_concept": late_concept,
                "concept_NMI_peak_layer": concept_peak_layer,
                "concept_NMI_peak_norm": concept_peak_norm,
                "concept_NMI_peak_value": concept_peak_value,
            }
        )
        log(
            f"  {model_cfg['name']}: "
            f"NMI_lang(early/mid/late)={early_lang:.3f}/{middle_lang:.3f}/{late_lang:.3f}; "
            f"NMI_concept(early/mid/late)={early_concept:.3f}/{middle_concept:.3f}/{late_concept:.3f}; "
            f"concept-NMI peak at layer {concept_peak_layer} (norm={concept_peak_norm:.2f}, "
            f"NMI={concept_peak_value:.3f})"
        )
        log("")

    df_full = pd.DataFrame(all_rows)
    out = RESULTS / "cluster_purity.csv"
    df_full.to_csv(out, index=False)
    log(f"saved {out}")

    sdf = pd.DataFrame(summary)
    sout = RESULTS / "cluster_purity_summary.csv"
    sdf.to_csv(sout, index=False)
    log(f"saved {sout}")

    log("")
    log("Cross-architecture summary:")
    log(sdf.to_string(index=False))


if __name__ == "__main__":
    main()
