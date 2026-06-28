# `test/` — Testes automatizados

Testes do domínio com o framework **GUT** (headless). Todos determinísticos, sem
dependência de cena/render. Rode com `bash scripts/test.sh`.

## `test/domain/`

| Arquivo | Cobre |
|---|---|
| `test_smoke.gd` | Teste mínimo que confirma que o runner funciona. |
| `test_direction.gd` | Sinal relativo e oposto da direção. |
| `test_units.gd` | Atributos de cada unidade e imutabilidade do dano. |
| `test_space_and_level_state.gd` | Consultas e imutabilidade do estado. |
| `test_senses.gd` | feel / look / listen / direction_of_stairs. |
| `test_actions.gd` | Os objetos de comando. |
| `test_behaviors.gd` | IA melee / ranged (com bloqueio de linha) / inert. |
| `test_turn_resolver.gd` | Turno completo: efeitos, vitória, derrota, determinismo. |

**Estado:** 51 asserções, todas verdes.

## Convenção

Cada arquivo de teste estende `GutTest` e tem funções `test_*`. A organização espelha o
domínio (um arquivo de teste por área de regra).
