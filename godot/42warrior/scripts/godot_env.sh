#!/usr/bin/env bash
# Descobre o executável do Godot 4 e o diretório de binários do gdtoolkit.
# Fonte única: variável GODOT_BIN (se exportada) tem prioridade; caso contrário
# tenta o godot no PATH e, por fim, locais conhecidos. Falha-alto se não achar —
# nunca usa um caminho-fantasma silencioso.
set -euo pipefail

resolve_godot() {
  if [[ -n "${GODOT_BIN:-}" ]]; then
    echo "$GODOT_BIN"
    return 0
  fi
  if command -v godot >/dev/null 2>&1; then
    command -v godot
    return 0
  fi
  local candidates=(
    "$HOME/Downloads/Godot.app/Contents/MacOS/Godot"
    "/Applications/Godot.app/Contents/MacOS/Godot"
    "$HOME/Applications/Godot.app/Contents/MacOS/Godot"
  )
  local c
  for c in "${candidates[@]}"; do
    if [[ -x "$c" ]]; then
      echo "$c"
      return 0
    fi
  done
  echo "ERRO: Godot não encontrado. Exporte GODOT_BIN=/caminho/para/Godot." >&2
  return 1
}

# Garante que gdformat/gdlint (gdtoolkit, instalado via pip --user) estejam no PATH.
ensure_gdtoolkit_path() {
  local pybin="$HOME/Library/Python/3.9/bin"
  if [[ -d "$pybin" ]]; then
    export PATH="$pybin:$PATH"
  fi
}
