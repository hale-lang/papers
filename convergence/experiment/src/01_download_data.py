#!/usr/bin/env python3
"""Download FLORES-200 and XNLI subsets to local cache.

Idempotent: if the processed parquet files already exist, this
script does nothing. To force re-download, delete the
data/processed/ directory.

Output structure:
  data/processed/flores200_lang_id.parquet
    columns: language_code (str), sentence (str), split (train|test)
  data/processed/xnli_concept.parquet
    columns: language_code (str), premise (str), hypothesis (str),
             label (int 0/1/2), split (train|test)
"""

from __future__ import annotations

import sys
import random
from pathlib import Path

import yaml
import pandas as pd
from datasets import load_dataset

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS = EXPERIMENT_ROOT / "configs"
PROCESSED = EXPERIMENT_ROOT / "data" / "processed"


def log(msg: str) -> None:
    print(f"[download] {msg}", flush=True)


def fail(msg: str) -> None:
    print(f"[download] FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def load_config():
    return yaml.safe_load((CONFIGS / "experiment.yaml").read_text())


def download_flores(cfg) -> Path:
    """Download FLORES+ dev split for the configured languages.

    Uses openlanguagedata/flores_plus, which is parquet-based (no
    remote code execution required). The dataset is one big table;
    we filter by (iso_639_3, iso_15924) per language.
    """
    out = PROCESSED / "flores200_lang_id.parquet"
    if out.exists():
        log(f"FLORES+ already at {out} — skipping.")
        return out

    lp = cfg["language_probe"]
    languages = lp["languages"]
    filters = lp["language_filters"]
    examples_per_lang = lp["examples_per_language"]
    test_split = lp["test_split"]
    seed = cfg["seeds"]["global_seed"]
    text_col = lp["dataset"].get("text_column", "text")

    log(f"Downloading FLORES+ {lp['dataset']['split']} split for {len(languages)} languages...")
    log(f"  hub_id: {lp['dataset']['hub_id']}")
    log(f"  languages: {languages}")

    # Single load; filter in-memory per language.
    log("  loading full dataset (one parquet load)...")
    try:
        ds = load_dataset(
            lp["dataset"]["hub_id"],
            split=lp["dataset"]["split"],
            revision=lp["dataset"].get("revision", "main"),
        )
    except Exception as e:
        fail(f"could not load {lp['dataset']['hub_id']}: {e}")

    log(f"  total rows in {lp['dataset']['split']} split: {len(ds)}")
    df_full = ds.to_pandas()

    rows = []
    for lang in languages:
        f = filters[lang]
        mask = (df_full["iso_639_3"] == f["iso_639_3"]) & \
               (df_full["iso_15924"] == f["iso_15924"])
        sub = df_full.loc[mask]
        log(f"  {lang}: {len(sub)} sentences after filter")
        if len(sub) == 0:
            fail(f"no rows match filter {f} for language {lang!r}; "
                 f"check available iso codes in {lp['dataset']['hub_id']}")
        sentences = sub[text_col].iloc[:examples_per_lang].tolist()
        for s in sentences:
            rows.append({"language_code": lang, "sentence": s})

    log(f"Total sentences collected: {len(rows)}")

    # Deterministic train/test split
    random.seed(seed)
    random.shuffle(rows)
    n_test = int(len(rows) * test_split)
    for i, r in enumerate(rows):
        r["split"] = "test" if i < n_test else "train"

    df = pd.DataFrame(rows)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    log(f"Saved {len(df)} rows to {out}")
    log(f"  per-language: {df.groupby('language_code').size().to_dict()}")
    log(f"  per-split:    {df.groupby('split').size().to_dict()}")
    return out


def download_xnli(cfg) -> Path:
    """Download XNLI validation split for the configured languages."""
    out = PROCESSED / "xnli_concept.parquet"
    if out.exists():
        log(f"XNLI already at {out} — skipping.")
        return out

    cp = cfg["concept_probe"]
    languages = cp["languages"]
    examples_per_lang = cp["examples_per_language"]
    test_split = cp["test_split"]
    seed = cfg["seeds"]["global_seed"]

    log(f"Downloading XNLI {cp['dataset']['split']} split for {len(languages)} languages...")
    log(f"  hub_id: {cp['dataset']['hub_id']}")

    rows = []
    for lang in languages:
        log(f"  loading {lang}...")
        try:
            ds = load_dataset(
                cp["dataset"]["hub_id"],
                lang,
                split=cp["dataset"]["split"],
                revision=cp["dataset"].get("revision", "main"),
                trust_remote_code=False,
            )
        except Exception as e:
            fail(f"could not load XNLI for language {lang!r}: {e}")

        n = min(len(ds), examples_per_lang)
        for i in range(n):
            ex = ds[i]
            rows.append({
                "language_code": lang,
                "premise": ex["premise"],
                "hypothesis": ex["hypothesis"],
                "label": int(ex["label"]),
            })

    log(f"Total NLI examples collected: {len(rows)}")

    random.seed(seed + 1)  # different seed from FLORES so splits are independent
    random.shuffle(rows)
    n_test = int(len(rows) * test_split)
    for i, r in enumerate(rows):
        r["split"] = "test" if i < n_test else "train"

    df = pd.DataFrame(rows)
    PROCESSED.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False)
    log(f"Saved {len(df)} rows to {out}")
    log(f"  per-language: {df.groupby('language_code').size().to_dict()}")
    log(f"  per-label:    {df.groupby('label').size().to_dict()}")
    log(f"  per-split:    {df.groupby('split').size().to_dict()}")
    return out


def main() -> None:
    cfg = load_config()
    flores_path = download_flores(cfg)
    xnli_path = download_xnli(cfg)
    log("")
    log("Data download complete.")
    log(f"  Language probe data: {flores_path}")
    log(f"  Concept probe data:  {xnli_path}")


if __name__ == "__main__":
    main()
