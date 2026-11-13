---
sidebar_position: 4
title: O código do Solver
---

# O código do Solver

Quando a busca da [página anterior](./04-a-busca-do-solver.md) termina, o dicionário
`parents` tem o pai de cada célula descoberta, mas o `Solver` ainda precisa devolver o
caminho em letras, e decidir o que fazer se a saída nunca foi descoberta. Esta página escreve
esses dois trechos e mostra o arquivo `mazegen/services/solver.py` inteiro.

## A saída inalcançável

```python
        if goal not in parents:
            raise MazeError("internal: exit is not reachable from entry")
```

Se a fila esvaziou sem descobrir a saída, não existe caminho até ela. `raise` interrompe o método
e **levanta** (lança) a exceção: ela sobe para quem chamou o método, que pode capturá-la com
`try`/`except`. Num labirinto gerado pelo `MazeGenerator`, isso não acontece:

- o `Carver` liga todas as células livres ([parte 6](../06-carver/01-labirinto-perfeito.md));
- o `MazeGenerator` garante que a saída fica dentro da grade e fora do "42".

Se acontecer, é bug. O começo `internal:` da mensagem é a convenção do `MazeError` para "defeito
do código, não erro de quem usa" ([parte 4](../04-value-objects/01-maze-error.md)). A alternativa,
devolver uma string vazia em silêncio, esconderia o defeito e gravaria um arquivo de saída
errado.

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

- `link` começa com o par `(pai, lado)` da saída e vai de pai em pai. O laço para no `None` da
  entrada.
- `previous, side = link` desmonta a tupla em duas variáveis: o pai e o lado do passo.
- `side.letter` é a letra do lado (`"N"`, `"E"`, `"S"` ou `"W"`).
- `letters.reverse()` inverte a lista no lugar: as letras foram lidas da saída para a entrada.
- `"".join(letters)` cola as letras numa string só, sem nada entre elas. Somar as strings uma a
  uma dentro do laço (`texto = texto + letra`) criaria uma string nova a cada passo.

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

## Experimente

O exemplo da [página 2](./02-pais-e-letras.md): abre à mão todas as paredes internas de uma grade
3x2 (`open_wall` derruba uma parede, [parte 5](../05-maze/04-abrir-e-fechar.md)) e pede o caminho
nos dois sentidos. Depois, um `Maze` 2x1 com todas as paredes fechadas, sem passar pelo `Carver`:
a saída não tem como ser alcançada. Na raiz do projeto:

```bash
.venv/bin/python - <<'EOF'
from mazegen.entities.maze import Maze
from mazegen.errors import MazeError
from mazegen.services.solver import Solver
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(3, 2, Pattern42.for_size(3, 2))
for x in range(3):
    maze.open_wall(Cell(x, 0), Direction.SOUTH)
    if x < 2:
        maze.open_wall(Cell(x, 0), Direction.EAST)
        maze.open_wall(Cell(x, 1), Direction.EAST)
print(maze.rows())
print(Solver().shortest_path(maze, Cell(0, 0), Cell(2, 1)))
print(Solver().shortest_path(maze, Cell(2, 1), Cell(0, 0)))

closed = Maze(2, 1, Pattern42.for_size(2, 1))
try:
    Solver().shortest_path(closed, Cell(0, 0), Cell(1, 0))
except MazeError as error:
    print("MazeError:", error)
EOF
```

```text
[[9, 1, 3], [12, 4, 6]]
EES
NWW
MazeError: internal: exit is not reachable from entry
```

- `maze.rows()` mostra as paredes de cada célula como números (`9` = Norte e Oeste fechados, por
  exemplo, [parte 1](../01-o-problema/02-paredes-em-bits.md)); só a borda ficou fechada.
- `EES` e `NWW` são os caminhos do desempate: vizinhas na ordem N, E, S, W, e vale o pai da
  primeira descoberta.
- No `Maze` fechado, o `Solver` levanta o `MazeError`. O `try`/`except` o captura só para imprimir
  a mensagem numa linha.
