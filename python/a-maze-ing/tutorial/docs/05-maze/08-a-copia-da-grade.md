---
sidebar_position: 8
title: A cópia da grade
---

# A cópia da grade

## `rows`

```python
    def rows(self) -> list[list[int]]:
        return [row[:] for row in self._walls]
```

A grade pronta, uma lista por linha, no formato da API pública: `rows()[y][x]` são as paredes da
célula `(x, y)`. O `MazeGenerator` (parte 9) a guarda no atributo `grid` no fim de `generate()`,
e dali ela vai para o arquivo de saída e para o desenho.

## Por que uma cópia

Devolver `self._walls` direto entregaria a lista **interna**. Quem a recebesse poderia escrever
`grid[0][0] = 0` e abrir as quatro paredes de uma célula sem passar por `open_wall`: a coerência,
a borda e o "42" deixariam de estar garantidos, e o `Maze` nem saberia.

`row[:]` copia cada linha. A cópia de cada linha basta, sem copiar os números: um `int` não
muda, então compartilhar os mesmos inteiros entre as duas grades não oferece risco. O que
precisa ser novo são as **listas**, que são mutáveis.

```python
from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(3, 2, Pattern42.for_size(3, 2))
copy = maze.rows()
copy[0][0] = 0
print(copy[0][0], maze.walls(Cell(0, 0)))
```

```text
0 15
```

A cópia mudou; o `Maze`, não.

## A classe inteira

| Método | Papel |
|---|---|
| `__init__` | cria a grade com tudo fechado |
| `__contains__` | a posição está dentro da grade? |
| `cells` | as células fora do "42", linha por linha |
| `walls` | a máscara de paredes de uma célula |
| `neighbour` | a vizinha de um lado, ou `None` na borda e no "42" |
| `is_open` | um lado é passagem? |
| `open_wall`, `close_wall` | as únicas mudanças, sempre nas duas células |
| `_other_side` | a guarda das duas mudanças |
| `passages` | os lados abertos |
| `closed_sides` | os lados fechados que poderiam abrir |
| `dead_ends` | os becos reais |
| `loop_count` | os ciclos independentes |
| `has_open_3x3`, `_window_open` | há área aberta 3x3? |
| `rows` | a cópia da grade |

Cada método tem uma docstring no estilo Google: um resumo, os parâmetros (`Args:`), o que
devolve (`Returns:` ou `Yields:`) e o que levanta (`Raises:`). A docstring da classe registra as
regras que ela protege.

## O arquivo completo

