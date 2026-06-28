# `scripts/` — Scripts de qualidade

Verificações executáveis do projeto. Todos descobrem o Godot via `godot_env.sh`
(use `GODOT_BIN` para sobrescrever o caminho).

| Arquivo | O que faz |
|---|---|
| `godot_env.sh` | Helper: localiza o executável do Godot e põe o gdtoolkit no PATH. Não roda sozinho — é `source`-ado pelos outros. |
| `test.sh` | Roda os testes de domínio (GUT, headless). Importa os recursos num checkout limpo. |
| `lint.sh` | `gdformat --check` + `gdlint` sobre `src/` e `test/`. |
| `arch_guard.sh` | Falha se `src/domain` ou `src/application` usarem a engine (`extends Node`, `get_node`, `$`, `.tscn`...). |
| `check.sh` | Roda tudo acima de uma vez (a verificação completa). |

## Uso

```bash
bash scripts/check.sh   # arch_guard + lint + testes
```

Saída esperada: guard OK, lint OK, todos os testes passando, `== check.sh: tudo verde ==`.

> Estes comandos também estão declarados na spec do projeto
> (`specs/project/conventions.ts`), que o gate de revisão executa.
