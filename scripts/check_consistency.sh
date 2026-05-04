#!/usr/bin/env bash
# Lexical consistency check between PlantUML class diagram and guarded diagrams.
#
# Verifies that every identifier appearing inside guard brackets [...] in the
# state-machine and activity diagrams is either a declared class-diagram
# attribute/method or a reserved token (Boolean operator, environmental
# driver passed as parameter, common loop counter).
#
# Exit status: 0 = consistent, 1 = at least one undeclared identifier.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLASS_DIAGRAM="${ROOT}/plantuml/AedesClassDiagram.puml"
GUARDED=(
  "${ROOT}/plantuml/AedesStateMachine.puml"
  "${ROOT}/plantuml/AedesActivityDiagram.puml"
)

RESERVED='^(AND|OR|NOT|true|false|temp|photoperiod|degreedays|degreeDays|age|density|threshold|cycle|nAND|nOR)$'

# Extract attribute and method identifiers (lines beginning with - or +)
attr_lines=$(grep -E '^\s*[-+]\s+\w+' "$CLASS_DIAGRAM" \
  | sed -E 's/^\s*[-+]\s+([A-Za-z_][A-Za-z0-9_]*).*/\1/')

# Extract enum values (bare identifiers inside `enum Foo { ... }` blocks)
enum_lines=$(awk '
  /^enum / { inenum=1; next }
  inenum && /^\}/ { inenum=0; next }
  inenum && /^[[:space:]]*[A-Za-z_]/ {
    gsub(/^[[:space:]]+|[[:space:]]+$/, "")
    print
  }
' "$CLASS_DIAGRAM")

attrs=$(printf '%s\n%s\n' "$attr_lines" "$enum_lines" | sort -u)

status=0
for f in "${GUARDED[@]}"; do
  [[ -f "$f" ]] || { echo "skip: $f (not found)"; continue; }
  used=$(grep -oE '\[[^][]+\]' "$f" \
    | grep -oE '[A-Za-z_][A-Za-z0-9_]*' \
    | sort -u)
  for id in $used; do
    [[ "$id" =~ $RESERVED ]] && continue
    if ! grep -qx "$id" <<< "$attrs"; then
      echo "WARN: $f references '$id' not declared in $CLASS_DIAGRAM" >&2
      status=1
    fi
  done
done

if [[ $status -eq 0 ]]; then
  echo "Consistency check passed."
fi
exit $status
