#!/usr/bin/env bash
# Build PDFs for both papers from Markdown source.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "[build] convergence/"
"$SCRIPT_DIR/convergence/build.sh"

echo "[build] framework/"
"$SCRIPT_DIR/framework/build.sh"

echo "[build] done"
