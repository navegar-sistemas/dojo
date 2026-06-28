#!/usr/bin/env bash
# Verifica formatação (gdformat) e lint (gdlint) do código do jogo.
# Escopo: src/ e test/ (o addon de terceiros addons/gut não entra).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$HERE/godot_env.sh"
ensure_gdtoolkit_path
PROJECT="${PROJECT_OVERRIDE:-$(cd "$HERE/.." && pwd)}"
cd "$PROJECT"

targets=()
[[ -d src ]] && targets+=("src")
[[ -d test ]] && targets+=("test")
if [[ ${#targets[@]} -eq 0 ]]; then
  echo "Nenhum diretório src/ ou test/ ainda — nada a verificar."
  exit 0
fi

if ! find "${targets[@]}" -name "*.gd" -print -quit | grep -q .; then
  echo "Nenhum .gd em ${targets[*]} ainda — nada a verificar."
  exit 0
fi

echo "== gdformat --check =="
gdformat --check "${targets[@]}"
echo "== gdlint =="
gdlint "${targets[@]}"
echo "Lint OK."
