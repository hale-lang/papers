#!/usr/bin/env bash
# Build prime-torus/paper.pdf from prime-torus/paper.md.
#
# Requires: pandoc, xelatex (or lualatex). Unicode requires a
# Unicode-capable engine.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

ENGINE="${PDF_ENGINE:-xelatex}"
DRAFT_DATE="$(sed -n 's/^date: "\(.*\)"$/\1/p' paper.md | head -1)"

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
  --toc-depth=1 \
  --metadata title='The Tangent Space Cannot See the Discriminant' \
  --metadata author='Riley Rook' \
  --metadata date="$DRAFT_DATE"

echo "[prime-torus] paper.pdf written"
