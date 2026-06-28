#!/usr/bin/env bash
# Guarda de Clean Architecture: o Domain e a Application são GDScript puro.
# Falha (exit 1) se algum .gd em src/domain ou src/application:
#   - estender um tipo da árvore de cenas (Node/Control/...), ou
#   - referenciar API de cena/UI (get_node/get_tree/add_child/$/.tscn).
# A dependência deve apontar para dentro: Presentation → Application → Domain.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="${PROJECT_OVERRIDE:-$(cd "$HERE/.." && pwd)}"
cd "$PROJECT"

violations=0

scan() {
  local dir="$1"
  [[ -d "$dir" ]] || return 0
  while IFS= read -r f; do
    [[ -z "$f" ]] && continue
    if grep -nE '^[[:space:]]*extends[[:space:]]+(Node|Node2D|Node3D|Control|CanvasItem|Sprite2D|Area2D)\b' "$f" >/dev/null; then
      echo "VIOLAÇÃO [$f]: estende um tipo de cena/UI (Domain/Application deve ser RefCounted/Resource puro)."
      violations=$((violations + 1))
    fi
    if grep -nE '(get_node\(|get_tree\(|add_child\(|\.tscn|\$)' "$f" >/dev/null; then
      echo "VIOLAÇÃO [$f]: referencia API de cena/UI (get_node/get_tree/add_child/\$/.tscn)."
      violations=$((violations + 1))
    fi
  done < <(find "$dir" -name "*.gd")
}

scan "src/domain"
scan "src/application"

if [[ $violations -gt 0 ]]; then
  echo "Guard de arquitetura: $violations violação(ões)."
  exit 1
fi
echo "Guard de arquitetura: OK (Domain/Application puros)."
