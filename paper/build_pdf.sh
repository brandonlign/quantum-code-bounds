#!/usr/bin/env bash
# Compile the authoritative LaTeX manuscript and check the resulting PDF.
set -euo pipefail

cd "$(dirname "$0")/.."

SOURCE="paper/QEC1435_NO_BINARY_14_3_5.tex"
PDF="output/pdf/QEC1435_NO_BINARY_14_3_5.pdf"

if ! command -v tectonic >/dev/null 2>&1; then
  echo "ERROR: Tectonic is required to compile $SOURCE" >&2
  exit 2
fi

mkdir -p output/pdf
echo "== Compile LaTeX manuscript =="
tectonic --outdir output/pdf "$SOURCE"

echo "== Check manuscript PDF =="
python3 paper/pdf_preflight.py "$PDF"

echo "Generated: $PDF"
