# `src/domain/world/` — O tabuleiro

Representa o "mundo" do nível: por onde se anda, o que há em cada casa e o estado completo
do nível num dado instante.

| Arquivo | Classe | Responsabilidade |
|---|---|---|
| `direction.gd` | `Direction` | Direção **relativa** ao warrior (forward/backward): sinal relativo (+1/−1) e oposto (usado pelo pivot). |
| `space.gd` | `Space` | Visão **somente-leitura** de uma casa: `is_empty/is_stairs/is_enemy/is_captive/is_wall` e o tipo da unidade. |
| `level_state.gd` | `LevelState` | "Fotografia" **imutável** do nível (grade, warrior + facing, unidades por posição, turno). Consultas puras + construtores `with_*` que devolvem um novo estado. |

## Notas

- A grade é 1×N (um corredor). Posições fora de `[0, largura-1]` são **parede**.
- O `LevelState` é a fonte de verdade do estado; ninguém o muta — produz-se um novo.
- "Frente/trás" é relativo ao *facing* do warrior; o passo absoluto na grade
  (`facing × sinal`) é calculado pelo `LevelState`.
