---
sidebar_position: 2
title: O caminho em células
---

# O caminho em células

O `solution` é o caminho em **letras**: `EES` quer dizer "Leste, Leste, Sul". O arquivo de saída
grava exatamente essas letras, mas o desenho (parte 13) precisa saber **quais células** pintar de
ciano. O método `path()` do `GeneratedMaze` faz a tradução.

![Labirinto 3 por 2 com o caminho EES e o índice de cada célula do caminho](/img/geracao/caminho-3x2.svg)

Partindo da entrada `(0, 0)`:

| Passo | Letra | Deslocamento | Célula |
|---|---|---|---|
| início | | | `(0, 0)` |
| 1 | `E` | `dx = 1`, `dy = 0` | `(1, 0)` |
| 2 | `E` | `dx = 1`, `dy = 0` | `(2, 0)` |
| 3 | `S` | `dx = 0`, `dy = 1` | `(2, 1)` |

Três letras viram quatro células: a entrada mais uma por passo. A última é a saída.

## Da letra à direção

A `Direction` do `mazegen` (parte 4) já sabe, para cada lado, a letra (`letter`) e o
deslocamento (`dx`, `dy`). Falta o caminho inverso: da letra à direção. Um dicionário montado uma
vez, no carregamento do módulo:

```python
_BY_LETTER = {side.letter: side for side in Direction}
```

Percorrer um `Enum` dá os seus membros, então o dicionário fica
`{"N": NORTH, "E": EAST, "S": SOUTH, "W": WEST}`. Montá-lo **a partir** da `Direction`, em vez de
escrever as quatro entradas à mão, garante que as letras e os deslocamentos são os mesmos que o
`Solver` usou para escrever o caminho.

## O método

```python
def path(self) -> list[tuple[int, int]]:
    x, y = self.entry
    cells = [(x, y)]
    for letter in self.solution:
        side = _BY_LETTER[letter]
        x, y = x + side.dx, y + side.dy
        cells.append((x, y))
    return cells
```

1. Começa na entrada, que já é a primeira célula do caminho.
2. Para cada letra, acha a direção e anda um passo.
3. Guarda cada célula visitada.

O resultado tem sempre `len(solution) + 1` células, da entrada à saída.

### Por que recalcular em vez de guardar

O caminho em células poderia ser mais um campo do retrato. Mas o arquivo grava as letras, e as
células são deriváveis delas: guardar as duas formas abriria espaço para elas discordarem. Com
`path()`, há uma fonte só (o `solution`), e a tela pinta exatamente o caminho que o arquivo
grava. Calcular é barato: uma soma por passo, e mesmo numa grade 100x100 o caminho tem no
máximo 10 000 células.

## Experimente

```bash
.venv/bin/python -c '
from amazeing.domain.value_objects.generated_maze import GeneratedMaze

maze = GeneratedMaze(((9, 1, 3), (12, 4, 6)), (0, 0), (2, 1), "EES",
                     frozenset())
print(maze.path())
'
```

```text
[(0, 0), (1, 0), (2, 0), (2, 1)]
```

O retrato também pode ser criado direto pelo construtor, com valores escritos à mão, como aqui:
útil para experimentar sem gerar um labirinto.

## O arquivo completo

```python title="amazeing/domain/value_objects/generated_maze.py"
"""Immutable snapshot of one generation."""

from dataclasses import dataclass

from mazegen import MazeGenerator
from mazegen.value_objects.direction import Direction

_BY_LETTER = {side.letter: side for side in Direction}


@dataclass(frozen=True)
class GeneratedMaze:
    """What the output file stores and the screen draws for one maze.

    The file and the screen always start from the same snapshot, so they
    cannot disagree.

    Attributes:
        grid: height rows of width wall masks.
        entry: Entry cell as (x, y).
        exit: Exit cell as (x, y).
        solution: Shortest path from entry to exit, one letter per step.
        pattern: (x, y) cells of the "42"; empty when it does not fit.
    """

    grid: tuple[tuple[int, ...], ...]
    entry: tuple[int, int]
    exit: tuple[int, int]
    solution: str
    pattern: frozenset[tuple[int, int]]

    @classmethod
    def from_generator(cls, generator: MazeGenerator, entry: tuple[int, int],
                       exit: tuple[int, int]) -> "GeneratedMaze":
        """Copy the result of the last generate() call.

        Args:
            generator: Generator right after generate().
            entry: Entry cell as (x, y).
            exit: Exit cell as (x, y).

        Returns:
            The snapshot.
        """
        return cls(tuple(tuple(row) for row in generator.grid), entry, exit,
                   generator.solution, frozenset(generator.pattern))

    def path(self) -> list[tuple[int, int]]:
        """Cells of the shortest path, rebuilt from entry and solution.

        Returns:
            len(solution) + 1 cells, from entry to exit.
        """
        x, y = self.entry
        cells = [(x, y)]
        for letter in self.solution:
            side = _BY_LETTER[letter]
            x, y = x + side.dx, y + side.dy
            cells.append((x, y))
        return cells
```

`MazeGenerator` vem de `mazegen`, o nome público do pacote; `Direction` vem pelo caminho
interno, porque o pacote só exporta `MazeGenerator` e `MazeError`.
