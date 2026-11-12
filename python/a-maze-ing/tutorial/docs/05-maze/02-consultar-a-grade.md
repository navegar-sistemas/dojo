---
sidebar_position: 2
title: Consultar a grade
---

# Consultar a grade

Três perguntas simples, que os outros métodos usam o tempo todo: a posição está dentro da grade?
quais são as células do labirinto? quais paredes de uma célula estão fechadas?

## `__contains__`: dentro da grade?

```python
    def __contains__(self, cell: object) -> bool:
        return (isinstance(cell, Cell) and 0 <= cell.x < self.width
                and 0 <= cell.y < self.height)
```

`cell in maze` é `True` quando a posição existe: coluna de `0` a `width - 1` e linha de `0` a
`height - 1`. É a mesma ideia do `Pattern42.__contains__` (parte 4): só uma `Cell` responde
`True`.

`0 <= cell.x < self.width` é uma comparação encadeada: o Python a lê como
`0 <= cell.x and cell.x < self.width`.

Essa é a pergunta que a `Cell` não sabe responder: o `step` da parte 4 devolve qualquer posição,
e o `Maze` decide se ela existe.

## `cells`: as células do labirinto

```python
    def cells(self) -> Iterator[Cell]:
        for y in range(self.height):
            for x in range(self.width):
                cell = Cell(x, y)
                if cell not in self.pattern:
                    yield cell
```

Percorre a grade linha por linha (`y` por fora, `x` por dentro), a mesma ordem de leitura do
arquivo de saída, e **pula as células do "42"**. Elas não fazem parte do labirinto: não têm
passagem, não são becos, não contam nos ciclos.

### Por que `yield`

Uma função com `yield` é um **gerador**: em vez de montar uma lista inteira e devolvê-la, ela
entrega uma célula de cada vez, quando o `for` de quem chamou pede a próxima. Por isso o tipo de
retorno é `Iterator[Cell]`.

Quem só quer percorrer as células (`for cell in maze.cells():`) não paga uma lista de 10 000
posições numa grade de 100x100. Quem precisa da lista pode pedir `list(maze.cells())`.

## `walls`: as paredes de uma célula

```python
    def walls(self, cell: Cell) -> int:
        return self._walls[cell.y][cell.x]
```

A máscara da célula, de `0` a `15`, com um bit por parede fechada. Note a ordem dos índices:
primeiro a linha (`y`), depois a coluna (`x`), porque `_walls` é uma lista de linhas.

`walls` é só leitura e não confere limites: quem chama já sabe que a célula está na grade.

## Experimente

```python
from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(9, 7, Pattern42.for_size(9, 7))
print(Cell(8, 6) in maze, Cell(9, 0) in maze, (0, 0) in maze)
print(len(list(maze.cells())), 9 * 7 - len(maze.pattern.cells))
print([cell.as_tuple() for cell in maze.cells()][:5])
print(maze.walls(Cell(0, 0)))
```

```text
True False False
45 45
[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
15
```

Uma grade 9x7 tem 63 posições; tirando as 18 do "42", o labirinto tem 45 células.
