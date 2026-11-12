---
sidebar_position: 3
title: Conferir com o analisador
---

# Conferir com o analisador

O subject vem com um `maze_analyzer.py`, que lê um arquivo de saída e diz se ele é um labirinto
perfeito ou um tabuleiro de Pac-Man utilizável. Ele confirma o bônus com a opção
`--max-dead-ends 0`.

O analisador não faz parte da entrega: deixe-o fora do repositório, por exemplo na pasta acima
da raiz do projeto.

## As opções

```text
python3 maze_analyzer.py <output_file> [--min-loops N] [--max-dead-ends N]
```

- `--min-loops` (padrão `2`): quantos ciclos independentes o tabuleiro precisa ter.
- `--max-dead-ends` (padrão `2`): quantos becos **reais** são tolerados. Os becos cercados pelo
  "42" nunca contam.

Com o padrão, o analisador confere a regra obrigatória do modo Pac-Man. Com
`--max-dead-ends 0`, confere o bônus.

## Rodar

Gere um labirinto com o `config.txt` padrão (`PERFECT=False`) e passe o `maze.txt` ao
analisador:

```bash
printf '4\n' | make run > /dev/null
python3 ../maze_analyzer.py maze.txt --max-dead-ends 0
```

Com `SEED=42` descomentado no `config.txt`:

```text
Maze size        : 20 x 15 (300 cells)
Entry            : (0, 0)   Exit: (19, 14) (reachable)
Reachable region : 282 cells (0 corridor(s) unreachable)
Independent loops: 32 / 228 possible (path ratio 14%)
Dead-ends        : 0 real + 2 enclosed by the '42' (tolerated)
Corners + centre : all reachable
Wall coherence   : OK (all shared walls match)

Verdict: Pac-Man-USABLE: fully connected, corners and centre reachable, 32 independent routes; no real dead-end -> bonus-grade (perfectly braided).
```

## Ler o relatório

| Linha | O que confirma |
|---|---|
| `Reachable region` | 282 = 300 células menos as 18 do "42": toda célula livre é alcançável a partir da entrada |
| `Independent loops` | 32 ciclos, bem acima dos 2 exigidos |
| `Dead-ends` | **0 reais**; os 2 cercados pelo "42" são tolerados |
| `Corners + centre` | os quatro cantos e o centro são corredores alcançáveis |
| `Wall coherence` | toda parede compartilhada está igual nas duas células |
| `Verdict` | `Pac-Man-USABLE` e `no real dead-end -> bonus-grade (perfectly braided)` |

O veredito é o que conta: ele começa com `Pac-Man-USABLE` e termina com
`bonus-grade (perfectly braided)`. Se o labirinto tivesse um beco real, a última parte diria
`1 real dead-end(s) within tolerance (0 would be bonus-grade)` com as opções padrão, e com
`--max-dead-ends 0` o veredito seria `Not Pac-Man-ready`.

## Sem seed

Sem `SEED`, cada `make run` gera um labirinto diferente, e o número de ciclos muda (29, 30, 32
em execuções seguidas). O que se repete é a linha `0 real + 2 enclosed by the '42'` e o
veredito com `bonus-grade (perfectly braided)`.

## Na defesa

O avaliador pode pedir para ver o bônus funcionando. O caminho mais curto é o mesmo desta
página: `make run`, sair com `4`, rodar o analisador com `--max-dead-ends 0` e mostrar o
veredito. O README (parte 15) traz o mesmo comando na seção **Bonus**, e a página
[Por que não é garantido](./02-por-que-nao-e-garantido.md) responde a pergunta seguinte, se ela
vier: o código não promete zero, a regra do 3x3 tem prioridade, e o resultado medido é zero.
