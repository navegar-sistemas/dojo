---
sidebar_position: 8
title: Um README inicial
---

# Um README inicial

O próximo passo é empacotar o `mazegen` ([página 9](./08-o-pacote.md)), e o empacotamento lê dois
arquivos da raiz do repositório: o `README.md` e o `LICENSE.md`. Se um deles faltar, o pacote sai
incompleto. A licença foi escrita na [página 7](./06-a-licenca.md); esta página escreve um
`README.md` inicial, só com o que o pacote e a documentação do módulo já precisam. O README
completo vem na [parte 15](../15-fechamento/01-o-que-o-readme-precisa-ter.md), com o programa
pronto.

## O empacotamento lê o README e a licença

O `README.md` ("leia-me") é o texto de apresentação de um repositório, escrito em **Markdown**
(texto comum com marcações simples, como `#` para título e `*texto*` para itálico). O
`pyproject.toml`, o arquivo que descreve o pacote ([parte 3](../03-ambiente/04-pyproject.md)),
aponta os dois arquivos:

```toml
readme = "README.md"
requires-python = ">=3.10"
license = "MIT"
license-files = ["LICENSE.md"]
```

- `readme`: o texto do `README.md` vira a **descrição longa** do pacote. O empacotamento gera dois
  arquivos instaláveis com `pip`: o **wheel** (`.whl`), pronto para instalar, e o **sdist**
  (`.tar.gz`), com os fontes ([página 9](./08-o-pacote.md)). Cada um leva dentro um arquivo de
  texto com os dados do pacote (nome, versão, licença, descrição): o `METADATA`, no wheel, e o
  `PKG-INFO`, no sdist. A descrição longa vai nesses arquivos. É o texto que um índice de
  pacotes, como o site PyPI, de onde o `pip` baixa pacotes, mostra na página do projeto.
- `license-files`: o `LICENSE.md` é copiado para dentro do pacote.

Se um deles não existe, o empacotamento ainda termina, mas imprime avisos e gera um pacote
incompleto:

| Arquivo ausente | O que o empacotamento imprime | O que falta no pacote |
|---|---|---|
| `README.md` | `WARNING File '.../README.md' cannot be found` | a descrição longa |
| `LICENSE.md` | `Pattern 'LICENSE.md' did not match any files.` | a licença |

Este projeto trata aviso como erro: o empacotamento tem de terminar sem nenhum. Por isso os dois
arquivos precisam existir **antes** do primeiro `make build`.

## O que o README já precisa ter

Por enquanto, duas coisas:

1. a **primeira linha** que o enunciado exige, em itálico (entre `*`), com a frase fixa que ele dá e,
   no fim, quem fez o projeto: o seu login (o seu nome de usuário);
2. a **documentação do módulo**, que o enunciado manda pôr também no `README.md`. É o mesmo texto
   da docstring de `mazegen/__init__.py` ([página 6](./05-documentacao-do-modulo.md)), com o
   exemplo num bloco de código Python.

Um README inicial com só isso (troque `macoelho` pelo seu login):

````markdown
*This project has been created as part of the 42 curriculum by macoelho.*

# A-Maze-ing

## Reusable module

The reusable part of the project is the `mazegen` package; it is the only
code that goes into the wheel.

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

The constructor raises MazeError when a parameter has the wrong type
(width, height or seed not an int, entry or exit not a tuple of two
ints, perfect not a bool) or an impossible value: width or height
outside 1..100, entry or exit outside the grid or on the "42", entry
equal to exit, or perfect=False with (width - 1) * (height - 1) < 2.
The message names the parameter.

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

- O README é em inglês, como todo o resto do projeto entregue (escolha do projeto).
- A seção `## Reusable module` ("módulo reutilizável") tem duas partes. O primeiro parágrafo é do
  README: diz, a quem chega pelo repositório, que o pacote `mazegen` é a parte reutilizável.
  Daí em diante, o texto é o da docstring, sem mudança, a partir de "Generate random mazes...",
  inclusive o comando `pip install`: quem lê um ou outro encontra a mesma documentação.
- A única diferença entre a docstring e o README é o exemplo: na docstring ele é texto recuado
  com 4 espaços; no README ele vai para um bloco de código marcado como `python`, que o GitHub
  mostra colorido.
- Ao mudar os parâmetros ou os atributos do `MazeGenerator`, os dois lugares mudam juntos.
