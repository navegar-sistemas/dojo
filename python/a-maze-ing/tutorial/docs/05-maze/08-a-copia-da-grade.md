---
sidebar_position: 9
title: A cópia da grade
---

# A cópia da grade

Quando os algoritmos terminam, a grade pronta precisa sair do `Maze` para ser gravada no arquivo
de saída e desenhada na tela. Mas, se o `Maze` entregar a sua própria lista de paredes, quem a
receber pode mudá-la sem passar pelas regras. Esta página escreve o método que entrega a grade
com segurança, `rows`, o último método da classe, e mostra o arquivo completo do `Maze`.

## `rows`

```python
    def rows(self) -> list[list[int]]:
        return [row[:] for row in self._walls]
```

Devolve a grade pronta, uma lista por linha, cada linha com o número de paredes (0 a 15) de cada
célula: `rows()[y][x]` são as paredes da célula `x,y`. É o formato que o `mazegen` mostra para
fora: o `MazeGenerator` ([parte 9](../09-gerador/03-generate.md)) guarda essa grade no atributo
`grid` no fim da geração, e dali ela vai para o arquivo de saída e para o desenho.

## Por que uma cópia

Devolver `self._walls` direto entregaria a lista **interna**, a mesma que o `Maze` usa. Quem a
recebesse poderia escrever `grid[0][0] = 0` e abrir as quatro paredes de uma célula sem passar
por `open_wall`. A coerência (vizinhas concordando sobre a parede do meio), a borda fechada e o
"42" fechado deixariam de estar garantidos, e o `Maze` nem ficaria sabendo.

`row[:]` é uma **fatia** (*slice*) da linha do começo ao fim: uma lista nova com os mesmos
elementos. A compreensão de lista `[row[:] for row in self._walls]` faz isso para cada linha e
junta as cópias numa lista nova.

Copiar as linhas basta, sem copiar os números: um `int` não muda, então as duas grades podem
compartilhar os mesmos inteiros sem risco. O que precisa ser novo são as **listas**, porque uma
lista pode ser alterada.

O [Experimente](#experimente), depois do arquivo completo, mostra a cópia mudando sem
mexer no `Maze`.

## A classe inteira

| Método | O problema que resolve | Página |
|---|---|---|
| `__init__` | criar a grade com tudo fechado | [O construtor](./09-o-construtor.md) |
| `__contains__` | a posição está dentro da grade? | [Consultar a grade](./02-consultar-a-grade.md) |
| `cells` | percorrer as células do labirinto, linha por linha, sem o "42" | [Consultar a grade](./02-consultar-a-grade.md) |
| `walls` | quais paredes de uma célula estão fechadas (0 a 15) | [Consultar a grade](./02-consultar-a-grade.md) |
| `neighbour` | a célula do outro lado de uma parede, ou `None` na borda e no "42" | [Vizinhos](./03-vizinhos.md) |
| `is_open` | dá para passar por este lado? | [Vizinhos](./03-vizinhos.md) |
| `open_wall`, `close_wall` | mudar uma parede, sempre nas duas células | [Abrir e fechar paredes](./04-abrir-e-fechar.md) |
| `_other_side` | recusar mudanças na borda e no "42" antes de escrever | [Abrir e fechar paredes](./04-abrir-e-fechar.md) |
| `passages` | os lados abertos, na ordem `N, E, S, W` | [Passagens e becos](./05-passagens-e-becos.md) |
| `closed_sides` | os lados fechados que poderiam abrir | [Passagens e becos](./05-passagens-e-becos.md) |
| `dead_ends` | os becos sem saída reais | [Passagens e becos](./05-passagens-e-becos.md) |
| `loop_count` | quantos ciclos independentes o labirinto tem | [Contar ciclos](./06-contar-ciclos.md) |
| `has_open_3x3`, `_window_open` | algum bloco 3x3 ficou sem paredes por dentro? | [Áreas abertas 3x3](./07-areas-abertas-3x3.md) |
| `rows` | entregar uma cópia da grade | esta |

## As docstrings

O enunciado pede docstrings (o texto entre `"""` que documenta) nas funções e nas classes,
seguindo a PEP 257, e cita os estilos Google e NumPy como exemplo. O projeto escolheu o Google
([parte 3](../03-ambiente/07-pacotes-do-mazegen.md)): um resumo de uma linha e, depois, as
seções que se aplicam:

- `Args:` os parâmetros, um por linha;
- `Returns:` o que o método devolve;
- `Yields:` o que uma função geradora (um método com `yield`, como o `cells`) entrega a cada
  passo;
- `Raises:` as exceções que ele pode levantar, e quando.

A docstring da classe registra as três regras que ela protege: coerência, borda fechada e "42"
fechado.

## O arquivo completo

O arquivo abaixo tem os mesmos imports e métodos montados ao longo desta parte, na mesma ordem,
agora com as docstrings. Ele substitui o `maze.py` montado até aqui.

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

        Stopping at the first closed wall rejects most windows after one
        or two reads, which keeps 100x100 Pac-Man boards fast.

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

## Experimente

Com o arquivo acima gravado em `mazegen/entities/maze.py`, na raiz do projeto
([como rodar os exemplos](../00-introducao/03-pre-requisitos.md#como-rodar-os-exemplos)):

```bash
.venv/bin/python - <<'EOF'
from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(3, 2, Pattern42.for_size(3, 2))
copy = maze.rows()
print(copy)
copy[0][0] = 0
print(copy[0][0], maze.walls(Cell(0, 0)))
EOF
```

```text
[[15, 15, 15], [15, 15, 15]]
0 15
```

A primeira linha é a grade 3x2 recém-criada, com 15 (as quatro paredes fechadas) em todas as
células. Depois de `copy[0][0] = 0`, a cópia tem 0 na célula `0,0`, e o `Maze` continua com 15:
a cópia mudou; o `Maze`, não.
