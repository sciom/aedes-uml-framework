#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UML="$ROOT/plantuml"
OUT="$ROOT/plantuml/figures"

mkdir -p "$OUT"

echo "▶ Rendering PlantUML diagrams (SVG)..."
plantuml -tsvg -o "$OUT" "$UML"/*.puml

echo "▶ Converting SVG → PDF (Inkscape)..."
for f in "$OUT"/*.svg; do
  inkscape "$f" \
    --export-type=pdf \
    --export-filename="${f%.svg}.pdf" \
    >/dev/null 2>&1
done

echo "✅ All figures generated in $OUT"
