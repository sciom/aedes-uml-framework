#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UML="$ROOT/plantuml"
OUT="$ROOT/plantuml/figures"

mkdir -p "$OUT"

plantuml -tsvg -o "$OUT" "$UML"/*.puml

for f in "$OUT"/*.svg; do
  inkscape "$f" --export-type=pdf --export-filename="${f%.svg}.pdf" >/dev/null 2>&1
done

echo "✅ Rendered PlantUML figures to: $OUT (SVG + PDF)"
