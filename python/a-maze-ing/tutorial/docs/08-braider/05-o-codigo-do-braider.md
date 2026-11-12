---
sidebar_position: 5
title: O código do Braider
---

# O código do Braider

O `Braider` é um service sem estado, em `mazegen/services/braider.py`. Os métodos
`_remove_dead_ends`, `_add_loops` e `_open_without_3x3` foram construídos nas páginas
anteriores; falta o método público que os junta.

## `braid`

```python
    def braid(self, maze: Maze, rng: random.Random) -> None:
        """Remove the dead ends, then add loops up to MIN_LOOPS.

        Args:
            maze: Carved perfect maze, changed in place.
            rng: The single random source of the generator.
        """
        self._remove_dead_ends(maze, rng)
        self._add_loops(maze, rng)
```

- Recebe o labirinto **perfeito** que o `Carver` acabou de escavar e o altera no lugar.
- Recebe o **mesmo** `rng` que o `Carver` usou. Os sorteios do braiding continuam a sequência da
  escavação, e a seed fixa o tabuleiro inteiro.
- A ordem importa: o passo (a) primeiro, porque costuma criar ciclos de sobra; o passo (b) só
  completa o que faltar.

O sublinhado no início de `_remove_dead_ends`, `_add_loops` e `_open_without_3x3` marca esses
métodos como internos: de fora da classe, só `braid` deve ser chamado.

## O `Braider` não levanta exceção

Em casos raros o braiding não consegue cumprir as regras: um beco cujos lados todos completariam
um 3x3, ou uma grade fina em que as paredes candidatas a ciclo são todas recusadas. O `Braider`
não trata isso. Ele faz o melhor que pode e devolve.

Quem confere é o `MazeGenerator` (parte 9): depois de `braid`, ele testa
`len(maze.dead_ends()) <= MAX_DEAD_ENDS` e `maze.loop_count() >= MIN_LOOPS`. Se falhar, descarta
a grade e começa outra. Cada classe fica com uma responsabilidade: o `Braider` abre paredes, o
gerador decide se o resultado serve. A docstring da classe registra esse acordo.

## Experimente

Na raiz do projeto, com `.venv/bin/python`:

```python
import random

from mazegen.entities.maze import Maze
from mazegen.services.braider import Braider
from mazegen.services.carver import Carver
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(20, 15, Pattern42.for_size(20, 15))
rng = random.Random(42)
Carver().carve(maze, Cell(0, 0), rng)
print(len(maze.dead_ends()), maze.loop_count())
Braider().braid(maze, rng)
print(len(maze.dead_ends()), maze.loop_count(), maze.has_open_3x3())
```

```text
32 0
0 32 False
```

Antes: 32 becos reais e nenhum ciclo. Depois: nenhum beco real, 32 ciclos e nenhum 3x3 aberto.
É o tabuleiro sem becos que o subject premia como bônus.

## O arquivo completo

```python title="mazegen/services/braider.py"
"""Braiding that turns a perfect maze into a Pac-Man board."""

import random

from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction

MIN_LOOPS = 2
MAX_DEAD_ENDS = 2


class Braider:
    """Open walls of a perfect maze without ever opening a 3x3 area.

    The braider never raises: the MazeGenerator checks MIN_LOOPS and
    MAX_DEAD_ENDS on the result and rebuilds the grid when needed.
    """

    def braid(self, maze: Maze, rng: random.Random) -> None:
        """Remove the dead ends, then add loops up to MIN_LOOPS.

        Args:
            maze: Carved perfect maze, changed in place.
            rng: The single random source of the generator.
        """
        self._remove_dead_ends(maze, rng)
        self._add_loops(maze, rng)

    def _remove_dead_ends(self, maze: Maze, rng: random.Random) -> None:
        """Open one wall of every real dead end, in random order.

        Args:
            maze: Maze changed in place.
            rng: The single random source of the generator.
        """
        dead_ends = maze.dead_ends()
        rng.shuffle(dead_ends)
        for cell in dead_ends:
            if len(maze.passages(cell)) != 1:
                # An earlier opening already linked this cell.
                continue
            sides = maze.closed_sides(cell)
            rng.shuffle(sides)
            for side in sides:
                if self._open_without_3x3(maze, cell, side):
                    break

    def _add_loops(self, maze: Maze, rng: random.Random) -> None:
        """Open random inner walls until the maze has MIN_LOOPS cycles.

        Args:
            maze: Maze changed in place.
            rng: The single random source of the generator.
        """
        walls: list[tuple[Cell, Direction]] = [
            (cell, side)
            for cell in maze.cells()
            for side in maze.closed_sides(cell)
            # East and South list every inner wall exactly once.
            if side in (Direction.EAST, Direction.SOUTH)
        ]
        rng.shuffle(walls)
        for cell, side in walls:
            if maze.loop_count() >= MIN_LOOPS:
                return
            self._open_without_3x3(maze, cell, side)

    @staticmethod
    def _open_without_3x3(maze: Maze, cell: Cell, side: Direction) -> bool:
        """Open a wall and undo it when a 3x3 window becomes fully open.

        Args:
            maze: Maze changed in place.
            cell: Cell on one side of the wall.
            side: Side of the wall.

        Returns:
            True when the wall stayed open.
        """
        maze.open_wall(cell, side)
        if maze.has_open_3x3():
            maze.close_wall(cell, side)
            return False
        return True
```
