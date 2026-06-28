#!/usr/bin/env bash
# Roda a suíte de testes de domínio (GUT) em modo headless e propaga o exit code.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/godot_env.sh"
GODOT="$(resolve_godot)"
PROJECT="$(cd "$HERE/.." && pwd)"

# Garante que os recursos (incl. class_names do GUT) estejam importados num checkout limpo.
if [[ ! -d "$PROJECT/.godot/imported" ]]; then
  "$GODOT" --headless --path "$PROJECT" --import >/dev/null 2>&1 || true
fi

"$GODOT" --headless --path "$PROJECT" \
  -s res://addons/gut/gut_cmdln.gd \
  -gdir=res://test -ginclude_subdirs -gexit
