---
sidebar_position: 3
title: O código do Solver
---

# O código do Solver

O `Solver` é um service sem estado, em `mazegen/services/solver.py`.

## Os imports

```python
from collections import deque

from mazegen.entities.maze import Maze
from mazegen.errors import MazeError
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
```

`deque` é a fila. `MazeError` aparece para o caso que nunca deveria acontecer, explicado abaixo.

## A assinatura

```python
    def shortest_path(self, maze: Maze, start: Cell, goal: Cell) -> str:
```

Recebe o labirinto já escavado, a entrada e a saída. Devolve uma `str` com uma letra por passo:
um caminho de `n` células tem `n − 1` letras. Entrada e saída nunca são a mesma célula (o
`MazeGenerator` recusa), então a string nunca sai vazia.

## A busca

```python
        parents: dict[Cell, tuple[Cell, Direction] | None] = {start: None}
        queue: deque[Cell] = deque([start])
        while queue:
            current = queue.popleft()
            if current == goal:
                break
            for side in maze.passages(current):
                nxt = current.step(side)
                if nxt not in parents:
                    parents[nxt] = (current, side)
                    queue.append(nxt)
```

- O tipo de `parents` diz tudo: cada célula aponta para o par `(anterior, lado)`, ou para
  `None` no caso da entrada.
- `if current == goal: break`: assim que a saída sai da fila, o resto do labirinto não interessa.
- `maze.passages(current)` (parte 5) devolve só os lados **abertos**, na ordem N, E, S, W. Uma
  passagem nunca dá para a borda nem para o "42", porque essas paredes nunca abrem; o `Solver`
  não precisa checar limites.
- `nxt not in parents` é o teste de "já descoberta". A primeira descoberta vence.

## A saída inalcançável

```python
        if goal not in parents:
            raise MazeError("internal: exit is not reachable from entry")
```

Se a fila esvaziou sem descobrir a saída, não existe caminho. Num labirinto gerado pelo
`MazeGenerator` isso não acontece:

- o `Carver` liga todas as células livres;
- o construtor do `MazeGenerator` garante que a saída é uma célula livre, dentro da grade e fora
  do "42".

Se acontecer, é bug. O prefixo `internal:` segue a convenção do `MazeError` (parte 4): a
mensagem aponta para um defeito do código, não para um erro de quem usa. Devolver uma string
vazia em silêncio esconderia o defeito e gravaria um arquivo de saída errado.

### Experimente

Um `Maze` 2x1 com todas as paredes fechadas, sem passar pelo `Carver`:

```python
from mazegen.entities.maze import Maze
from mazegen.services.solver import Solver
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

closed = Maze(2, 1, Pattern42.for_size(2, 1))
Solver().shortest_path(closed, Cell(0, 0), Cell(1, 0))
```

A última linha da saída:

```text
mazegen.errors.MazeError: internal: exit is not reachable from entry
```

## A reconstrução

```python
        letters: list[str] = []
        link = parents[goal]
        while link is not None:
            previous, side = link
            letters.append(side.letter)
            link = parents[previous]
        letters.reverse()
        return "".join(letters)
```

- `link` começa no par da saída e anda de pai em pai; o laço para no `None` da entrada.
- As letras são acumuladas numa lista e unidas no fim com `"".join`. Somar strings uma a uma
  dentro do laço criaria uma string nova a cada passo.
- `reverse()` inverte a lista no lugar: as letras foram lidas da saída para a entrada.

## O arquivo completo

```python title="mazegen/services/solver.py"
"""Breadth-first search for the shortest path of a maze."""

from collections import deque

from mazegen.entities.maze import Maze
from mazegen.errors import MazeError
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction


class Solver:
    """Find the shortest path between two cells through the passages."""

    def shortest_path(self, maze: Maze, start: Cell, goal: Cell) -> str:
        """Search breadth-first, neighbours in the order N, E, S, W.

        A cell keeps the parent of its first discovery, so equal-length
        paths always resolve to the same letters.

        Args:
            maze: Carved maze.
            start: Entry cell.
            goal: Exit cell.

        Returns:
            One letter N, E, S or W per step from start to goal.

        Raises:
            MazeError: The goal is not reachable, which points to a bug.
        """
        parents: dict[Cell, tuple[Cell, Direction] | None] = {start: None}
        queue: deque[Cell] = deque([start])
        while queue:
            current = queue.popleft()
            if current == goal:
                break
            for side in maze.passages(current):
                nxt = current.step(side)
                if nxt not in parents:
                    parents[nxt] = (current, side)
                    queue.append(nxt)
        if goal not in parents:
            raise MazeError("internal: exit is not reachable from entry")
        letters: list[str] = []
        link = parents[goal]
        while link is not None:
            previous, side = link
            letters.append(side.letter)
            link = parents[previous]
        letters.reverse()
        return "".join(letters)
```
