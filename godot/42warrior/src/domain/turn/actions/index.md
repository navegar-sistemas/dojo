# `src/domain/turn/actions/` — Comandos do warrior

Os objetos de comando que representam o que o warrior pode fazer em um turno. Modelados
como **tipos** (não strings), para o `ActionApplier` despachar por tipo.

| Arquivo | Classe | Gasta turno? | Parâmetro |
|---|---|---|---|
| `action.gd` | `Action` (base) | — | — |
| `walk_action.gd` | `WalkAction` | sim | `direction` |
| `attack_action.gd` | `AttackAction` | sim | `direction` |
| `rest_action.gd` | `RestAction` | sim | nenhum |

## Notas

- Cada ação consome o turno; os **sentidos** (leitura) ficam em
  [`../../senses/`](../../senses/index.md) e não gastam turno.
- Faltam `RescueAction`, `PivotAction` e `ShootAction` — chegam no **Sprint 2**.
- Quem interpreta cada comando é o `ActionApplier` em [`../`](../index.md).
