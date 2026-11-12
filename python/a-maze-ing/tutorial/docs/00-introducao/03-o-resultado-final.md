---
sidebar_position: 3
title: O resultado final
---

# O resultado final

## A sessão no terminal

Com o projeto pronto, `make run` desenha o labirinto com cores de fundo. Este é o labirinto do
`config.txt` padrão com `SEED=42`, com o "42" em cinza e o caminho mais curto à mostra:

![Labirinto 20 por 15 com o caminho mais curto](/img/problema/labirinto-20x15-caminho.svg)

Abaixo do desenho, o menu:

```text
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
Choice? (1-4):
```

| Tecla | Efeito |
|---|---|
| `1` | gera outro labirinto e regrava o arquivo de saída |
| `2` | mostra ou esconde o caminho mais curto, em ciano |
| `3` | troca a cor das paredes: branco, amarelo, verde, azul, e volta ao branco |
| `4` | sai |

## O arquivo de saída

Ao mesmo tempo, o programa grava `maze.txt`: uma linha de dígitos hexadecimais por linha do
labirinto, uma linha vazia, a entrada, a saída e o caminho mais curto. Com o `config.txt` padrão
e `SEED=42`:

```text
95395539555515513913
854693c69553c53c46aa
8153ac55695293a9556a
a852c3939696aac69552
ac3a92c045456a938556
c3aaaafa93fffaac4513
96aaaafc6857faa9396a
856c6afffafffac2aa92
81539053fafd5016a86a
ac3aaa92fafffaa9683a
a96aaaaa9695502c386a
c29046c069293c438692
9686953c52aaa93a83aa
83a943c13a86aaac6aaa
c4445456c44546c55446

0,0
19,14
SSEEESSSSSENNNESSSSEESSSSEESSEEEENNESSEEEEE
```

Os `f` no meio formam o "42": são as células com as quatro paredes fechadas.

## O pacote reutilizável

`make build` gera `mazegen-1.0.0-py3-none-any.whl`. Em outro projeto:

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42)
gen.generate()
print(gen.grid[0][0])   # paredes da célula (0, 0)
print(gen.solution)     # caminho mais curto, em letras N, E, S, W
```

## A árvore de arquivos

```text
a_maze_ing.py         o programa
config.txt            configuração padrão
Makefile              install, run, debug, clean, lint, lint-strict, build
pyproject.toml        metadados do pacote mazegen
mazegen/              o gerador (vai para o pacote)
amazeing/             a aplicação (fica fora do pacote)
README.md, LICENSE.md
mazegen-1.0.0-py3-none-any.whl, mazegen-1.0.0.tar.gz
```

A próxima parte explica cada regra do problema antes de qualquer código.
