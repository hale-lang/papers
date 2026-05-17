#!/usr/bin/env bash
# setup.sh — reproducible environment setup for the
# encoding/decoding asymmetry probing experiment.
#
# Three modes:
#   --install-rocm       Install ROCm 6.4 (interactive, requires sudo)
#   --install-python     Create venv, install pinned Python deps
#   --verify             Verify environment without making changes
#
# Tested on Pop!_OS 24.04 (Ubuntu Noble) with AMD RX 9070 XT
# (RDNA 4 / gfx1201). Should work on Ubuntu 24.04 with minor
# adjustments and on RDNA 3 cards (RX 7000-series) without
# changes.

set -euo pipefail

EXPERIMENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="${EXPERIMENT_DIR}/venv"

# Pinned versions for reproducibility. Update these together
# (PyTorch's ROCm minor version must match the ROCm install).
ROCM_VERSION="6.4"
ROCM_DEB_VERSION="6.4.60400-1"  # bumped occasionally; check repo.radeon.com
PYTORCH_ROCM_INDEX="https://download.pytorch.org/whl/rocm6.4"

usage() {
    cat <<USAGE
Usage: $(basename "$0") [--install-rocm | --install-python | --verify]

  --install-rocm     Install ROCm ${ROCM_VERSION} via amdgpu-install.
                     System-modifying; interactive; requires sudo.
                     A reboot is recommended after this step.

  --install-python   Create a Python venv at ${VENV_DIR} and
                     install pinned dependencies. Idempotent;
                     re-running upgrades to the pinned versions.
                     Does not require sudo.

  --verify           Run sanity checks: ROCm visible, PyTorch
                     sees the GPU, all required packages
                     importable. Read-only; no changes.

Recommended order: --install-rocm  →  reboot  →  --install-python  →  --verify
USAGE
}

log() { echo "[setup] $*" >&2; }
err() { echo "[setup] ERROR: $*" >&2; exit 1; }

# ---------------------------------------------------------------
# ROCm install
# ---------------------------------------------------------------
install_rocm() {
    log "Starting ROCm ${ROCM_VERSION} install for AMD GPUs."
    log "This is system-modifying and requires sudo."

    if [[ "$(. /etc/os-release && echo "${VERSION_CODENAME:-}")" != "noble" ]]; then
        log "WARNING: this script targets Ubuntu Noble (24.04) /"
        log "Pop!_OS 24.04. Detected: ${PRETTY_NAME:-unknown}. Continuing anyway."
    fi

    if command -v rocminfo >/dev/null 2>&1; then
        log "rocminfo already present:"
        rocminfo 2>/dev/null | grep -E "Name:|Marketing Name:" | head -4 || true
        read -rp "[setup] ROCm appears installed. Reinstall? [y/N] " ans
        [[ "${ans:-N}" =~ ^[Yy]$ ]] || { log "Skipping ROCm install."; return 0; }
    fi

    # Step 1: prerequisites
    log "Installing apt prerequisites..."
    sudo apt-get update
    sudo apt-get install -y wget gnupg python3-setuptools python3-wheel \
        libpython3-dev linux-headers-generic

    # Step 2: download amdgpu-install (handles ROCm repo + GPU
    # driver bundle setup; AMD's official install path).
    local AMDGPU_DEB="amdgpu-install_${ROCM_DEB_VERSION}_all.deb"
    local AMDGPU_URL="https://repo.radeon.com/amdgpu-install/${ROCM_VERSION}/ubuntu/noble/${AMDGPU_DEB}"

    log "Downloading ${AMDGPU_URL}..."
    cd /tmp
    wget -q --show-progress "${AMDGPU_URL}" || err "Download failed; check ROCM_DEB_VERSION in setup.sh"

    log "Installing amdgpu-install package (sets up apt repos)..."
    sudo apt-get install -y "/tmp/${AMDGPU_DEB}"
    sudo apt-get update

    # Step 3: install ROCm itself. Use 'rocm' meta-package which
    # pulls compute libraries and HIP runtime, but skips the
    # AMDGPU kernel driver (which Pop!_OS already provides via
    # mesa). This avoids conflicts.
    log "Installing ROCm runtime + libraries (this is several GB)..."
    sudo apt-get install -y rocm

    # Step 4: udev / group permissions for non-sudo GPU access
    log "Adding $(whoami) to render and video groups..."
    sudo usermod -a -G render,video "$(whoami)"

    # Step 5: ensure ROCm binaries are in PATH
    if ! grep -q "/opt/rocm/bin" "${HOME}/.profile" 2>/dev/null; then
        log "Appending ROCm PATH to ~/.profile..."
        cat >>"${HOME}/.profile" <<'PROFILE'

# ROCm — added by encoding_decoding_asymmetry/setup.sh
if [ -d /opt/rocm/bin ]; then
    export PATH="/opt/rocm/bin:${PATH}"
fi
PROFILE
    fi

    log ""
    log "ROCm install complete."
    log ""
    log "NEXT STEPS:"
    log "  1. Reboot the machine (required for kernel driver / group changes)."
    log "  2. After reboot, verify by running:  rocminfo | grep 'Marketing Name'"
    log "  3. Then run:  ./setup.sh --install-python"
}

