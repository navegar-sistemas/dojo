---
sidebar_position: 7
title: "Pattern42: consultar o padrão"
---

# `Pattern42`: consultar o padrão

Com as células do "42" calculadas pelo `for_size` (página
[Pattern42: o desenho e a posição](./05-pattern42-posicao.md)), o resto do programa precisa
perguntar ao padrão: "esta célula é do 42?". Esta página dá a essa pergunta a cara de Python
comum, `cell in pattern`, e mostra o arquivo completo.

## Quem pergunta

- O `Maze`, a grade de paredes ([parte 5](../05-maze/03-vizinhos.md)), pergunta para nunca
  abrir uma parede de célula do "42".
- O `MazeGenerator`, a classe principal do gerador ([parte 9](../09-gerador/02-validar-os-parametros.md)),
  e o `MazeConfig`, as opções lidas do arquivo de configuração
  ([parte 11](../11-configuracao/04-o-42-e-o-arquivo-completo.md)), perguntam para recusar uma
  entrada ou uma saída em cima do desenho.

Saber se o "42" coube na grade não precisa de método: quando a grade é menor que 9x7, o campo
`cells` fica vazio, e um conjunto vazio conta como "falso" num `if`. A pergunta se faz ao
**campo**, não ao padrão:

```python
if pattern.cells:
    print("o 42 coube")
```

`if pattern:` não serve: o próprio objeto `Pattern42` conta sempre como verdadeiro, mesmo vazio,
porque a classe não diz ao Python como responder a essa pergunta.

## Métodos especiais

O Python tem métodos com nomes entre dois sublinhados de cada lado, como `__init__`, que ele
mesmo chama em certas situações. São os **métodos especiais**. Um deles transforma a pergunta
acima em sintaxe comum:

| Quando o código escreve... | O Python chama... |
|---|---|
| `x in objeto` | `objeto.__contains__(x)` |

## `__contains__`: o operador `in`

```python
    def __contains__(self, cell: object) -> bool:
        return isinstance(cell, Cell) and cell in self.cells
```

`cell in pattern` chama esse método, que responde se a célula está no `frozenset` de células.

O tipo do parâmetro é `object`, "qualquer coisa": o lado esquerdo de um `in` pode ser qualquer
valor, e é assim que o próprio Python declara esse método. Por isso a primeira parte confere o
tipo. `isinstance(cell, Cell)` responde se `cell` é uma `Cell`.

### Só uma `Cell` pertence

O `and` do Python **para na primeira parte falsa**: se `isinstance` dá `False`, a busca no
`frozenset` nem é feita. Isso decide dois casos:

- **Uma tupla nunca pertence.** `(6, 5) in pattern` é `False`, mesmo com `Cell(6, 5)` no padrão.
  Dentro do `mazegen` toda posição é `Cell`; uma tupla ali é engano de quem chamou. Responder
  `False` não muda nenhuma resposta: mesmo sem o `isinstance`, a busca no `frozenset` daria
  `False`, porque `(6, 5) == Cell(6, 5)` é `False` (o `==` da dataclass só compara uma `Cell`
  com outra `Cell`).
- **Um objeto sem hash não quebra a consulta.** Procurar uma lista num conjunto levanta erro, porque
  uma lista não tem hash (o número que o conjunto usa para achar as coisas rápido, explicado na
  [página da Cell](./04-cell.md)). O texto do erro muda conforme a versão do Python. Do 3.10 ao
  3.13:

  ```text
  TypeError: unhashable type: 'list'
  ```

  A partir do 3.14, a mensagem explica um pouco mais:

  ```text
  TypeError: cannot use 'list' as a set element (unhashable type: 'list')
  ```

  Com o `isinstance` na frente, `[6, 5] in pattern` responde só `False`.

Quem tem uma tupla converte antes de perguntar: o `MazeConfig` consulta com
`Cell(x, y) in pattern`.

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
```

## Experimente

Com o arquivo acima gravado em `mazegen/value_objects/pattern42.py`, na raiz do projeto
([como rodar os exemplos](../00-introducao/03-pre-requisitos.md#como-rodar-os-exemplos)):

```bash
.venv/bin/python - <<'EOF'
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

p = Pattern42.for_size(20, 15)
xs = [cell.x for cell in p.cells]
ys = [cell.y for cell in p.cells]
print(len(p.cells), min(xs), max(xs), min(ys), max(ys))
print(Pattern42.for_size(8, 7))
print(Cell(6, 5) in p, Cell(9, 7) in p)
print((6, 5) in p, [6, 5] in p)
EOF
```

```text
18 6 12 5 9
Pattern42(cells=frozenset())
True False
False False
```

- `xs` e `ys` são compreensões de lista (*list comprehensions*, a lista montada por um `for`
  entre colchetes): as colunas e as linhas das 18 células. Em 20x15, o "42" ocupa as colunas 6 a
  12 e as linhas 5 a 9.
- Em 8x7, o padrão é vazio: `frozenset()` sem nada dentro.
- `6,5` é o canto de cima à esquerda do "4" numa grade 20x15; `9,7` é a coluna livre entre os
  dois dígitos.
- A tupla e a lista não pertencem, e a lista não causa erro.
