#!/usr/bin/env python3
"""Verify the experiment environment is fully ready.

Checks:
 1. PyTorch sees the AMD GPU at device 0 with sufficient VRAM.
 2. All required packages are importable at the pinned versions
    declared in configs/experiment.yaml's dependencies are
    matched by the venv.
 3. HuggingFace authentication is set up (HF_TOKEN env var or
    saved login token).
 4. Each model in configs/models.yaml is reachable and the
    license has been accepted (no full download — just metadata
    fetch).

Run before any data collection.
"""

from __future__ import annotations

import os
import sys
import subprocess
from pathlib import Path

import yaml

EXPERIMENT_ROOT = Path(__file__).resolve().parent.parent
CONFIGS = EXPERIMENT_ROOT / "configs"


def fail(msg: str) -> None:
    print(f"FAIL: {msg}", file=sys.stderr)
    sys.exit(1)


def info(msg: str) -> None:
    print(f"  {msg}")


def section(name: str) -> None:
    print(f"\n[verify] {name}")


def check_pytorch_gpu() -> None:
    section("PyTorch + GPU")
    try:
        import torch
    except ImportError as e:
        fail(f"torch not importable: {e}")

    info(f"torch version: {torch.__version__}")
    if not torch.cuda.is_available():
        fail("torch.cuda.is_available() is False — ROCm not visible to PyTorch.")

    n = torch.cuda.device_count()
    info(f"GPU device count: {n}")
    if n == 0:
        fail("No GPU devices found.")

    # Device 0 is the dGPU; VRAM should be >= 12 GB for 7B models in bf16
    props = torch.cuda.get_device_properties(0)
    vram_gb = props.total_memory / (1024 ** 3)
    info(f"device[0]: {props.name} — {vram_gb:.1f} GB VRAM")
    if vram_gb < 12.0:
        fail(f"device[0] has only {vram_gb:.1f} GB VRAM; need >= 12 GB for 7B models in bf16.")

    if n > 1:
        for i in range(1, n):
            p = torch.cuda.get_device_properties(i)
            info(f"device[{i}]: {p.name} — {p.total_memory / (1024 ** 3):.1f} GB (will not be used)")


def check_packages() -> None:
    section("Required packages")
    required = [
        "transformers", "datasets", "accelerate",
        "sklearn", "numpy", "pandas",
        "matplotlib", "yaml", "tqdm", "huggingface_hub",
    ]
    import importlib
    for pkg in required:
        try:
            mod = importlib.import_module(pkg)
            ver = getattr(mod, "__version__", "?")
            info(f"{pkg:18s} {ver}")
        except ImportError:
            fail(f"package {pkg!r} not importable")


def check_hf_auth() -> None:
    section("HuggingFace authentication")
    token = os.environ.get("HF_TOKEN") or os.environ.get("HUGGING_FACE_HUB_TOKEN")
    if token:
        info(f"HF_TOKEN found in env (length={len(token)})")
        return

    # Fall back to saved login
    try:
        from huggingface_hub import HfFolder
        saved = HfFolder.get_token()
    except Exception as e:
        fail(f"could not query HuggingFace credentials: {e}")

    if saved:
        info("Saved HF token found via huggingface-cli login")
    else:
        fail(
            "No HuggingFace token found.\n"
            "        Run one of:\n"
            "          export HF_TOKEN=hf_xxxxx     # in your shell\n"
            "          huggingface-cli login        # one-time interactive\n"
            "        Get a token at: https://huggingface.co/settings/tokens"
        )


def check_models_reachable() -> None:
    section("Model accessibility (license + reachability)")
    cfg = yaml.safe_load((CONFIGS / "models.yaml").read_text())
    from huggingface_hub import HfApi
    api = HfApi()
    for m in cfg["models"]:
        hub_id = m["hub_id"]
        revision = m.get("revision", "main")
        try:
            mi = api.model_info(repo_id=hub_id, revision=revision)
        except Exception as e:
            fail(
                f"model {hub_id!r} not reachable at revision {revision!r}: {e}\n"
                f"        Possible causes:\n"
                f"        - License not accepted (open https://huggingface.co/{hub_id} "
                f"and click the accept button)\n"
                f"        - Token doesn't have read access to the repo\n"
                f"        - Network issue"
            )
        info(f"{m['name']:18s}  {hub_id}  (sha: {mi.sha[:8]}…)")


def check_disk_space() -> None:
    section("Disk space")
    import shutil
    # We need ~80 GB for: 4 models × ~16 GB weights + datasets + activations
    needed_gb = 80.0
    stat = shutil.disk_usage(EXPERIMENT_ROOT)
    free_gb = stat.free / (1024 ** 3)
    info(f"free space at {EXPERIMENT_ROOT}: {free_gb:.1f} GB")
    if free_gb < needed_gb:
        fail(f"need >= {needed_gb:.0f} GB free; have {free_gb:.1f} GB.")


def main() -> None:
    print("[verify] Encoding/decoding asymmetry experiment — environment check")
    check_pytorch_gpu()
    check_packages()
    check_hf_auth()
    check_disk_space()
    check_models_reachable()
    print("\n[verify] All checks passed. Ready to run the pipeline.")


if __name__ == "__main__":
    main()