# ---------------------------------------------------------------
# Python venv + pinned deps
# ---------------------------------------------------------------
install_python() {
    # Pop!_OS / Ubuntu ships system Python without ensurepip /
    # the venv module. Verify the prerequisite before failing
    # with a confusing error from python3 -m venv.
    if ! python3 -c "import ensurepip" 2>/dev/null; then
        err "python3-venv is missing. Install it once with:
        sudo apt install python3.12-venv
Then re-run ./setup.sh --install-python."
    fi

    log "Creating Python venv at ${VENV_DIR}..."

    # If the venv is missing or broken (e.g., a prior failed
    # creation left an empty skeleton), rebuild it from scratch.
    if [[ ! -f "${VENV_DIR}/bin/activate" ]]; then
        if [[ -e "${VENV_DIR}" ]]; then
            log "Existing ${VENV_DIR} is incomplete; removing."
            rm -rf "${VENV_DIR}"
        fi
        python3 -m venv "${VENV_DIR}"
    fi

    if [[ ! -f "${VENV_DIR}/bin/activate" ]]; then
        err "venv creation failed; ${VENV_DIR}/bin/activate is still missing."
    fi

    # shellcheck source=/dev/null
    source "${VENV_DIR}/bin/activate"

    log "Upgrading pip and wheel..."
    pip install --upgrade pip wheel setuptools

    log "Installing PyTorch with ROCm ${ROCM_VERSION} wheels..."
    log "(index: ${PYTORCH_ROCM_INDEX})"
    pip install \
        --index-url "${PYTORCH_ROCM_INDEX}" \
        torch torchvision torchaudio

    log "Installing pinned Python dependencies from requirements.txt..."
    pip install -r "${EXPERIMENT_DIR}/requirements.txt"

    log "Generating lock file at requirements.lock.txt..."
    pip freeze --exclude torch --exclude torchvision --exclude torchaudio \
        > "${EXPERIMENT_DIR}/requirements.lock.txt"
    {
        echo "# Pinned via setup.sh on $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "# torch / torchvision / torchaudio installed from ${PYTORCH_ROCM_INDEX}"
        echo "# (pinned separately because they have ROCm-specific wheels)"
        cat "${EXPERIMENT_DIR}/requirements.lock.txt"
    } > "${EXPERIMENT_DIR}/requirements.lock.txt.new"
    mv "${EXPERIMENT_DIR}/requirements.lock.txt.new" "${EXPERIMENT_DIR}/requirements.lock.txt"

    log ""
    log "Python environment ready."
    log "Activate with:  source ${VENV_DIR}/bin/activate"
    log "Verify with:    ./setup.sh --verify"
}

# ---------------------------------------------------------------
# Verify
# ---------------------------------------------------------------
verify() {
    log "=== Environment verification ==="

    # ROCm
    log "[1/4] ROCm presence..."
    if command -v rocminfo >/dev/null 2>&1; then
        rocminfo 2>/dev/null | grep -E "Name:|Marketing Name:" | head -6 || \
            log "  rocminfo runs but no GPUs reported (may need reboot or group membership)"
    else
        err "rocminfo not found. Run --install-rocm first."
    fi

    # venv exists
    log "[2/4] Python venv..."
    if [[ ! -d "${VENV_DIR}" ]]; then
        err "venv not found at ${VENV_DIR}. Run --install-python first."
    fi
    log "  venv: ${VENV_DIR}"
    # shellcheck source=/dev/null
    source "${VENV_DIR}/bin/activate"

    # PyTorch + GPU
    log "[3/4] PyTorch and GPU detection..."
    python3 - <<'PY'
import sys
try:
    import torch
except ImportError as e:
    print(f"  FAIL: torch not importable ({e})", file=sys.stderr)
    sys.exit(1)
print(f"  torch.__version__   = {torch.__version__}")
print(f"  torch.version.hip   = {torch.version.hip}")
print(f"  torch.version.cuda  = {torch.version.cuda}")
print(f"  cuda.is_available() = {torch.cuda.is_available()}")
if torch.cuda.is_available():
    n = torch.cuda.device_count()
    print(f"  cuda.device_count() = {n}")
    for i in range(n):
        props = torch.cuda.get_device_properties(i)
        print(f"  device[{i}]: {props.name}  mem={props.total_memory / (1024**3):.1f} GB")
else:
    print("  WARN: PyTorch does not see any GPU. Check ROCm install + group membership.", file=sys.stderr)
PY

    # Required packages
    log "[4/4] Required packages..."
    python3 - <<'PY'
required = [
    "transformers", "datasets", "accelerate", "sklearn",
    "numpy", "pandas", "matplotlib", "yaml", "tqdm",
]
import importlib, sys
missing = []
for name in required:
    try:
        m = importlib.import_module(name)
        v = getattr(m, "__version__", "?")
        print(f"  {name:15s} {v}")
    except ImportError:
        missing.append(name)
        print(f"  {name:15s} MISSING", file=sys.stderr)
if missing:
    print(f"FAIL: missing packages: {missing}", file=sys.stderr)
    sys.exit(1)
PY

    log ""
    log "Verification complete. Environment is ready for the experiment."
}

# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------
case "${1:-}" in
    --install-rocm)   install_rocm ;;
    --install-python) install_python ;;
    --verify)         verify ;;
    -h|--help|"")     usage ;;
    *)                usage; exit 1 ;;
esac