```python title="mazegen/entities/maze.py"
"""Mutable grid of wall masks, the state the generator carves."""

from collections.abc import Iterator

from mazegen.errors import MazeError
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
from mazegen.value_objects.pattern42 import Pattern42

ALL_WALLS = 15


class Maze:
    """Grid of cells whose set bits are closed walls.

    Every cell starts with ALL_WALLS. Only open_wall and close_wall change
    the grid, always on both cells of the wall, so neighbours stay
    coherent, the border stays closed and the "42" cells keep their four
    walls.

    Attributes:
        width: Number of columns.
        height: Number of rows.
        pattern: Cells of the "42", outside the maze graph.
    """

    def __init__(self, width: int, height: int, pattern: Pattern42) -> None:
        """Create a grid with every wall closed.

        Args:
            width: Number of columns.
            height: Number of rows.
            pattern: Cells of the "42" for this size.
        """
        self.width = width
        self.height = height
        self.pattern = pattern
        self._walls: list[list[int]] = [
            [ALL_WALLS] * width for _ in range(height)
        ]

    def __contains__(self, cell: object) -> bool:
        """Tell whether a cell lies inside the grid.

        Args:
            cell: Object to look up; only a Cell can be inside.

        Returns:
            True for a Cell with 0 <= x < width and 0 <= y < height.
        """
        return (isinstance(cell, Cell) and 0 <= cell.x < self.width
                and 0 <= cell.y < self.height)

    def cells(self) -> Iterator[Cell]:
        """Walk the grid row by row, skipping the "42".

        Yields:
            Every cell outside the "42", y outer and x inner.
        """
        for y in range(self.height):
            for x in range(self.width):
                cell = Cell(x, y)
                if cell not in self.pattern:
                    yield cell

    def walls(self, cell: Cell) -> int:
        """Closed walls of a cell.

        Args:
            cell: Cell inside the grid.

        Returns:
            The wall mask, 0 to 15.
        """
        return self._walls[cell.y][cell.x]

    def neighbour(self, cell: Cell, side: Direction) -> Cell | None:
        """Cell across one side, when it belongs to the maze graph.

        Args:
            cell: Starting cell.
            side: Side to look across.

        Returns:
            The neighbour, or None outside the grid and on the "42".
        """
        other = cell.step(side)
        if other not in self or other in self.pattern:
            return None
        return other

    def is_open(self, cell: Cell, side: Direction) -> bool:
        """Tell whether a side of a cell is a passage.

        Args:
            cell: Cell inside the grid.
            side: Side to check.

        Returns:
            True when the neighbour exists and the wall bit is clear.
        """
        return (self.neighbour(cell, side) is not None
                and not self.walls(cell) & side)

    def open_wall(self, cell: Cell, side: Direction) -> None:
        """Open the wall between a cell and its neighbour.

        Args:
            cell: Cell outside the "42".
            side: Side of the wall.

        Raises:
            MazeError: The wall is on the border or touches the "42".
        """
        other = self._other_side(cell, side)
        self._walls[cell.y][cell.x] &= ~side
        self._walls[other.y][other.x] &= ~side.opposite

    def close_wall(self, cell: Cell, side: Direction) -> None:
        """Close the wall between a cell and its neighbour.

        Args:
            cell: Cell outside the "42".
            side: Side of the wall.

        Raises:
            MazeError: The wall is on the border or touches the "42".
        """
        other = self._other_side(cell, side)
        self._walls[cell.y][cell.x] |= side
        self._walls[other.y][other.x] |= side.opposite

    def _other_side(self, cell: Cell, side: Direction) -> Cell:
        """Neighbour that shares a wall that may change.

        Args:
            cell: Cell on one side of the wall.
            side: Side of the wall.

        Returns:
            The cell on the other side of the wall.

        Raises:
            MazeError: The wall is on the border or touches the "42".
        """
        other = self.neighbour(cell, side)
        if other is None or cell in self.pattern:
            raise MazeError('internal: cannot change a border or "42" wall')
        return other

    def passages(self, cell: Cell) -> list[Direction]:
        """Open sides of a cell.

        Args:
            cell: Cell inside the grid.

        Returns:
            The open sides, in the order N, E, S, W.
        """
        return [side for side in Direction if self.is_open(cell, side)]

    def closed_sides(self, cell: Cell) -> list[Direction]:
        """Closed sides that face a cell of the maze graph.

        Args:
            cell: Cell inside the grid.

        Returns:
            The closed sides whose neighbour is inside the grid and outside
            the "42", in the order N, E, S, W.
        """
        return [
            side for side in Direction
            if self.neighbour(cell, side) is not None
            and self.walls(cell) & side
        ]

    def dead_ends(self) -> list[Cell]:
        """Real dead ends: one passage and a closed side to a free cell.

        A cell with one passage walled in only by the border and the "42"
        is not a real dead end.

        Returns:
            The real dead ends, in the order of cells().
        """
        return [
            cell for cell in self.cells()
            if len(self.passages(cell)) == 1 and self.closed_sides(cell)
        ]

    def loop_count(self) -> int:
        """Independent cycles of the connected maze.

        Returns:
            Passages minus cells outside the "42" plus one.
        """
        ends = 0
        count = 0
        for cell in self.cells():
            ends += len(self.passages(cell))
            count += 1
        return ends // 2 - count + 1

    def has_open_3x3(self) -> bool:
        """Tell whether some 3x3 window has its 12 inner walls open.

        Returns:
            True when at least one window of the grid is fully open.
        """
        for y0 in range(self.height - 2):
            for x0 in range(self.width - 2):
                if self._window_open(x0, y0):
                    return True
        return False

    def _window_open(self, x0: int, y0: int) -> bool:
        """Tell whether the 3x3 window at a corner is fully open.

        Stopping at the first closed wall keeps 100x100 Pac-Man boards
        well under the 30 s limit of the test suite.

        Args:
            x0: Column of the top-left cell of the window.
            y0: Row of the top-left cell of the window.

        Returns:
            True when the 6 East and the 6 South inner walls are open.
        """
        for y in range(y0, y0 + 3):
            for x in range(x0, x0 + 3):
                walls = self.walls(Cell(x, y))
                if x < x0 + 2 and walls & Direction.EAST:
                    return False
                if y < y0 + 2 and walls & Direction.SOUTH:
                    return False
        return True

    def rows(self) -> list[list[int]]:
        """Copy of the grid, one list per row.

        Returns:
            height lists of width wall masks.
        """
        return [row[:] for row in self._walls]
```
