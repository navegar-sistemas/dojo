---
sidebar_position: 4
title: O arquivo do gerador
---

# O arquivo do gerador

## Resolver e publicar

Depois do laço de tentativas, `generate()` termina com duas linhas:

```python
        self.solution = Solver().shortest_path(maze, self._entry, self._exit)
        self.grid = maze.rows()
```

Depois do laço, `maze` é a grade aceita. O caminho é calculado uma vez, aqui, e
`maze.rows()` devolve uma cópia das linhas em listas de inteiros. O `Maze` termina junto com o
método: só os tipos simples saem do pacote.

## Experimente

```python
from mazegen import MazeGenerator

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
```

```text
[] '' 18
15 20 SSEEESSSSSENNNESSSSEESSSSEESSEEEENNESSEEEEE
False
True
```

Antes de `generate()`, só `pattern` está preenchido. A segunda chamada dá outro labirinto, e um
gerador novo com a mesma seed repete o primeiro.

## O arquivo completo

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
