#!/usr/bin/env python3
"""Train per-layer linear probes for each (model, probe) pair.

For each model and each probe:
 1. Load activations from results/activations/<model>/<probe>/.
 2. For each layer, train a logistic regression probe on
    train activations against the target label.
 3. Evaluate on the test split.
 4. Save per-layer accuracy curve.

Output:
  results/probes/<model_name>/
    language_accuracy.csv     # columns: layer, train_acc, test_acc, n_train, n_test
    concept_accuracy.csv      # same schema

Probes are tiny — sklearn LogisticRegression on hidden_size
features. CPU-only; fast.

Idempotent: skips (model, probe) pairs already on disk.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml
import numpy as np
import pandas as pd
from tqdm import tqdm
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder, StandardScaler

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS = EXPERIMENT_ROOT / "configs"
ACTIVATIONS = EXPERIMENT_ROOT / "results" / "activations"
PROBES = EXPERIMENT_ROOT / "results" / "probes"


def log(msg: str) -> None:
    print(f"[probes] {msg}", flush=True)


def load_configs():
    return (
        yaml.safe_load((CONFIGS / "experiment.yaml").read_text()),
        yaml.safe_load((CONFIGS / "models.yaml").read_text()),
    )


def train_probe_for_layer(X_train: np.ndarray, y_train: np.ndarray,
                          X_test: np.ndarray, y_test: np.ndarray,
                          probe_cfg: dict, seed: int) -> tuple[float, float]:
    """Train one logistic regression probe; return (train_acc, test_acc).

    Standardizes features (zero mean, unit variance per feature)
    using train-set statistics. Standardization is a linear
    transform that does not change which classes are linearly
    separable; it dramatically speeds LBFGS convergence and is
    standard practice in linear-probing interpretability work.
    """
    # Cast fp16 → fp32 for sklearn (does not accept fp16 features)
    Xt = X_train.astype(np.float32)
    Xv = X_test.astype(np.float32)

    # Fit the scaler on training data only; apply to both splits.
    scaler = StandardScaler()
    Xt = scaler.fit_transform(Xt)
    Xv = scaler.transform(Xv)

    clf = LogisticRegression(
        solver=probe_cfg["solver"],
        max_iter=probe_cfg["max_iter"],
        C=probe_cfg["C"],
        random_state=seed,
        n_jobs=-1,
    )
    clf.fit(Xt, y_train)
    train_acc = float(clf.score(Xt, y_train))
    test_acc = float(clf.score(Xv, y_test))
    return train_acc, test_acc


def train_probes_for_model_probe(model_name: str, probe: str, ecfg: dict) -> Path:
    out_dir = PROBES / model_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / f"{probe}_accuracy.csv"
    if out_csv.exists():
        log(f"  {model_name}/{probe}: already done at {out_csv}")
        return out_csv

    act_dir = ACTIVATIONS / model_name / probe
    if not (act_dir / "activations.npy").exists():
        log(f"  {model_name}/{probe}: activations missing at {act_dir}; skipping")
        return out_csv

    activations = np.load(act_dir / "activations.npy")  # (n, n_layers+1, hidden_size)
    metadata = pd.read_parquet(act_dir / "metadata.parquet")

    n_examples, n_layers_plus_1, hidden_size = activations.shape
    log(f"  {model_name}/{probe}: shape={activations.shape}, n_layers+1={n_layers_plus_1}")

    # Determine target labels per probe type
    if probe == "language":
        labels_str = metadata["language_code"].values
        le = LabelEncoder()
        y_all = le.fit_transform(labels_str)
        log(f"    classes (language): {list(le.classes_)}")
    elif probe == "concept":
        # XNLI labels: 0=entailment, 1=neutral, 2=contradiction
        y_all = metadata["label"].values.astype(int)
        log(f"    classes (concept): entailment(0), neutral(1), contradiction(2)")
    else:
        raise ValueError(probe)

    # Train/test split (already encoded in metadata.split)
    train_mask = (metadata["split"].values == "train")
    test_mask = (metadata["split"].values == "test")
    n_train = int(train_mask.sum())
    n_test = int(test_mask.sum())
    log(f"    n_train={n_train}, n_test={n_test}")

    rows = []
    seed = ecfg["seeds"]["probe_seed"]
    probe_cfg = ecfg["probe_training"]

    for layer in tqdm(range(n_layers_plus_1), desc=f"  layers({probe})", file=sys.stdout):
        X = activations[:, layer, :]  # (n, hidden_size)
        train_acc, test_acc = train_probe_for_layer(
            X[train_mask], y_all[train_mask],
            X[test_mask], y_all[test_mask],
            probe_cfg, seed,
        )
        rows.append({
            "layer": layer,
            "train_acc": train_acc,
            "test_acc": test_acc,
            "n_train": n_train,
            "n_test": n_test,
        })

    df = pd.DataFrame(rows)
    df.to_csv(out_csv, index=False)
    log(f"  saved {out_csv}")
    log(f"    test_acc range across layers: [{df['test_acc'].min():.3f}, {df['test_acc'].max():.3f}]")
    return out_csv


def main() -> None:
    ecfg, mcfg = load_configs()

    log(f"Probes directory: {PROBES}")
    for model_cfg in mcfg["models"]:
        model_name = model_cfg["name"]
        log(f"=== {model_name} ===")
        for probe in ("language", "concept"):
            train_probes_for_model_probe(model_name, probe, ecfg)

    log("")
    log("All probes trained.")


if __name__ == "__main__":
    main()
