---
sidebar_position: 6
title: "Pattern42: consultar o padrão"
---

# `Pattern42`: consultar o padrão

## As duas perguntas

Quem usa o padrão faz duas perguntas:

- "esta célula é do 42?": o `Maze`, para não abrir paredes nela, e o `MazeConfig` (parte 11),
  para recusar `ENTRY` ou `EXIT` em cima do desenho;
- "o 42 coube?": o gerador e o menu, para avisar quando a grade é pequena demais.

Os métodos especiais `__contains__` e `__bool__` deixam as duas perguntas com a cara de Python
comum: `cell in pattern` e `if pattern:`.

## `__contains__`: o operador `in`

```python
    def __contains__(self, cell: object) -> bool:
        return isinstance(cell, Cell) and cell in self.cells
```

`x in objeto` chama `objeto.__contains__(x)`. O lado esquerdo do `in` pode ser qualquer coisa,
por isso o parâmetro é `object`, como no próprio protocolo do Python.

### Só uma `Cell` pertence

O `isinstance` vem antes da busca no `frozenset`, e isso decide dois casos:

- **uma tupla nunca pertence**: `(6, 5) in pattern` é `False` mesmo com `Cell(6, 5)` no padrão.
  Dentro do `mazegen` toda posição é `Cell`; uma tupla ali é engano de quem chamou, e o `False`
  não esconde nada, porque uma tupla nunca é igual a uma `Cell`.
- **um objeto sem hash não quebra a consulta**: `[6, 5] in frozenset(...)` levanta `TypeError`,
  porque uma lista não pode ser procurada num conjunto. Com o `isinstance` na frente, o `and`
  para antes, e a resposta é só `False`.

Quem tem uma tupla converte antes: o `MazeConfig` consulta com `Cell(x, y) in pattern`.

## `__bool__`: o padrão coube?

```python
    def __bool__(self) -> bool:
        return bool(self.cells)
```

`if pattern:` chama `pattern.__bool__()`. O padrão é "verdadeiro" quando tem células, ou seja,
quando o "42" coube na grade. Um padrão vazio (grade menor que 9x7) é "falso".

Sem esse método, todo objeto de uma classe comum é verdadeiro, e `if pattern:` daria `True`
mesmo para o padrão vazio.

## Experimente

```python
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

p = Pattern42.for_size(20, 15)
print(Cell(6, 5) in p, Cell(9, 7) in p)
print((6, 5) in p, [6, 5] in p)
print(bool(p), bool(Pattern42.for_size(8, 7)))
```

```text
True False
False False
True False
```

`(6, 5)` é o canto de cima à esquerda do "4" em 20x15. `(9, 7)` é a coluna livre entre os dois
dígitos.

## O arquivo completo

```python title="mazegen/value_objects/pattern42.py"
"""Cells of the "42" drawn by fully closed cells in the middle of the maze."""

from dataclasses import dataclass

from mazegen.value_objects.cell import Cell

GLYPHS = ("X...XXX", "X.....X", "XXX.XXX", "..X.X..", "..X.XXX")
PATTERN_WIDTH = 7
PATTERN_HEIGHT = 5
MIN_WIDTH = 9
MIN_HEIGHT = 7


@dataclass(frozen=True)
class Pattern42:
    """Immutable set of the "42" cells for one grid size.

    Attributes:
        cells: Cells drawn by an "X" of GLYPHS; empty when the "42" does
            not fit in the grid.
    """

    cells: frozenset[Cell]

    @classmethod
    def for_size(cls, width: int, height: int) -> "Pattern42":
        """Centre the "42" in a grid, or leave it out when it does not fit.

        The minimum size keeps at least one corridor cell between the block
        and every border.

        Args:
            width: Number of columns of the grid.
            height: Number of rows of the grid.

        Returns:
            The pattern; empty below MIN_WIDTH x MIN_HEIGHT.
        """
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            return cls(frozenset())
        x0 = (width - PATTERN_WIDTH) // 2
        y0 = (height - PATTERN_HEIGHT) // 2
        return cls(frozenset(
            Cell(x0 + dx, y0 + dy)
            for dy, row in enumerate(GLYPHS)
            for dx, char in enumerate(row)
            if char == "X"
        ))

    def __contains__(self, cell: object) -> bool:
        """Tell whether a cell belongs to the "42".

        Args:
            cell: Object to look up; only a Cell can belong.

        Returns:
            True for a Cell of the pattern.
        """
        return isinstance(cell, Cell) and cell in self.cells

    def __bool__(self) -> bool:
        """Tell whether the "42" fits in the grid.

        Returns:
            False when the pattern is empty.
        """
        return bool(self.cells)
```
