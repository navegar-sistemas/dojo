---
sidebar_position: 4
title: Cell
---

# `Cell`

## O que é

Uma posição na grade: a coluna `x` e a linha `y`, ambas a partir de 0, com a origem no canto de
cima à esquerda. Dentro do `mazegen`, toda célula é uma `Cell`; fora dele (no config, na API
pública, na aplicação), é uma tupla `(x, y)`.

## Por que não uma tupla

Uma tupla `(3, 4)` funcionaria, mas:

- `cell.x` diz o que é; `pos[0]` obriga a lembrar que o primeiro elemento é a coluna;
- o mypy distingue uma `Cell` de qualquer outro par de inteiros (um `(dx, dy)`, um
  `(largura, altura)`);
- a `Cell` tem um método, `step`, que anda até a vizinha.

Numa grade de 100x100, o custo extra de memória e de tempo é desprezível.

## `@dataclass(frozen=True, slots=True)`

```python
@dataclass(frozen=True, slots=True)
class Cell:
    x: int
    y: int
```

`@dataclass` gera o `__init__`, o `__repr__` e o `__eq__` a partir dos campos anotados:
`Cell(3, 4) == Cell(3, 4)` compara `x` e `y`, não a identidade dos objetos.

### `frozen=True`: imutável e com hash

Uma `Cell` não muda depois de criada. Tentar alterar um campo levanta erro:

```python
cell = Cell(3, 4)
cell.x = 5      # dataclasses.FrozenInstanceError: cannot assign to field 'x'
```

Com `frozen=True` e a igualdade por conteúdo, o `@dataclass` também gera o `__hash__`. Isso
permite guardar células num `set` ou usá-las como chave de `dict`, que é como os algoritmos
registram "já visitei esta célula" e "de onde vim". Um objeto mutável como chave seria um
perigo: se mudasse depois de entrar no `set`, ficaria perdido na posição errada da tabela.

### `slots=True`: sem `__dict__`

Normalmente, cada objeto Python carrega um dicionário com os seus atributos. Com `slots=True`, a
classe reserva espaço só para `x` e `y`: cada célula ocupa menos memória e não aceita atributos
inventados. É um recurso do Python 3.10, a versão mínima do projeto.

## `step`: a vizinha, sem conferir limites

```python
    def step(self, direction: Direction) -> "Cell":
        return Cell(self.x + direction.dx, self.y + direction.dy)
```

Soma o deslocamento do lado à posição:

![Os quatro passos a partir da célula 3,4](/img/value-objects/cell-step.svg)

A `Cell` não sabe o tamanho da grade, então `step` **não confere limites**. Do canto `(0, 0)`, o
passo para o Norte dá `(0, -1)`, uma posição que não existe:

![Do canto 0,0 dois passos caem fora da grade](/img/value-objects/cell-step-canto.svg)

Quem sabe o tamanho da grade é o `Maze` (parte 5): o `Maze.neighbour` chama `step` e devolve
`None` quando o resultado cai fora. Cada classe responde pelo que conhece.

## `as_tuple`: a saída do `mazegen`

```python
    def as_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
```

A API pública do gerador fala em tuplas: `entry=(0, 0)`, e `pattern` é um conjunto de tuplas.
`as_tuple` faz a conversão no ponto em que uma célula sai do pacote.

## Experimente

```python
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction

cell = Cell(3, 4)
print(cell.step(Direction.NORTH), cell.step(Direction.WEST).as_tuple())
print(Cell(0, 0).step(Direction.NORTH))
print(cell == Cell(3, 4), len({cell, Cell(3, 4)}))
print(hasattr(cell, "__dict__"))
```

```text
Cell(x=3, y=3) (2, 4)
Cell(x=0, y=-1)
True 1
False
```

As duas `Cell(3, 4)` são iguais e têm o mesmo hash, então o `set` guarda uma só.

## O arquivo completo

```python title="mazegen/value_objects/cell.py"
"""Position of a cell in the maze grid."""

from dataclasses import dataclass

from mazegen.value_objects.direction import Direction


@dataclass(frozen=True, slots=True)
class Cell:
    """Immutable grid position, origin at the top-left corner.

    Attributes:
        x: Column, from 0.
        y: Row, from 0.
    """

    x: int
    y: int

    def step(self, direction: Direction) -> "Cell":
        """Cell next to this one towards a side, without bounds checking.

        Args:
            direction: Side to move to.

        Returns:
            The neighbouring position; the Maze decides whether it exists.
        """
        return Cell(self.x + direction.dx, self.y + direction.dy)

    def as_tuple(self) -> tuple[int, int]:
        """Plain coordinates used outside the mazegen package.

        Returns:
            The pair (x, y).
        """
        return (self.x, self.y)
```
