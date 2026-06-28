#!/usr/bin/env bash
# Verificação completa do projeto: arquitetura + lint/format + testes.
# Exit não-zero se qualquer etapa falhar.
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

bash "$HERE/arch_guard.sh"
bash "$HERE/lint.sh"
bash "$HERE/test.sh"
echo "== check.sh: tudo verde =="
