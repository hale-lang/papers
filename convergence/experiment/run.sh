#!/usr/bin/env bash
# run.sh — orchestrate the probing pipeline end-to-end.
#
# Modes:
#   ./run.sh          Full pipeline.
#   ./run.sh --smoke  Quick smoke test: load smallest model, run
#                     ONE forward pass, confirm RDNA 4 kernels work.
#                     ~3 minutes; doesn't touch any cached data.
#   ./run.sh --steps "01 02 03 04 05 06"
#                     Run only specified pipeline stages.

set -euo pipefail

EXPERIMENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${EXPERIMENT_DIR}/venv"

# ---------------------------------------------------------------
# Activate venv + set caches
# ---------------------------------------------------------------
if [[ ! -f "${VENV_DIR}/bin/activate" ]]; then
    echo "[run] FAIL: venv not found at ${VENV_DIR}. Run ./setup.sh --install-python" >&2
    exit 1
fi
# shellcheck source=/dev/null
source "${VENV_DIR}/bin/activate"

# Pin caches to the experiment directory so the run is fully
# self-contained — but DO NOT override HF_HOME, which is where
# huggingface-cli saves the auth token. Overriding HF_HOME makes
# transformers unable to find the token even though `curl` works.
# Instead, redirect only the model + dataset caches.
export HUGGINGFACE_HUB_CACHE="${EXPERIMENT_DIR}/data/cache/hub"
export HF_DATASETS_CACHE="${EXPERIMENT_DIR}/data/cache/hf_datasets"

# Avoid using the iGPU (device 1) by default
export ROCR_VISIBLE_DEVICES=0

# Reduce VRAM fragmentation, especially helpful for Llama-3.1-8B
# which sits at the 16 GB VRAM boundary.
export PYTORCH_HIP_ALLOC_CONF=expandable_segments:True

# Slightly chatty logging
export TRANSFORMERS_VERBOSITY=info

mkdir -p "${HUGGINGFACE_HUB_CACHE}" "${HF_DATASETS_CACHE}"

log() { echo "[run] $*" >&2; }

run_step() {
    local script="$1"
    local label="$2"
    log ""
    log "=========================================="
    log "Stage ${label}: ${script}"
    log "=========================================="
    python3 "${EXPERIMENT_DIR}/src/${script}"
}

# ---------------------------------------------------------------
# Smoke test: ensures the AMD GPU + ROCm + PyTorch actually
# runs a forward pass on a real LLM before committing to a
# multi-hour pipeline. Also doubles as a HuggingFace-auth check.
# ---------------------------------------------------------------
smoke_test() {
    log "Smoke test: loading Llama-3.2-3B and running ONE forward pass..."
    python3 - <<'PY'
import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_id = "meta-llama/Llama-3.2-3B"
print(f"  Loading {model_id} (this requires accepted Meta license + HF token)...")
tok = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id, torch_dtype=torch.bfloat16, device_map={"": "cuda:0"},
    output_hidden_states=True,
)
model.eval()
print(f"  Model loaded. num_hidden_layers={model.config.num_hidden_layers}")

inputs = tok("The capital of France is", return_tensors="pt").to("cuda:0")
print("  Running forward pass...")
with torch.no_grad():
    out = model(**inputs, output_hidden_states=True)
print(f"  hidden_states len = {len(out.hidden_states)}")
print(f"  hidden_states[0].shape = {tuple(out.hidden_states[0].shape)}")
print(f"  hidden_states[-1].shape = {tuple(out.hidden_states[-1].shape)}")
print("  Smoke test PASSED — RDNA 4 forward pass works end-to-end.")
PY
}

# ---------------------------------------------------------------
# Mode dispatch
# ---------------------------------------------------------------
case "${1:-}" in
    --smoke)
        smoke_test
        ;;
    --steps)
        shift
        IFS=' ' read -ra STEPS <<<"${1:-}"
        for s in "${STEPS[@]}"; do
            case "$s" in
                01|01_*) run_step "01_download_data.py" "01-download" ;;
                02|02_*) run_step "02_extract_activations.py" "02-extract" ;;
                03|03_*) run_step "03_train_probes.py" "03-probes" ;;
                04|04_*) run_step "04_compute_widths.py" "04-widths" ;;
                05|05_*) run_step "05_plot.py" "05-plot" ;;
                06|06_*) run_step "06_evaluate_predictions.py" "06-evaluate" ;;
                *) echo "[run] unknown step: $s" >&2; exit 1 ;;
            esac
        done
        ;;
    -h|--help)
        cat <<HELP
Usage: ./run.sh [MODE]

Modes:
  (no flag)              Full pipeline: 01 → 06.
  --smoke                Single-forward-pass smoke test (~3 min).
  --steps "01 02 03"     Run specific stages.

Stages:
  01  download FLORES-200 + XNLI subsets (~5 min)
  02  extract per-layer activations (~60-90 min, GPU)
  03  train per-layer linear probes (~10 min, CPU)
  04  compute w_E, w_D from probe curves
  05  generate plots
  06  generate EVALUATION_REPORT.md
HELP
        ;;
    "")
        # Full pipeline
        run_step "00_verify_env.py" "00-verify"
        run_step "01_download_data.py" "01-download"
        run_step "02_extract_activations.py" "02-extract"
        run_step "03_train_probes.py" "03-probes"
        run_step "04_compute_widths.py" "04-widths"
        run_step "05_plot.py" "05-plot"
        run_step "06_evaluate_predictions.py" "06-evaluate"
        log ""
        log "Pipeline complete. See:"
        log "  results/EVALUATION_REPORT.md"
        log "  results/plots/"
        ;;
    *)
        echo "[run] unknown mode: $1" >&2
        exit 1
        ;;
esac
