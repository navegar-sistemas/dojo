---
sidebar_position: 4
title: Abrir e fechar paredes
---

# Abrir e fechar paredes

## Os únicos métodos que mudam a grade

`open_wall` e `close_wall` são as duas únicas portas de escrita em `_walls`. Todas as regras da
grade dependem deles:

| Regra | Como os dois métodos a garantem |
|---|---|
| **coerência**: o Leste de `(x, y)` é igual ao Oeste de `(x + 1, y)` | mexem nas duas células de uma vez |
| **borda fechada** | recusam uma parede sem vizinha |
| **"42" fechado** | recusam uma parede de célula do "42" ou voltada para ela |
| cada célula entre `0` e `15` | só ligam ou desligam um bit |

## `open_wall`

```python
    def open_wall(self, cell: Cell, side: Direction) -> None:
        other = self._other_side(cell, side)
        self._walls[cell.y][cell.x] &= ~side
        self._walls[other.y][other.x] &= ~side.opposite
```

1. `_other_side` encontra a célula do outro lado da parede, ou levanta erro (abaixo).
2. Desliga o bit `side` na célula.
3. Desliga o bit **oposto** na vizinha.

`~side` inverte todos os bits do lado: para `EAST` (`0b0010`), dá uma máscara com todos os bits
ligados menos o bit 1. O `&=` mantém os outros bits como estavam e apaga só aquele. O resultado
é um `int`, porque operação de bits com `IntEnum` devolve `int`.

Abrir o Leste de `(0, 0)` muda as duas células: `15 - 2 = 13` em `(0, 0)` e `15 - 8 = 7` em
`(1, 0)`:

![A grade 3 por 2 depois de abrir a parede entre 0,0 e 1,0](/img/maze/abrir-depois.svg)

## `close_wall`

```python
    def close_wall(self, cell: Cell, side: Direction) -> None:
        other = self._other_side(cell, side)
        self._walls[cell.y][cell.x] |= side
        self._walls[other.y][other.x] |= side.opposite
```

O espelho de `open_wall`: liga os dois bits com `|=`. Só o `Braider` (parte 8) o usa, para
desfazer uma abertura que criou uma área aberta 3x3.

## `_other_side`: a guarda

```python
    def _other_side(self, cell: Cell, side: Direction) -> Cell:
        other = self.neighbour(cell, side)
        if other is None or cell in self.pattern:
            raise MazeError('internal: cannot change a border or "42" wall')
        return other
```

As duas operações começam pela mesma verificação, então ela mora num método auxiliar, privado
(o `_` no nome). A parede só pode mudar quando:

- existe vizinha do outro lado (`neighbour` não é `None`): nem borda, nem célula do "42" do
  outro lado;
- a própria célula não é do "42". `neighbour` não olha a célula de partida, por isso a segunda
  condição.

O erro vem **antes** de qualquer escrita: se a parede não pode mudar, a grade fica intacta.

### Por que levantar erro, e não ignorar

Um algoritmo correto nunca pede para abrir a borda: ele só abre paredes que `neighbour` aprovou.
Se o pedido chega, há um bug no algoritmo. Ignorar o pedido em silêncio esconderia o bug e
produziria um labirinto diferente do esperado; levantar `MazeError` faz o bug aparecer na hora,
no ponto exato.

A mensagem começa com `internal:` (parte 4): é um defeito do programa, não um erro do usuário.

## Experimente

```python
from mazegen.entities.maze import Maze
from mazegen.errors import MazeError
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(3, 2, Pattern42.for_size(3, 2))
maze.open_wall(Cell(0, 0), Direction.EAST)
print(maze.rows())
maze.close_wall(Cell(1, 0), Direction.WEST)
print(maze.rows())
try:
    maze.open_wall(Cell(0, 0), Direction.NORTH)
except MazeError as error:
    print(error)
```

```text
[[13, 7, 15], [15, 15, 15]]
[[15, 15, 15], [15, 15, 15]]
internal: cannot change a border or "42" wall
```

Fechar o Oeste de `(1, 0)` desfaz a abertura feita a partir de `(0, 0)`: é a mesma parede vista
do outro lado.
