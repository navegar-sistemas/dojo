---
sidebar_position: 3
title: "Direction: oposto, passo e letra"
---

# `Direction`: oposto, passo e letra

## Três perguntas sobre um lado

| Propriedade | `NORTH` | `EAST` | `SOUTH` | `WEST` | Quem usa |
|---|---|---|---|---|---|
| `opposite` | `SOUTH` | `WEST` | `NORTH` | `EAST` | `Maze`, para manter as duas células coerentes |
| `dx` | `0` | `1` | `0` | `-1` | `Cell.step`, para andar um passo |
| `dy` | `-1` | `0` | `1` | `0` | `Cell.step` |
| `letter` | `"N"` | `"E"` | `"S"` | `"W"` | o `Solver`, para escrever o caminho |

### `opposite`

A parede Leste de uma célula é a parede Oeste da vizinha da direita. Ao abrir o Leste de
`(x, y)`, o `Maze` (parte 5) também abre o `EAST.opposite`, isto é, o Oeste, de `(x + 1, y)`.

### `dx` e `dy`

Quanto `x` e `y` mudam num passo para aquele lado. Como `y` é a linha e cresce **para baixo**,
o Norte é `dy = -1`:

![Os quatro deltas em volta de uma célula](/img/value-objects/direction-deltas.svg)

### `letter`

O caminho mais curto é gravado no arquivo como uma sequência de letras `N`, `E`, `S` e `W`, uma
por passo. `side.letter` dá a letra sem depender do `str()` do enum.

## Propriedades que leem tabelas

```python
    @property
    def opposite(self) -> "Direction":
        return _OPPOSITE[self.value]
```

`@property` faz o método ser lido como atributo: `side.dx`, sem parênteses. Combina com o que
ele é: um dado fixo do lado, não uma ação.

`"Direction"` vai entre aspas porque, enquanto o corpo da classe executa, o nome `Direction`
ainda não existe. A anotação em texto é resolvida depois pelo mypy.

Cada propriedade só consulta um dicionário com o valor do lado:

```python
_OPPOSITE: dict[int, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}
_DELTA: dict[int, tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}
```

`_DELTA` guarda o par `(dx, dy)`: `dx` lê a posição `[0]` e `dy` a posição `[1]`. O `_` no nome
diz que as tabelas são internas ao módulo.

## Por que as tabelas ficam fora da classe

Dentro do corpo de um `Enum`, **toda atribuição vira um membro**. Uma tabela escrita ali dentro
viraria um quinto "lado", e o `IntEnum` tentaria convertê-la em inteiro:

```python
class Direction(IntEnum):
    NORTH = 1
    SOUTH = 4
    _OPPOSITE = {NORTH: SOUTH}
```

A classe nem chega a ser criada: o Python levanta `TypeError`, porque `int()` não aceita um
`dict`.

Além disso, dentro do corpo, `NORTH` ainda é o inteiro `1`, não o membro `Direction.NORTH`: a
tabela guardaria inteiros, e `opposite` devolveria `int` em vez de `Direction`.

Depois da classe pronta, os membros existem, e as tabelas podem usá-los. As propriedades só leem
as tabelas quando são chamadas, e nessa hora o módulo inteiro já foi carregado.

### E um `if`/`elif`?

Cada propriedade poderia testar os quatro lados com `if`. Seriam quatro blocos de oito linhas
quase iguais, e um erro de digitação num deles passaria despercebido. As tabelas põem os
valores lado a lado, onde dá para conferir de uma vez.

## Experimente

```python
from mazegen.value_objects.direction import Direction

for side in Direction:
    print(side.name, side.opposite.name, side.dx, side.dy, side.letter)
```

```text
NORTH SOUTH 0 -1 N
EAST WEST 1 0 E
SOUTH NORTH 0 1 S
WEST EAST -1 0 W
```

## O arquivo completo

```python title="mazegen/value_objects/direction.py"
"""The four sides of a cell and the wall bit of each one."""

from enum import IntEnum


class Direction(IntEnum):
    """Side of a cell; the value is the wall bit in the output file.

    Iterating the enum yields NORTH, EAST, SOUTH and WEST, the neighbour
    order of the breadth-first search.
    """

    NORTH = 1
    EAST = 2
    SOUTH = 4
    WEST = 8

    @property
    def opposite(self) -> "Direction":
        """Side that faces this one across a shared wall.

        Returns:
            The opposite direction.
        """
        return _OPPOSITE[self.value]

    @property
    def dx(self) -> int:
        """Column offset of one step towards this side.

        Returns:
            -1, 0 or 1.
        """
        return _DELTA[self.value][0]

    @property
    def dy(self) -> int:
        """Row offset of one step towards this side.

        Returns:
            -1, 0 or 1.
        """
        return _DELTA[self.value][1]

    @property
    def letter(self) -> str:
        """Letter of this side in the shortest path.

        Returns:
            "N", "E", "S" or "W".
        """
        return _LETTER[self.value]


_OPPOSITE: dict[int, Direction] = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}
_DELTA: dict[int, tuple[int, int]] = {
    Direction.NORTH: (0, -1),
    Direction.EAST: (1, 0),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
}
_LETTER: dict[int, str] = {
    Direction.NORTH: "N",
    Direction.EAST: "E",
    Direction.SOUTH: "S",
    Direction.WEST: "W",
}
```
