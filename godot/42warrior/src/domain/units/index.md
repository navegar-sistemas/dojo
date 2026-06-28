# `src/domain/units/` — Unidades

O warrior e as demais unidades do jogo. Cada tipo numa classe própria (responsabilidade
única), herdando a base `Unit`.

| Arquivo | Classe | HP | Ataque | Alcance | Papel |
|---|---|---:|---:|---:|---|
| `unit.gd` | `Unit` (base) | — | — | — | Saúde, atributos, imutabilidade do dano, `create_behavior()`. |
| `warrior.gd` | `Warrior` | 20 | 5 | 1 | O herói do jogador. |
| `sludge.gd` | `Sludge` | 12 | 3 | 1 | Inimigo corpo-a-corpo básico. |
| `thick_sludge.gd` | `ThickSludge` | 24 | 3 | 1 | Inimigo corpo-a-corpo resistente. |
| `archer.gd` | `Archer` | 7 | 3 | 3 | Inimigo à distância. |
| `wizard.gd` | `Wizard` | 3 | 11 | 3 | Frágil, mas letal — matar rápido. |
| `captive.gd` | `Captive` | 1 | 0 | 0 | Refém: resgatar, **nunca** atacar. |

## Notas

- **Imutabilidade**: `damaged_by(n)` devolve uma **nova** unidade do mesmo tipo com menos
  vida; a original não muda.
- **`create_behavior()`**: cada tipo declara sua IA (ver [`../combat/`](../combat/index.md)).
  A base devolve `InertBehavior`; inimigos sobrescrevem.
- Os números são **ajustáveis** (balanceamento) e ficam centralizados aqui.
