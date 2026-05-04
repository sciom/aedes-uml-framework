#!/usr/bin/env bash
# Render supplementary Markdown files to PDF using Pandoc + XeLaTeX.
#
# Output PDFs are written next to the .md sources in /supplementary.
# Run from anywhere; the script resolves its own location.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUPP_DIR="${SCRIPT_DIR}/../supplementary"

cd "${SUPP_DIR}"

shopt -s nullglob
files=( S?_*.md )
if (( ${#files[@]} == 0 )); then
  echo "No S?_*.md files found in ${SUPP_DIR}" >&2
  exit 1
fi

for f in "${files[@]}"; do
  out="${f%.md}.pdf"
  echo "Rendering ${f} -> ${out}"
  pandoc "${f}" -o "${out}" \
    --pdf-engine=xelatex \
    -V geometry:margin=2.5cm \
    -V mainfont="DejaVu Serif" \
    -V monofont="DejaVu Sans Mono" \
    -V colorlinks=true \
    -V linkcolor=blue \
    -V urlcolor=blue \
    --toc
done

echo "Done. Rendered ${#files[@]} file(s)."
