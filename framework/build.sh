#!/usr/bin/env bash
# Build framework/paper.pdf from framework/paper.md.
#
# Requires: pandoc, xelatex (or lualatex). Unicode (k̄, φ, σ, log₂)
# requires a Unicode-capable engine.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

ENGINE="${PDF_ENGINE:-xelatex}"

pandoc paper.md \
  --output paper.pdf \
  --pdf-engine="$ENGINE" \
  --bibliography references.bib \
  --citeproc \
  --variable=geometry:margin=1in \
  --variable=fontsize:11pt \
  --variable=mainfont:'Latin Modern Roman' \
  --variable=monofont:'Latin Modern Mono' \
  --variable=colorlinks:true \
  --variable=linkcolor:NavyBlue \
  --variable=urlcolor:NavyBlue \
  --variable=citecolor:NavyBlue \
  --toc \
  --toc-depth=2 \
  --metadata title='A Capacity-Allocation Framework for Coordinated Systems' \
  --metadata author='Riley Rook' \
  --metadata date='2026-05-16'

echo "[framework] paper.pdf written"
