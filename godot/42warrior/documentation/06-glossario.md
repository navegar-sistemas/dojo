# 06 — Glossário (Ruby Warrior ↔ 42 Warrior)

Tradução dos conceitos do jogo original para os nomes usados neste projeto.

## Conceitos

| Ruby Warrior | Neste projeto | O que é |
|---|---|---|
| `play_turn(warrior)` | (Sprint 2) `PlayerScriptRunner` + `WarriorFacade` | a lógica que o jogador escreve, chamada uma vez por turno |
| nível / level | `LevelState` (estado) + `LevelDefinition` (dados, Sprint 2) | o corredor com unidades e a escada |
| turn | `TurnResolver.resolve()` | a resolução de um turno |
| stairs (escada) | posição da escada no `LevelState` | a saída / objetivo do nível |
| wall | `Space.is_wall()` | borda do nível |
| ace score | (Sprint 2) na pontuação | nota-alvo para uma execução "perfeita" |
| time bonus | (Sprint 2) na pontuação | bônus que cai a cada turno gasto |

## Sentidos (consultas — não gastam turno)

| Ruby Warrior | Neste projeto (`Senses`) |
|---|---|
| `warrior.feel(dir)` | `feel(direction)` |
| `warrior.look(dir)` | `look(direction)` |
| `warrior.listen` | `listen()` |
| `warrior.health` | `health()` |
| `warrior.direction_of_stairs` | `direction_of_stairs()` |
| `warrior.direction_of(space)` | `direction_of_position(pos)` |

## Ações (gastam o turno)

| Ruby Warrior | Neste projeto | Status |
|---|---|---|
| `warrior.walk!(dir)` | `WalkAction` | ✅ Sprint 1 |
| `warrior.attack!(dir)` | `AttackAction` | ✅ Sprint 1 |
| `warrior.rest!` | `RestAction` | ✅ Sprint 1 |
| `warrior.rescue!(dir)` | `RescueAction` | ⬜ Sprint 2 |
| `warrior.pivot!(dir)` | `PivotAction` | ⬜ Sprint 2 |
| `warrior.shoot!(dir)` | `ShootAction` | ⬜ Sprint 2 |

## Unidades

| Ruby Warrior | Neste projeto | HP |
|---|---|---:|
| warrior | `Warrior` | 20 |
| sludge | `Sludge` | 12 |
| thick sludge | `ThickSludge` | 24 |
| archer | `Archer` | 7 |
| wizard | `Wizard` | 3 |
| captive | `Captive` | 1 |

## Predicados de espaço

| Ruby Warrior | Neste projeto (`Space`) |
|---|---|
| `space.empty?` | `is_empty()` |
| `space.stairs?` | `is_stairs()` |
| `space.enemy?` | `is_enemy()` |
| `space.captive?` | `is_captive()` |
| `space.wall?` | `is_wall()` |

> Em GDScript não existe `?` no nome de método (como em Ruby), então usamos o prefixo
> `is_` (ex.: `is_empty()`), que também é a convenção em TypeScript.
