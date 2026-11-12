---
sidebar_position: 5
title: Passagens e becos
---

# Passagens e becos

## `passages`: os lados abertos

```python
    def passages(self, cell: Cell) -> list[Direction]:
        return [side for side in Direction if self.is_open(cell, side)]
```

Os lados de uma célula por onde se pode andar, na ordem `N, E, S, W` (a ordem de iteração do
`Direction`, parte 4). O `Solver` (parte 7) anda pelo labirinto com ele, e a ordem fixa é a que
a busca em largura precisa.

## `closed_sides`: as paredes que **poderiam** abrir

```python
    def closed_sides(self, cell: Cell) -> list[Direction]:
        return [
            side for side in Direction
            if self.neighbour(cell, side) is not None
            and self.walls(cell) & side
        ]
```

Os lados fechados **com uma vizinha livre do outro lado**. Uma parede da borda ou voltada para o
"42" está fechada, mas não entra na lista: ela nunca pode ser aberta.

`passages` e `closed_sides` juntos não cobrem os quatro lados. O que falta são justamente as
paredes permanentes.

## Beco sem saída

Um **beco** é uma célula com exatamente uma passagem: só se entra e sai pelo mesmo lado. O modo
Pac-Man (parte 8) tolera no máximo dois becos, então o `Braider` precisa achá-los e o gerador
precisa contá-los.

Mas nem todo beco é igual:

- **beco real**: tem uma parede fechada que dá para uma célula livre. Abrir essa parede acaba
  com o beco.
- **beco cercado**: todas as paredes fechadas dão para a borda ou para o "42". Não há o que
  abrir, então ele não conta.

O "42" sempre cria dois becos cercados: as células à direita do "4", nas linhas 1 e 3 do
desenho, têm uma única vizinha livre.

![Labirinto 9 por 7 com os becos reais em laranja e os cercados em amarelo](/img/maze/becos-9x7.svg)

## `dead_ends`: só os reais

```python
    def dead_ends(self) -> list[Cell]:
        return [
            cell for cell in self.cells()
            if len(self.passages(cell)) == 1 and self.closed_sides(cell)
        ]
```

Uma célula de `cells()` (fora do "42") com uma passagem **e** pelo menos uma parede que pode
abrir. Uma lista vazia é "falsa" no Python, então `and self.closed_sides(cell)` descarta os
becos cercados sem precisar de `len(...) > 0`.

É a mesma definição do `maze_analyzer.py` entregue com o subject, que conta os becos cercados à
parte, como tolerados.

## Experimente

A serpentina 3x2: um corredor só, que vai até o fim da primeira linha e volta pela segunda.

![A serpentina 3 por 2, com os dois becos reais em laranja](/img/maze/ciclos-serpentina.svg)

```python
from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(3, 2, Pattern42.for_size(3, 2))
for cell, side in [(Cell(0, 0), Direction.EAST), (Cell(1, 0), Direction.EAST),
                   (Cell(2, 0), Direction.SOUTH), (Cell(2, 1), Direction.WEST),
                   (Cell(1, 1), Direction.WEST)]:
    maze.open_wall(cell, side)
print(maze.rows())
print([side.letter for side in maze.passages(Cell(0, 0))],
      [side.letter for side in maze.closed_sides(Cell(0, 0))])
print([cell.as_tuple() for cell in maze.dead_ends()])
small = Maze(2, 1, Pattern42.for_size(2, 1))
small.open_wall(Cell(0, 0), Direction.EAST)
print(small.dead_ends())
```

```text
[[13, 5, 3], [13, 5, 6]]
['E'] ['S']
[(0, 0), (0, 1)]
[]
```

- `(0, 0)` tem uma passagem (Leste) e uma parede que pode abrir (Sul, para `(0, 1)`): beco real.
- Na grade 2x1 aberta, as duas células também têm uma passagem só, mas todas as paredes fechadas
  dão para a borda: são becos cercados, e `dead_ends()` devolve uma lista vazia.
