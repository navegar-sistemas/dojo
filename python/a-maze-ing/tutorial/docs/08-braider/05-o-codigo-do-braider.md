---
sidebar_position: 5
title: O código do Braider
---

# O código do Braider

As páginas anteriores construíram as três peças do `Braider`: o passo (a), que abre os becos
(`_remove_dead_ends`), o passo (b), que garante 2 ciclos (`_add_loops`), e a abertura conferida
pela regra do 3x3 (`_open_without_3x3`). Falta o método público que as junta, e que é o único que
o resto do programa chama. O arquivo é `mazegen/services/braider.py`. Como o `Carver` e o
`Solver`, o `Braider` é um **service**: só executa uma operação e não guarda nada entre uma chamada
e outra.

## `braid`

```python
    def braid(self, maze: Maze, rng: random.Random) -> None:
        """Remove the dead ends, then add loops up to MIN_LOOPS.

        Args:
            maze: Carved perfect maze, changed in place.
            rng: The single random source of the generator.
        """
        self._remove_dead_ends(maze, rng)
        self._add_loops(maze, rng)
```

*Braid* quer dizer "trançar".

- Recebe o labirinto **perfeito** que o `Carver` acabou de cavar e o altera no lugar.
- Recebe o **mesmo** `rng` que o `Carver` usou ([parte 6](../06-carver/04-a-seed.md)). Os sorteios
  do braiding continuam a sequência da escavação, e a semente fixa o tabuleiro inteiro.
- A ordem importa: o passo (a) primeiro, porque costuma criar ciclos de sobra; o passo (b) só
  completa o que faltar.

`braid` não tem sublinhado no começo do nome; os outros três métodos têm. É a convenção do Python
para separar o que é para uso de fora da classe (`braid`) do que é interno.

## O `Braider` não levanta exceção

Em casos raros o braiding não consegue cumprir as regras. Por exemplo, um beco em que todo lado
abriria um 3x3, ou uma grade fina em que todas as paredes candidatas a ciclo são recusadas. O
`Braider` não trata esses casos e nunca **levanta** (lança) uma exceção, o jeito do Python de
interromper o método e avisar quem o chamou de que algo deu errado (em inglês, *raise*). Ele faz
o melhor que pode e devolve o labirinto como ficou.

Quem confere é o `MazeGenerator`, a classe que coordena a geração
([parte 9](../09-gerador/03-generate.md)). Depois de `braid`, ele testa se há no máximo
`MAX_DEAD_ENDS` becos reais e pelo menos `MIN_LOOPS` ciclos. Se não há, joga a grade fora e começa
outra, desde a escavação, com o mesmo `rng`. A nova tentativa continua a sequência de sorteios de
onde a anterior parou, então sai um labirinto diferente, e não a mesma grade ruim de novo. Cada
classe fica com uma responsabilidade: o `Braider` abre paredes, e o gerador decide se o resultado
serve. A docstring da classe (o texto entre `"""` logo abaixo de `class Braider:`) registra esse
acordo para quem ler o código.

## O arquivo completo

```python title="mazegen/services/braider.py"
"""Braiding that turns a perfect maze into a Pac-Man board."""

import random

from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction

MIN_LOOPS = 2
MAX_DEAD_ENDS = 2


class Braider:
    """Open walls of a perfect maze without ever opening a 3x3 area.

    The braider never raises: the MazeGenerator checks MIN_LOOPS and
    MAX_DEAD_ENDS on the result and rebuilds the grid when needed.
    """

    def braid(self, maze: Maze, rng: random.Random) -> None:
        """Remove the dead ends, then add loops up to MIN_LOOPS.

        Args:
            maze: Carved perfect maze, changed in place.
            rng: The single random source of the generator.
        """
        self._remove_dead_ends(maze, rng)
        self._add_loops(maze, rng)

    def _remove_dead_ends(self, maze: Maze, rng: random.Random) -> None:
        """Open one wall of every real dead end, in random order.

        Args:
            maze: Maze changed in place.
            rng: The single random source of the generator.
        """
        dead_ends = maze.dead_ends()
        rng.shuffle(dead_ends)
        for cell in dead_ends:
            if len(maze.passages(cell)) != 1:
                # An earlier opening already linked this cell.
                continue
            sides = maze.closed_sides(cell)
            rng.shuffle(sides)
            for side in sides:
                if self._open_without_3x3(maze, cell, side):
                    break

    def _add_loops(self, maze: Maze, rng: random.Random) -> None:
        """Open random inner walls until the maze has MIN_LOOPS cycles.

        Args:
            maze: Maze changed in place.
            rng: The single random source of the generator.
        """
        walls: list[tuple[Cell, Direction]] = [
            (cell, side)
            for cell in maze.cells()
            for side in maze.closed_sides(cell)
            # East and South list every inner wall exactly once.
            if side in (Direction.EAST, Direction.SOUTH)
        ]
        rng.shuffle(walls)
        for cell, side in walls:
            if maze.loop_count() >= MIN_LOOPS:
                return
            self._open_without_3x3(maze, cell, side)

    @staticmethod
    def _open_without_3x3(maze: Maze, cell: Cell, side: Direction) -> bool:
        """Open a wall and undo it when a 3x3 window becomes fully open.

        Args:
            maze: Maze changed in place.
            cell: Cell on one side of the wall.
            side: Side of the wall.

        Returns:
            True when the wall stayed open.
        """
        maze.open_wall(cell, side)
        if maze.has_open_3x3():
            maze.close_wall(cell, side)
            return False
        return True
```

## Experimente

O código cava um labirinto 20x15, conta os becos reais e os ciclos, trança e conta de novo,
conferindo também se apareceu algum 3x3 aberto. Na raiz do projeto:

```bash
.venv/bin/python - <<'EOF'
import random

from mazegen.entities.maze import Maze
from mazegen.services.braider import Braider
from mazegen.services.carver import Carver
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(20, 15, Pattern42.for_size(20, 15))
rng = random.Random(42)
Carver().carve(maze, Cell(0, 0), rng)
print(len(maze.dead_ends()), maze.loop_count())
Braider().braid(maze, rng)
print(len(maze.dead_ends()), maze.loop_count(), maze.has_open_3x3())
EOF
```

```text
32 0
0 32 False
```

- O mesmo `rng` passa do `Carver` para o `Braider`, como o gerador fará.
- `dead_ends()` lista os becos reais ([parte 5](../05-maze/05-passagens-e-becos.md)),
  `loop_count()` conta os ciclos ([parte 5](../05-maze/06-contar-ciclos.md)) e `has_open_3x3()`
  diz se algum bloco 3x3 ficou todo aberto ([parte 5](../05-maze/07-areas-abertas-3x3.md)).

Antes: 32 becos reais e nenhum ciclo. Depois: nenhum beco real, 32 ciclos e nenhum 3x3 aberto. É
o tabuleiro sem becos que o enunciado premia como bônus
([parte 16](../16-bonus/01-o-tabuleiro-sem-becos.md)).
