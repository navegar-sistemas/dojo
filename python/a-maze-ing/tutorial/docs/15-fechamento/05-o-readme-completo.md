---
sidebar_position: 5
title: O README completo
---

# O README completo

As páginas anteriores explicaram o que o enunciado exige em cada seção do README. Esta mostra o
arquivo inteiro, pronto, para ficar na raiz do projeto com o nome `README.md`.

Parte dele descreve **você** e o seu trabalho, e não pode ser copiada como está. Algumas frases
também falam de coisas que quem seguiu o tutorial não tem: uma suíte de testes (um conjunto de
programas que testam o projeto), a biblioteca de testes `pytest-bdd`, uma especificação escrita
antes do código e uma lista de treze tarefas com "comandos de aceitação" (os comandos que
provavam cada tarefa pronta). Antes de usar, troque ou apague:

| Onde | O que trocar ou apagar |
|---|---|
| primeira linha | `macoelho` pelo seu login (ou logins, separados por vírgula) |
| `Algorithm`, os números medidos | os seus, se forem outros ([página 3](./03-algoritmo-e-modulo.md)) |
| `Algorithm`, a frase `The test suite checks 100 seeds and runs maze_analyzer.py on them.` | apague, ou diga como **você** conferiu a regra do 3x3 (por exemplo, rodando o `maze_analyzer.py` em vários arquivos de saída) |
| `Team`: `specification, implementation, tests and documentation` | o que você fez de fato |
| `Planning`: `thirteen ordered tasks` e `as the test suite grew` | o seu planejamento real; quem seguiu o tutorial pode descrever a ordem das partes ([página 4](./04-time-bonus-e-recursos.md)) |
| `What worked well`: `the acceptance commands written next to each task` | o que funcionou para você |
| `What could improve` | a sua melhoria |
| `Tools`: `pytest-bdd for the test suite` | apague, se você não a usou; liste as suas ferramentas |
| `Resources` | as referências que você leu |
| `AI usage`: as linhas que citam `the specification`, `the task list`, `the acceptance commands` e `the test suite` | as tarefas em que você usou IA e as partes afetadas |

O resto (formato do arquivo de configuração, menu, regras do `Makefile`, documentação do módulo)
descreve o programa e só muda se o seu programa for diferente.

Em Markdown, um bloco de código começa e termina com uma linha de três crases. Como o README tem
blocos assim por dentro, o bloco abaixo, que mostra o README inteiro, usa **quatro** crases nas
pontas; com três, ele terminaria no primeiro bloco interno.

````markdown title="README.md"
*This project has been created as part of the 42 curriculum by macoelho.*

# A-Maze-ing

## Description

A-Maze-ing generates a maze from a configuration file, writes it to an
output file in hexadecimal and shows it in the terminal.

- **Perfect mode** (`PERFECT=True`): exactly one path between any two
  cells, no loop.
- **Pac-Man mode** (`PERFECT=False`, the default): a fully connected board
  with loops, open corners and centre, at least two independent routes and
  at most two real dead ends (none in every maze measured).
- **The "42"**: 18 fully closed cells draw a "42" in the middle of every
  maze of at least 9x7 cells; smaller mazes are generated without it and
  the program prints `Error: maze too small for the "42" pattern`.
- **Output file**: one hexadecimal digit per cell, then the entry, the exit
  and the shortest path from entry to exit as `N`/`E`/`S`/`W` letters.
- **Display**: the maze is drawn with ANSI background colours, followed by
  a menu to regenerate it, show or hide the shortest path, rotate the wall
  colours and quit.
- **Reusable module**: the generator lives in the `mazegen` package,
  shipped as `mazegen-1.0.0-py3-none-any.whl` and `mazegen-1.0.0.tar.gz`.

## Instructions

Requirements: Python 3.10 or later and `make`.

```sh
make install          # creates .venv with flake8, mypy and build
make run              # runs python3 a_maze_ing.py config.txt with the .venv Python
```

`make run` is the same as `python3 a_maze_ing.py config.txt` with the
Python of `.venv`. To use another configuration file:

```sh
.venv/bin/python a_maze_ing.py my_config.txt
```

After each drawing the menu reads one choice:

| Choice | Effect |
|---|---|
| `1` | generate a new maze and write it to `OUTPUT_FILE` |
| `2` | show or hide the shortest path |
| `3` | rotate the wall colours (white, yellow, green, blue) |
| `4` | quit with exit code 0 |

