#!/usr/bin/env bash
# Roda a suíte de testes de domínio (GUT) em modo headless e propaga o exit code.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/godot_env.sh"
GODOT="$(resolve_godot)"
PROJECT="${PROJECT_OVERRIDE:-$(cd "$HERE/.." && pwd)}"

# Reimport incremental garante que arquivos .gd criados após o import inicial
# sejam registrados no filesystem virtual do Godot (evita silêncio de testes novos).
"$GODOT" --headless --path "$PROJECT" --import >/dev/null 2>&1 || true

"$GODOT" --headless --path "$PROJECT" \
  -s res://addons/gut/gut_cmdln.gd \
  -gdir=res://test -ginclude_subdirs -gexit
