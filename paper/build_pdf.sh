#!/usr/bin/env bash
# Build paper/No_Binary_14_3_5.pdf from the LaTeX source and check it.
# Requires Tectonic and Poppler (pdfinfo, pdffonts, pdftotext).
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v tectonic >/dev/null 2>&1; then
  echo "ERROR: Tectonic is required (https://tectonic-typesetting.github.io)" >&2
  exit 2
fi

tectonic No_Binary_14_3_5.tex
python3 pdf_preflight.py No_Binary_14_3_5.pdf
echo "Built paper/No_Binary_14_3_5.pdf"