Other rules of the `Makefile`:

| Rule | Effect |
|---|---|
| `make lint` | `flake8 .` and `mypy .` with the flags of the subject |
| `make lint-strict` | `flake8 .` and `mypy . --strict` |
| `make debug` | runs the program with `config.txt` inside `pdb` |
| `make clean` | removes `__pycache__`, `.mypy_cache`, `build`, `dist` and `*.egg-info` |
| `make build` | builds the wheel and the sdist and copies them to the root |

## Configuration file

One `KEY=VALUE` pair per line. Lines that start with `#` are comments and
blank lines are skipped. Coordinates are `x,y`, where `x` is the column and
`y` is the row, both from 0, with the origin at the top-left corner.

| Key | Mandatory | Value |
|---|---|---|
| `WIDTH` | yes | number of columns, 1 to 100 |
| `HEIGHT` | yes | number of rows, 1 to 100 |
| `ENTRY` | yes | entry cell `x,y`, inside the grid and outside the "42" |
| `EXIT` | yes | exit cell `x,y`, inside the grid, outside the "42" and different from `ENTRY` |
| `OUTPUT_FILE` | yes | path of the output file, not empty |
| `PERFECT` | yes | `True` or `False` |
| `SEED` | no | integer; the same seed gives the same sequence of mazes |

Reading rules:

- keys and booleans are accepted in any case (`width=20`, `perfect=true`);
- spaces around the key and the value are ignored; the line is split at
  the first `=`;
- an unknown key is ignored; a repeated key keeps its last value;
- a `#` after a value is part of the value, which then is invalid;
- every missing mandatory key is listed in one error;
- `SEED` is optional: without it every run draws a different maze;
- `WIDTH` and `HEIGHT` go from 1 to 100; `ENTRY` and `EXIT` must differ and
  stay off the "42"; `PERFECT=False` needs
  `(WIDTH - 1) x (HEIGHT - 1) >= 2`.

Every configuration or runtime error prints one line `Error: <cause>`
on stderr and exits with code 1. A wrong number of arguments prints the
usage line `Usage: python3 a_maze_ing.py <config_file>` instead, also
with code 1.

The `config.txt` of the repository:

```text
# Width of the maze, in cells (1 to 100)
WIDTH=20
# Height of the maze, in cells (1 to 100)
HEIGHT=15
# Entry cell as x,y (x = column, y = row, both from 0)
ENTRY=0,0
# Exit cell as x,y
EXIT=19,14
# File that receives the maze in hexadecimal
OUTPUT_FILE=maze.txt
# True: perfect maze (single path); False: Pac-Man board (default)
PERFECT=False
# Uncomment to get the same maze on every run
# SEED=42
```

## Algorithm

- **Perfect maze: iterative recursive backtracker.** A randomised
  depth-first search with an explicit stack starts at the entry and never
  enters the "42". A stack and a list of neighbours are the whole
  structure, every cell enters and leaves the stack once, and the
  corridors come out long with few dead ends: on 20x15, seeds 1 to 100,
  24 to 37 real dead ends, against 74 to 95 for Kruskal and 77 to 97 for
  Prim. Fewer dead ends mean fewer walls to open in Pac-Man mode.
- **Pac-Man board: braiding.** The same perfect maze, then one wall opened
  in every dead end, in random order, and, when still needed, random extra
  walls until there are 2 loops. With more than 2 real dead ends or fewer
  than 2 loops the generator rebuilds the grid, up to 20 attempts.
- **No open 3x3 area.** A perfect maze is a tree and cannot hold an open
  3x3 block, which would contain cycles. In Pac-Man mode, after each wall
  is opened, `Maze.has_open_3x3` scans every 3x3 window of the grid; when
  one has its 12 inner walls open, `close_wall` undoes the opening.
  The test suite checks 100 seeds and runs `maze_analyzer.py` on them.
- **Shortest path**: breadth-first search from the entry, neighbours in
  the order N, E, S, W.
- **The "42"**: two 3x5 glyphs with a free column between them, 7x5 in
  total, with the top-left corner at `x = (WIDTH - 7) // 2` and
  `y = (HEIGHT - 5) // 2`. It exists only with `WIDTH >= 9` and
  `HEIGHT >= 7`, which keeps a corridor all around it.

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

