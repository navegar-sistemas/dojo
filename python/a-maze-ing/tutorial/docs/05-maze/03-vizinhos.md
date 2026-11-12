---
sidebar_position: 3
title: 'Vizinhos: a borda e o "42"'
---

# Vizinhos: a borda e o "42"

## `neighbour`

```python
    def neighbour(self, cell: Cell, side: Direction) -> Cell | None:
        other = cell.step(side)
        if other not in self or other in self.pattern:
            return None
        return other
```

A célula do outro lado de uma parede, **se ela faz parte do labirinto**. Devolve `None` em dois
casos:

- o passo cai **fora da grade** (`other not in self`, o `__contains__` da página anterior);
- o passo cai **numa célula do "42"** (`other in self.pattern`).

Na grade 9x7, a partir de `(0, 1)`:

![Vizinhos de 0,1 numa grade 9 por 7: Norte e Sul existem, Leste é do 42 e Oeste está fora](/img/maze/vizinhos-9x7.svg)

## Por que a borda e o "42" dão a mesma resposta

Para os algoritmos, uma célula do "42" e uma posição fora da grade são a mesma coisa: um lugar
onde não se entra. Com `neighbour` devolvendo `None` nos dois casos, basta uma condição. O `Carver`
(parte 6) escolhe para onde cavar assim:

```python
nxt = maze.neighbour(current, side)
if nxt is not None and nxt not in visited:
    options.append(side)
```

O `Solver` e o `Braider` (partes 7 e 8) usam `passages` e `closed_sides`, que chamam
`neighbour` por dentro. Nenhum dos três conhece o desenho do "42" nem confere limites: se o "42"
mudasse de forma, só o `Pattern42` mudaria.

O tipo de retorno `Cell | None` obriga isso: o mypy recusa usar o resultado como `Cell` antes de
descartar o `None`.

## `is_open`: há passagem?

```python
    def is_open(self, cell: Cell, side: Direction) -> bool:
        return (self.neighbour(cell, side) is not None
                and not self.walls(cell) & side)
```

Um lado é passagem quando há uma vizinha **e** o bit daquele lado está desligado.

`self.walls(cell) & side` isola o bit do lado: dá `side` (diferente de zero) se a parede está
fechada, `0` se está aberta. O `not` transforma isso em "aberta?".

A primeira condição parece redundante, porque a borda e o "42" nunca são abertos. Ela deixa a
resposta certa mesmo assim: a parede da borda **nunca** é passagem, seja qual for o bit.

### Precedência

`not self.walls(cell) & side` é lido como `not (self.walls(cell) & side)`: no Python, o `&`
tem precedência maior que o `not`, então os parênteses não são necessários.

## Experimente

```python
from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(9, 7, Pattern42.for_size(9, 7))
for side in Direction:
    print(side.letter, maze.neighbour(Cell(0, 1), side))
maze.open_wall(Cell(0, 1), Direction.SOUTH)
print(maze.is_open(Cell(0, 1), Direction.SOUTH),
      maze.is_open(Cell(0, 1), Direction.WEST))
```

```text
N Cell(x=0, y=0)
E None
S Cell(x=0, y=2)
W None
True False
```

`(1, 1)`, à direita de `(0, 1)`, é o canto de cima do "4" em 9x7.
