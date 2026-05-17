#!/usr/bin/env python3
"""Extract per-layer hidden states for each model on each probe sentence.

For each (model, probe_dataset) pair:
  1. Load the model with output_hidden_states=True.
  2. For each example, run a forward pass.
  3. Extract the hidden state at the last non-pad token position
     for each layer.
  4. Save to disk as a numpy memmap, plus a metadata parquet.

Output structure:
  results/activations/<model_name>/
    language/
      activations.npy        # shape (n_examples, n_layers+1, hidden_size) fp16
      metadata.parquet       # row index → (language_code, split)
    concept/
      activations.npy        # shape (n_examples, n_layers+1, hidden_size) fp16
      metadata.parquet       # row index → (language_code, label, split)

Note: n_layers+1 because we include the embedding layer (layer 0)
plus n_layers transformer blocks.

Idempotent: skips (model, probe) pairs already on disk. Resume
from interruption is per-(model, probe) granularity (not
per-example, to keep the script simple).

Memory management:
 - Models loaded one at a time; old model freed before next loads.
 - bf16 model weights (~14-16 GB for 7-8B); activations
   collected in fp16 then saved.
 - Streaming, batch size 1; total VRAM peak ~17 GB during
   generation (model + per-step activations).
"""

from __future__ import annotations

import gc
import sys
import random
from pathlib import Path

import yaml
import numpy as np
import pandas as pd
import torch
from tqdm import tqdm
# AutoModel (base transformer) rather than AutoModelForCausalLM:
# we only need per-layer hidden states for probing, not the
# language-modeling head. For models with untied lm_head (e.g.,
# Llama-3.1-8B), this saves ~1 GB of VRAM — enough to make the
# 8B model fit on a 16 GB card.
from transformers import AutoTokenizer, AutoModel

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS = EXPERIMENT_ROOT / "configs"
PROCESSED = EXPERIMENT_ROOT / "data" / "processed"
ACTIVATIONS = EXPERIMENT_ROOT / "results" / "activations"


def log(msg: str) -> None:
    print(f"[extract] {msg}", flush=True)


def load_configs():
    return (
        yaml.safe_load((CONFIGS / "experiment.yaml").read_text()),
        yaml.safe_load((CONFIGS / "models.yaml").read_text()),
    )


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def get_dtype(name: str):
    return {"bfloat16": torch.bfloat16, "float16": torch.float16}[name]


def already_done(model_name: str, probe: str) -> bool:
    out_dir = ACTIVATIONS / model_name / probe
    return (out_dir / "activations.npy").exists() and (out_dir / "metadata.parquet").exists()


def load_probe_data(probe: str, cfg) -> pd.DataFrame:
    if probe == "language":
        df = pd.read_parquet(PROCESSED / "flores200_lang_id.parquet")
        df["text"] = df["sentence"]
    elif probe == "concept":
        df = pd.read_parquet(PROCESSED / "xnli_concept.parquet")
        # For concept probing, use premise + hypothesis concatenated.
        # The probe predicts the entailment label from the joint
        # representation, so we need both segments visible.
        df["text"] = df["premise"] + " </s> " + df["hypothesis"]
    else:
        raise ValueError(f"unknown probe: {probe!r}")
    return df.reset_index(drop=True)


def extract_for_model(model_cfg: dict, ecfg: dict) -> None:
    model_name = model_cfg["name"]
    hub_id = model_cfg["hub_id"]
    revision = model_cfg.get("revision", "main")
    dtype = get_dtype(model_cfg.get("dtype", "bfloat16"))
    device = ecfg["extraction"]["device"]
    max_seq = ecfg["extraction"]["max_seq_length"]

    log(f"=== Model: {model_name} ({hub_id}) ===")

    # Skip if both probes already done
    if already_done(model_name, "language") and already_done(model_name, "concept"):
        log(f"  both probes already extracted; skipping {model_name}")
        return

    # Load tokenizer + model
    log(f"  loading tokenizer from {hub_id}...")
    tokenizer = AutoTokenizer.from_pretrained(hub_id, revision=revision)
    if tokenizer.pad_token is None:
        # Decoder-only models often lack a pad token; use EOS for padding
        tokenizer.pad_token = tokenizer.eos_token

    log(f"  loading model in {dtype}...")
    model = AutoModel.from_pretrained(
        hub_id,
        revision=revision,
        torch_dtype=dtype,
        device_map={"": device},
        output_hidden_states=True,
    )
    model.eval()

    n_layers = model.config.num_hidden_layers
    hidden_size = model.config.hidden_size
    log(f"  num_hidden_layers: {n_layers}  hidden_size: {hidden_size}")

    for probe in ("language", "concept"):
        if already_done(model_name, probe):
            log(f"  probe={probe} already done; skipping")
            continue

        out_dir = ACTIVATIONS / model_name / probe
        out_dir.mkdir(parents=True, exist_ok=True)

        df = load_probe_data(probe, ecfg)
        n = len(df)
        log(f"  probe={probe}  n_examples={n}")

        # Allocate output array. Shape: (n, n_layers+1, hidden_size).
        # Stored as fp16 to halve disk size; conversion is lossy at the
        # ~0.001 level which is below probe-noise.
        acts = np.zeros((n, n_layers + 1, hidden_size), dtype=np.float16)

        with torch.no_grad():
            for i in tqdm(range(n), desc=f"  forward({probe})", file=sys.stdout):
                text = df.iloc[i]["text"]
                inputs = tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=max_seq,
                ).to(device)

                outputs = model(**inputs, output_hidden_states=True)
                # outputs.hidden_states is a tuple of (n_layers+1) tensors,
                # each of shape (batch=1, seq_len, hidden_size).

                # Index of the last non-pad token (== seq_len - 1 since
                # we're not padding in batch=1; just truncating).
                last_idx = inputs.attention_mask[0].sum().item() - 1

                for layer_i, h in enumerate(outputs.hidden_states):
                    # h: (1, seq_len, hidden_size)
                    vec = h[0, last_idx, :].to(torch.float32).cpu().numpy()
                    acts[i, layer_i, :] = vec.astype(np.float16)

                # Free batch tensors aggressively
                del outputs, inputs

        # Save
        np.save(out_dir / "activations.npy", acts)
        meta_cols = ["language_code", "split"]
        if probe == "concept":
            meta_cols.append("label")
        df[meta_cols].to_parquet(out_dir / "metadata.parquet", index=False)
        log(f"  saved {acts.shape} to {out_dir}")

    # Free the model before loading the next one
    del model, tokenizer
    gc.collect()
    torch.cuda.empty_cache()


def main() -> None:
    ecfg, mcfg = load_configs()
    set_seed(ecfg["seeds"]["global_seed"])

    # Confirm probe data is downloaded
    for fname in ("flores200_lang_id.parquet", "xnli_concept.parquet"):
        p = PROCESSED / fname
        if not p.exists():
            log(f"FAIL: {p} not found. Run src/01_download_data.py first.")
            sys.exit(1)

    log(f"Models to process: {[m['name'] for m in mcfg['models']]}")
    log(f"Activations directory: {ACTIVATIONS}")

    for model_cfg in mcfg["models"]:
        extract_for_model(model_cfg, ecfg)

    log("")
    log("Activation extraction complete for all models.")


if __name__ == "__main__":
    main()
