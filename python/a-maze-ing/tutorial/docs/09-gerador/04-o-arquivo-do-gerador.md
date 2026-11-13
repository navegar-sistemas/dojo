---
sidebar_position: 5
title: O arquivo do gerador
---

# O arquivo do gerador

Depois do laço de tentativas da [página anterior](./03-generate.md), a variável `maze` guarda um
labirinto aceito, mas ele ainda está nos tipos internos do pacote (`Maze`, `Cell`). Falta calcular
o caminho mais curto e entregar o resultado em tipos simples, que é o que a fachada promete. Esta
página fecha o método `generate()` e mostra o arquivo `mazegen/generator.py` inteiro.

## Resolver e publicar

`generate()` termina com duas linhas:

```python
        self.solution = Solver().shortest_path(maze, self._entry, self._exit)
        self.grid = maze.rows()
```

- `Solver().shortest_path(...)` devolve o caminho mais curto da entrada até a saída, em letras
  `N`, `E`, `S` e `W` ([parte 7](../07-solver/03-o-codigo-do-solver.md)). Ele é calculado uma vez
  por labirinto, aqui; o arquivo de saída e a tela usam o mesmo texto.
- `maze.rows()` devolve uma **cópia** da grade de paredes: uma lista por linha, com o número das
  paredes de cada célula ([parte 5](../05-maze/08-a-copia-da-grade.md)). Sendo cópia, quem mexer
  em `gen.grid` não estraga nada dentro do pacote.

O `Maze` deixa de existir quando o método termina: só os tipos simples (`str` e listas de `int`)
saem do pacote.

## O arquivo completo

Juntando as constantes e a assinatura ([página 2](./10-construtor-e-atributos.md)), as
conferências do construtor ([página 3](./02-validar-os-parametros.md)) e o laço de tentativas
([página 4](./03-generate.md)). Os imports trazem cada peça das partes 4 a 8; do módulo do
`Braider` vêm também as constantes `MAX_DEAD_ENDS` e `MIN_LOOPS`. A docstring da classe (o texto
entre `"""` abaixo de `class MazeGenerator:`) descreve os três atributos públicos.

```python title="mazegen/generator.py"
"""Public facade of the package: MazeGenerator."""

import random

from mazegen.entities.maze import Maze
from mazegen.errors import MazeError
from mazegen.services.braider import MAX_DEAD_ENDS, MIN_LOOPS, Braider
from mazegen.services.carver import Carver
from mazegen.services.solver import Solver
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

MIN_SIZE = 1
MAX_SIZE = 100
MAX_ATTEMPTS = 20


class MazeGenerator:
    """Generate perfect mazes or Pac-Man boards with a "42" in the middle.

    Attributes:
        grid: height rows of width wall masks after generate(); empty
            before it.
        solution: Shortest path from entry to exit after generate(), one
            letter N, E, S or W per step; empty before it.
        pattern: (x, y) cells of the "42"; empty when it does not fit.
    """

    def __init__(self, width: int, height: int,
                 entry: tuple[int, int] = (0, 0),
                 exit: tuple[int, int] | None = None, perfect: bool = False,
                 seed: int | None = None) -> None:
        """Validate the parameters and prepare the single random source.

        Args:
            width: Number of columns, MIN_SIZE to MAX_SIZE.
            height: Number of rows, MIN_SIZE to MAX_SIZE.
            entry: Entry cell as (x, y).
            exit: Exit cell as (x, y); None means the bottom-right cell.
            perfect: True for a perfect maze, False for a Pac-Man board.
            seed: Seed of the random source; None for a fresh one.

        Raises:
            MazeError: A parameter is impossible; the message names it.
        """
        for name, value in (("width", width), ("height", height)):
            if not MIN_SIZE <= value <= MAX_SIZE:
                raise MazeError(f"{name} must be between {MIN_SIZE} and "
                                f"{MAX_SIZE}, got {value}")
        if exit is None:
            exit = (width - 1, height - 1)
        for name, (x, y) in (("entry", entry), ("exit", exit)):
            if not (0 <= x < width and 0 <= y < height):
                raise MazeError(f"{name} ({x}, {y}) is outside the maze")
        if entry == exit:
            raise MazeError("entry and exit must differ")
        if not perfect and (width - 1) * (height - 1) < 2:
            raise MazeError(
                "perfect=False needs (width - 1) x (height - 1) >= 2 for a "
                f"Pac-Man board, got {width}x{height}")
        pattern42 = Pattern42.for_size(width, height)
        for name, (x, y) in (("entry", entry), ("exit", exit)):
            if Cell(x, y) in pattern42:
                raise MazeError(f'{name} ({x}, {y}) lies on the "42" pattern')
        self._width = width
        self._height = height
        self._entry = Cell(*entry)
        self._exit = Cell(*exit)
        self._perfect = perfect
        self._pattern42 = pattern42
        self._rng = random.Random(seed)
        self.grid: list[list[int]] = []
        self.solution = ""
        self.pattern: set[tuple[int, int]] = {
            cell.as_tuple() for cell in pattern42.cells
        }

    def generate(self) -> None:
        """Build a new maze and fill grid and solution.

        Every attempt and every call draws from the same random source, so
        a seed repeats the whole sequence of mazes.

        Raises:
            MazeError: MAX_ATTEMPTS attempts in a row failed to build a
                Pac-Man board.
        """
        for _ in range(MAX_ATTEMPTS):
            maze = Maze(self._width, self._height, self._pattern42)
            Carver().carve(maze, self._entry, self._rng)
            if self._perfect:
                break
            Braider().braid(maze, self._rng)
            if (len(maze.dead_ends()) <= MAX_DEAD_ENDS
                    and maze.loop_count() >= MIN_LOOPS):
                break
        else:
            raise MazeError("could not build a Pac-Man board after "
                            f"{MAX_ATTEMPTS} attempts")
        self.solution = Solver().shortest_path(maze, self._entry, self._exit)
        self.grid = maze.rows()
```

