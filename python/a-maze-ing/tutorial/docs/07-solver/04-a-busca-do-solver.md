---
sidebar_position: 3
title: A busca do Solver
---

# A busca do Solver

As páginas anteriores definiram o que o `Solver` faz: uma busca em largura a partir da entrada,
com uma fila, anotando o pai de cada célula num dicionário, e depois a leitura do caminho de trás
para a frente. Esta página começa a escrever a classe, em `mazegen/services/solver.py`: os
imports, a assinatura e a busca. A [próxima página](./03-o-codigo-do-solver.md) escreve a
leitura do caminho e mostra o arquivo completo. Como o `Carver`, o `Solver` é um **service**:
só executa uma operação e não guarda nada entre uma chamada e outra.

## Os imports

```python
from collections import deque

from mazegen.entities.maze import Maze
from mazegen.errors import MazeError
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
```

- `deque` é a fila ([página 1](./01-busca-em-largura.md)).
- `MazeError` é a exceção do `mazegen` ([parte 4](../04-value-objects/01-maze-error.md)). Ela
  aparece para um caso que nunca deveria acontecer, explicado na
  [próxima página](./03-o-codigo-do-solver.md).
- `Maze`, `Cell` e `Direction` são a grade de paredes, a posição de uma célula e os quatro lados.

## A assinatura

Os trechos desta página ficam dentro da classe `Solver`, no arquivo
`mazegen/services/solver.py`. Não grave o arquivo ainda: a
[próxima página](./03-o-codigo-do-solver.md) mostra o arquivo completo, pronto para copiar.

```python
class Solver:
    def shortest_path(self, maze: Maze, start: Cell, goal: Cell) -> str:
```

Recebe o labirinto já escavado, a entrada (`start`) e a saída (`goal`, "objetivo"). Devolve uma
`str` com uma letra por passo: um caminho que passa por `n` células tem `n − 1` passos, então
`n − 1` letras. Entrada e saída nunca são a mesma célula (o `MazeGenerator` recusa, na
[parte 9](../09-gerador/02-validar-os-parametros.md)), então a string nunca sai vazia.

## A busca

```python
        parents: dict[Cell, tuple[Cell, Direction] | None] = {start: None}
        queue: deque[Cell] = deque([start])
        while queue:
            current = queue.popleft()
            if current == goal:
                break
            for side in maze.passages(current):
                nxt = current.step(side)
                if nxt not in parents:
                    parents[nxt] = (current, side)
                    queue.append(nxt)
```

- A anotação de `parents` diz o que o dicionário guarda: a chave é uma `Cell`; o valor é uma
  tupla `(Cell, Direction)` **ou** `None`. O `|` numa anotação de tipo quer dizer "ou". O
  dicionário começa com a entrada, que não tem pai.
- `deque([start])` cria a fila já com a entrada dentro.
- `while queue:` repete enquanto a fila não estiver vazia.
- `queue.popleft()` tira a célula da frente.
- `if current == goal: break`: quando a saída sai da fila, o caminho até ela já está anotado, e o
  resto do labirinto não interessa. O `break` encerra o `while`.
- `maze.passages(current)` devolve só os lados **abertos** da célula, na ordem N, E, S, W
  ([parte 5](../05-maze/05-passagens-e-becos.md)). Uma passagem nunca dá para fora da grade nem
  para o "42", porque essas paredes nunca abrem; por isso o `Solver` não precisa conferir limites.
- `current.step(side)` é a célula vizinha daquele lado.
- `nxt not in parents` testa se a vizinha ainda não foi descoberta. Se não foi, ela ganha o pai e
  entra no fim da fila. A primeira descoberta vence.
