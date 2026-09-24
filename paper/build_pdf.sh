#!/usr/bin/env bash
# Rebuild and mechanically check the manuscript PDF from its Markdown source.
set -euo pipefail
cd "$(dirname "$0")/.."

SOURCE="paper/QEC1435_NO_BINARY_14_3_5.md"
PDF="output/pdf/QEC1435_NO_BINARY_14_3_5.pdf"
PYTHON_BIN="${QEC_PYTHON_BIN:-python3}"

if ! "$PYTHON_BIN" -c 'import reportlab' >/dev/null 2>&1; then
  echo "ERROR: ReportLab is unavailable. Install dependencies from requirements-qec1435.txt or set QEC_PYTHON_BIN." >&2
  exit 2
fi

echo "== Mathematical rendering regression tests =="
"$PYTHON_BIN" paper/test_math_rendering.py

echo "== Build manuscript PDF =="
"$PYTHON_BIN" paper/build_nonexistence_pdf.py --source "$SOURCE" --output "$PDF"

echo "== Check manuscript PDF =="
"$PYTHON_BIN" paper/pdf_preflight.py "$PDF"

echo "Generated: $PDF"
