---
sidebar_position: 5
title: O código do Carver
---

# O código do Carver

O `Carver` é um **service**: não guarda estado, recebe tudo por parâmetro e altera o `Maze` que
recebeu. Mora em `mazegen/services/carver.py`.

## Os imports

```python
import random

from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
```

Só a biblioteca padrão e as peças das partes 4 e 5. `random` aparece apenas na anotação de tipo
do parâmetro `rng`: o `Carver` não sorteia com o módulo, só com o objeto recebido.

## A assinatura

```python
    def carve(self, maze: Maze, start: Cell, rng: random.Random) -> None:
```

- `maze`: um `Maze` novo, com todas as paredes fechadas. O método o altera no lugar e não
  devolve nada.
- `start`: a célula de entrada. A escavação começa por ela, que nunca é célula do "42" (o
  construtor do `MazeGenerator` recusa).
- `rng`: o `random.Random` único do gerador.

## O estado inicial

```python
        visited: set[Cell] = {start}
        stack: list[Cell] = [start]
```

A entrada já começa visitada e na pilha. `Cell` é imutável e tem `__hash__` (é um
`dataclass(frozen=True)`), por isso pode entrar num `set`.

## O topo e as opções

```python
        while stack:
            current = stack[-1]
            options: list[Direction] = []
            for side in Direction:
                nxt = maze.neighbour(current, side)
                if nxt is not None and nxt not in visited:
                    options.append(side)
```

- `stack[-1]` **lê** o topo sem tirá-lo: a célula só sai da pilha quando não tiver mais nada a
  oferecer.
- `maze.neighbour` já descarta a borda e o "42" (devolve `None`). Sobra testar se a vizinha é
  nova.
- `options` guarda **lados** (`Direction`), não células: o lado é o que `open_wall` precisa.

## Recuar

```python
            if not options:
                stack.pop()
                continue
```

Sem vizinha nova, a célula atual é descartada e o laço olha a de baixo na próxima volta.

## Avançar

```python
            side = rng.choice(options)
            maze.open_wall(current, side)
            nxt = current.step(side)
            visited.add(nxt)
            stack.append(nxt)
```

1. sorteia um dos lados livres;
2. abre a parede: `open_wall` mexe nos bits das duas células, então a vizinha fica coerente;
3. calcula a célula nova com `step`;
4. marca como visitada **ao empilhar**, não ao desempilhar. Assim nenhuma célula entra duas
   vezes na pilha, e nenhuma parede é aberta para uma célula que já faz parte da árvore.

Cada célula livre entra uma vez e sai uma vez da pilha: o trabalho cresce em linha reta com o
tamanho da grade, e 100x100 escava num instante.

## O arquivo completo

```python title="mazegen/services/carver.py"
"""Iterative recursive backtracker that carves the perfect maze."""

import random

from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction


class Carver:
    """Carve a spanning tree of the cells outside the "42"."""

    def carve(self, maze: Maze, start: Cell, rng: random.Random) -> None:
        """Run a randomised depth-first search with an explicit stack.

        CPython stops recursion at about 1000 frames; a 100x100 maze needs
        up to 10 000, so the stack lives in a list.

        Args:
            maze: Fresh maze with every wall closed.
            start: Entry cell, outside the "42".
            rng: The single random source of the generator.
        """
        visited: set[Cell] = {start}
        stack: list[Cell] = [start]
        while stack:
            current = stack[-1]
            options: list[Direction] = []
            for side in Direction:
                nxt = maze.neighbour(current, side)
                if nxt is not None and nxt not in visited:
                    options.append(side)
            if not options:
                stack.pop()
                continue
            side = rng.choice(options)
            maze.open_wall(current, side)
            nxt = current.step(side)
            visited.add(nxt)
            stack.append(nxt)
```

A docstring do método registra o motivo da pilha explícita, para quem ler o código sem este
tutorial ao lado.