## Experimente

O `mazegen/__init__.py` ainda tem só a docstring de uma linha da
[parte 3](../03-ambiente/07-pacotes-do-mazegen.md), então os exemplos importam pelo caminho
completo, `from mazegen.generator import MazeGenerator`. A forma curta,
`from mazegen import MazeGenerator`, passa a funcionar na [página 6](./05-documentacao-do-modulo.md).

### Os atributos antes e depois de `generate()`

O código cria um gerador, olha os atributos antes e depois de `generate()`, gera um segundo
labirinto e compara com um gerador novo de mesma semente. Na raiz do projeto:

```bash
.venv/bin/python - <<'EOF'
from mazegen.generator import MazeGenerator

gen = MazeGenerator(width=20, height=15, seed=42)
print(gen.grid, repr(gen.solution), len(gen.pattern))
gen.generate()
print(len(gen.grid), len(gen.grid[0]), gen.solution)
first = gen.grid
gen.generate()
print(gen.grid == first)
again = MazeGenerator(width=20, height=15, seed=42)
again.generate()
print(again.grid == first)
EOF
```

```text
[] '' 18
15 20 SSEEESSSSSENNNESSSSEESSSSEESSEEEENNESSEEEEE
False
True
```

- Antes de `generate()`, só `pattern` está preenchido: 18 células do "42". (`repr` mostra o texto
  vazio como `''`, para ele aparecer na saída.)
- Depois, `grid` tem 15 linhas de 20 números, e `solution` tem o caminho.
- `first = gen.grid` não copia a grade: `first` passa a ser outro nome para a **mesma** lista.
  A segunda chamada a `generate()` não mexe nessa lista; ela guarda em `gen.grid` uma lista
  **nova**, a que `maze.rows()` devolve. Então `first` continua com o primeiro labirinto, e
  `gen.grid` passa a ter o segundo.
- A segunda chamada dá outro labirinto (`False`): o sorteador continuou de onde parou.
- Um gerador novo com a mesma semente repete o primeiro labirinto (`True`).

### Os parâmetros recusados

Cada recusa do construtor ([página 3](./02-validar-os-parametros.md)), uma por vez:

```bash
.venv/bin/python - <<'EOF'
from mazegen.errors import MazeError
from mazegen.generator import MazeGenerator

for kwargs in [
    {"width": 0, "height": 15},
    {"width": 20, "height": 101},
    {"width": 20, "height": 15, "entry": (20, 0)},
    {"width": 20, "height": 15, "exit": (0, 0)},
    {"width": 2, "height": 2},
    {"width": 20, "height": 15, "entry": (6, 5)},
]:
    try:
        MazeGenerator(**kwargs)
    except MazeError as error:
        print(error)
EOF
```

```text
width must be between 1 and 100, got 0
height must be between 1 and 100, got 101
entry (20, 0) is outside the maze
entry and exit must differ
perfect=False needs (width - 1) x (height - 1) >= 2 for a Pac-Man board, got 2x2
entry (6, 5) lies on the "42" pattern
```

- A lista tem seis dicionários, um por tentativa. `kwargs` é só o nome da variável, comum em
  Python para isto: vem de *keyword arguments*, "argumentos com nome".
- `MazeGenerator(**kwargs)`: os dois asteriscos desmontam o dicionário e passam cada chave como um
  parâmetro com nome. `{"width": 0, "height": 15}` vira `MazeGenerator(width=0, height=15)`.
- Cada tentativa levanta um `MazeError`, e o `except` imprime só a mensagem.
- Em 20x15, o canto de cima à esquerda do "42" fica na célula `6,5`: por isso a última entrada é
  recusada.