## Team and project management

- **Team**: macoelho, alone: specification, implementation, tests and
  documentation.
- **Planning**: the work followed thirteen ordered tasks, from the
  toolchain to the final package: value objects, the `Maze` entity, the
  carver, the solver, the braider, the public generator, the application
  utilities, the configuration, the output file, the drawing, the menu and
  the closing checks. The plan kept its order; the checks of each task
  were tightened as the test suite grew.
- **What worked well**: one convention for coordinates (`x,y` everywhere),
  the layers that keep files and terminal I/O at the edges, and the
  acceptance commands written next to each task.
- **What could improve**: the 3x3 check scans the whole grid after every
  opening; checking only the windows around the opened wall would be
  faster.
- **Tools**: Python 3, `venv`, `flake8`, `mypy`, `build`, `make`, `git`,
  pytest-bdd for the test suite and the `maze_analyzer.py` given with the
  subject.

## Bonus

The Pac-Man board (`PERFECT=False`, the default) came out with no real
dead end in every maze measured (seeds 1 to 100 in 9x7, 20x15 and 40x30):
the braiding opens one wall in every dead end. The code only guarantees
at most two, because a wall that would open a 3x3 area is never opened.
Only the 2 dead ends walled in by the "42" remain, and the analyzer does
not count them. Check it with:

```sh
python3 maze_analyzer.py maze.txt --max-dead-ends 0
```

The verdict starts with `Pac-Man-USABLE` and ends with
`no real dead-end -> bonus-grade (perfectly braided).`

## Resources

- Jamis Buck, *Mazes for Programmers* (Pragmatic Bookshelf, 2015).
- Jamis Buck, "Maze Generation: Recursive Backtracking",
  <http://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracking>.
- Wikipedia, "Maze generation algorithm",
  <https://en.wikipedia.org/wiki/Maze_generation_algorithm>.
- Wikipedia, "Breadth-first search",
  <https://en.wikipedia.org/wiki/Breadth-first_search>.
- Python, `random`, <https://docs.python.org/3/library/random.html>.
- Wikipedia, "ANSI escape code",
  <https://en.wikipedia.org/wiki/ANSI_escape_code>.
- PEP 257, <https://peps.python.org/pep-0257/>, and the Google Python
  Style Guide,
  <https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings>.
- Python Packaging User Guide, <https://packaging.python.org/>, and
  PEP 639, <https://peps.python.org/pep-0639/>.
- MIT License, <https://opensource.org/license/mit>.

### AI usage

| Task | Files or parts affected |
|---|---|
| reviewing the specification for gaps and contradictions | the task list and the acceptance commands |
| suggesting test cases for the configuration errors | the configuration scenarios of the test suite |
| explaining `mypy --strict` messages | `mazegen/` and `amazeing/` type hints |

Every line of the project was reviewed and can be explained by its author.
````

## Conferir antes de entregar

Três pontos que o avaliador procura e que um erro de digitação estraga podem ser conferidos no
terminal, na raiz do projeto:

- `head -n 1 README.md` mostra a primeira linha do arquivo;
- `grep -c 'python3 a_maze_ing.py config.txt' README.md` conta quantas linhas contêm o comando
  do enunciado;
- `grep -E '^## ' README.md` mostra só as linhas que começam com `## `, os títulos das seções.
  O texto entre aspas é um padrão de busca (uma *expressão regular*), em que alguns símbolos
  têm sentido especial: o `^` quer dizer "começo da linha", então `^## ` só aceita linhas que
  começam com `## `, e não as que têm `## ` no meio. O `-E` liga a forma mais completa desses
  padrões; para este, o resultado seria o mesmo sem ele.

```bash
head -n 1 README.md
grep -c 'python3 a_maze_ing.py config.txt' README.md
grep -E '^## ' README.md
```

```text
*This project has been created as part of the 42 curriculum by macoelho.*
2
## Description
## Instructions
## Configuration file
## Algorithm
## Reusable module
## Team and project management
## Bonus
## Resources
```

A saída certa: a primeira linha em itálico com o seu login; o comando do enunciado escrito por
extenso (ele aparece em duas linhas da seção `Instructions`); e as oito seções, na ordem.
`Description`, `Instructions` e `Resources` são os nomes que o enunciado fixa e precisam estar
escritos exatamente assim.
