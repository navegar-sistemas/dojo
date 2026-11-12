---
sidebar_position: 7
title: Um README inicial
---

# Um README inicial

## O build lê o README e a licença

O `pyproject.toml` da parte 3 aponta dois arquivos da raiz:

```toml
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
license-files = ["LICENSE.md"]
```

- `readme`: o texto do `README.md` vira a **descrição longa** do pacote, gravada nos metadados
  (`METADATA` no wheel, `PKG-INFO` no sdist). É o texto que um índice de pacotes mostra na
  página do projeto.
- `license-files`: o `LICENSE.md` é copiado para dentro do wheel.

Se um deles não existe, o build ainda termina, mas com avisos e um pacote incompleto:

| Arquivo ausente | O que o build imprime | O que falta no pacote |
|---|---|---|
| `README.md` | `WARNING File '.../README.md' cannot be found` | a descrição longa |
| `LICENSE.md` | `Pattern 'LICENSE.md' did not match any files.` | a licença |

O projeto exige um build sem nenhum aviso. Por isso os dois arquivos têm de existir **antes** do
primeiro `make build`, na próxima página.

## O que o README já precisa ter

O README completo, com todas as seções que o capítulo VII do subject pede, é escrito na parte 15,
quando o programa estiver pronto. Por enquanto bastam duas coisas:

1. a **primeira linha** exigida pelo subject, em itálico, com o seu login da intra 42;
2. a **documentação do módulo**, que o capítulo VI manda repetir no `README.md`. É o mesmo texto
   da docstring de `mazegen/__init__.py`, com o exemplo num bloco de código Python.

Um README inicial com só isso (troque `macoelho` pelo seu login):

````markdown
*This project has been created as part of the 42 curriculum by macoelho.*

# A-Maze-ing

## Reusable module

The reusable part of the project is the `mazegen` package; it is the only
code that goes into the wheel. Install it with
`pip install mazegen-1.0.0-py3-none-any.whl`.

Generate random mazes with a "42" drawn by fully closed cells.

The package exposes one class, MazeGenerator, and one exception,
MazeError. Install it with:

    pip install mazegen-1.0.0-py3-none-any.whl

MazeGenerator(width, height, entry=(0, 0), exit=None, perfect=False,
seed=None) takes:

    width (int, required): number of columns, 1 to 100, e.g. 20.
    height (int, required): number of rows, 1 to 100, e.g. 15.
    entry (tuple[int, int], default (0, 0)): entry cell as (x, y),
        where x is the column and y is the row, e.g. (0, 0).
    exit (tuple[int, int] | None, default None): exit cell as (x, y),
        e.g. (19, 14); None means the bottom-right cell.
    perfect (bool, default False): True builds a perfect maze, with
        exactly one path between any two cells; False builds a
        Pac-Man board, with loops and at most two dead ends; e.g. True.
    seed (int | None, default None): seed of the random source, e.g. 42;
        the same seed gives the same sequence of mazes; None gives a
        different one on every run.

The constructor raises MazeError when a parameter is impossible: width
or height outside 1..100, entry or exit outside the grid or on the
"42", entry equal to exit, or perfect=False with
(width - 1) * (height - 1) < 2. The message names the parameter.

Each call to generate() builds a new maze and fills:

    grid (list[list[int]]): height rows of width integers; grid[y][x]
        holds the closed walls of cell (x, y) as bits N=1, E=2, S=4,
        W=8, so 15 is a fully closed cell. The output file writes each
        value as one hexadecimal digit.
    solution (str): the shortest path from entry to exit, one letter
        N, E, S or W per step.

With perfect=False, generate() raises MazeError if 20 attempts in a
row fail to build a Pac-Man board.

pattern (set[tuple[int, int]]) holds the (x, y) cells of the "42" from
the constructor on. It is empty when the maze is smaller than 9x7 and
the "42" does not fit; the maze is generated without it.

Example:

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42)
gen.generate()
walls = gen.grid[0][0]
print("north wall of (0, 0) closed:", bool(walls & 1))
print(len(gen.pattern), "cells draw the 42")
print(gen.solution)
```
````

- O README é em inglês, como todo o resto do projeto entregue.
- No README, o exemplo sai da indentação e vai para um bloco de código marcado como `python`,
  que o GitHub colore. O texto em volta é o da docstring, sem mudança: quem lê um ou outro encontra a mesma
  documentação.
- Ao mudar a API do `MazeGenerator`, os dois lugares mudam juntos.
