# `src/domain/senses/` — Sentidos

O que o jogador pode **perceber** sobre o nível para decidir sua ação. São consultas puras:
**não mudam nada** e **não gastam o turno** (princípio CQS).

| Arquivo | Classe | Responsabilidade |
|---|---|---|
| `senses.gd` | `Senses` | Consultas sobre um snapshot do `LevelState`. |

## API de percepção

| Método | Retorna | O que diz |
|---|---|---|
| `feel(direction)` | `Space` | O que há na casa adjacente naquela direção. |
| `look(direction)` | `Array[Space]` | As 3 casas à frente (mais perto → mais longe). |
| `listen()` | `Array[Space]` | Todas as casas que contêm unidades. |
| `health()` | `int` | A vida atual do warrior. |
| `direction_of_stairs()` | `Direction` | Para onde fica a escada. |
| `direction_of_position(pos)` | `Direction` | Para onde fica uma posição (ex.: unidade ouvida). |

## Notas

- O fluxo é **sentir → decidir → agir**: o jogador usa os sentidos para escolher **uma**
  ação, que então é resolvida pelo [`../turn/`](../turn/index.md).
- No Sprint 2, esses sentidos serão expostos ao código do jogador pela `WarriorFacade`,
  sem dar acesso ao estado interno.
