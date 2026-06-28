# `src/domain/combat/` — Combate e IA dos inimigos

Como cada unidade age no seu turno (a "inteligência" dos inimigos) e como aplicar essa
reação ao estado. A IA é escolhida por **polimorfismo** — nada de `if (tipo == ...)`.

| Arquivo | Classe | Responsabilidade |
|---|---|---|
| `unit_behavior.gd` | `UnitBehavior` (base) | Contrato: *quanto de dano esta unidade causa ao warrior neste turno?* (base = 0). |
| `melee_behavior.gd` | `MeleeBehavior` | Ataca se o warrior está **adjacente** (sludge, thick sludge). |
| `ranged_behavior.gd` | `RangedBehavior` | Ataca **à distância** dentro do alcance, se a linha de tiro não estiver bloqueada por outra unidade (archer, wizard). |
| `inert_behavior.gd` | `InertBehavior` | Não age (cativo). |
| `enemy_phase.gd` | `EnemyPhase` | Após a ação do warrior, faz cada inimigo vivo agir (em ordem de posição = determinístico), acumulando dano e eventos. |

## Notas

- Adicionar um inimigo novo = uma nova classe de comportamento, sem tocar no resto.
- A ordenação por posição garante **determinismo** na fase dos inimigos.
- Quem decide qual comportamento cada unidade usa é o `create_behavior()` em
  [`../units/`](../units/index.md).
