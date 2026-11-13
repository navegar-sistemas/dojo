---
sidebar_position: 6
title: A assinatura e o estado do Carver
---

# A assinatura e o estado do Carver

As páginas anteriores definiram o que o `Carver` faz: partindo de uma grade toda fechada, derrubar
paredes com o backtracker até formar um labirinto perfeito, guardando o caminho numa lista usada
como pilha e sorteando com o `random.Random` que recebe. Esta página começa a escrever a classe,
em `mazegen/services/carver.py`: os imports, a assinatura do método e o estado com que ele
começa. A [próxima página](./05-o-codigo-do-carver.md) escreve o laço e mostra o arquivo
completo.

O `Carver` é um **service**: uma classe que só executa uma operação e não guarda nada entre uma
chamada e outra ([parte 2](../02-arquitetura/04-papeis-das-classes.md)). Tudo de que precisa
chega por parâmetro, e o único efeito é mudar as paredes do `Maze` recebido.

## Os imports

```python
import random

from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
```

Só a biblioteca padrão e as peças das partes 4 e 5: `Maze` (a grade de paredes), `Cell` (a
posição `x,y` de uma célula) e `Direction` (os quatro lados). O módulo `random` aparece apenas na
anotação de tipo do parâmetro `rng`: o `Carver` não usa as funções soltas de `random`, só o objeto
que recebe.

## A assinatura

Os trechos desta página ficam dentro da classe `Carver`, no arquivo
`mazegen/services/carver.py`. Não grave o arquivo ainda: a
[próxima página](./05-o-codigo-do-carver.md) mostra o arquivo completo, pronto para copiar.

```python
class Carver:
    def carve(self, maze: Maze, start: Cell, rng: random.Random) -> None:
```

As anotações depois de `:` dizem o tipo de cada parâmetro, e `-> None` diz que o método não
devolve nada: ele altera o `maze` recebido, no lugar.

- `maze`: um `Maze` novo, com todas as paredes fechadas.
- `start`: a célula de entrada, onde a escavação começa. Ela nunca é célula do "42", porque o
  `MazeGenerator` recusa uma entrada assim antes de chegar aqui
  ([parte 9](../09-gerador/02-validar-os-parametros.md)).
- `rng`: o `random.Random` único do gerador ([página 5](./04-a-seed.md)).

## O estado inicial

```python
        visited: set[Cell] = {start}
        stack: list[Cell] = [start]
```

- `visited` é um conjunto (`set`) com as células já visitadas. `{start}` cria um conjunto com um
  só elemento. A anotação `set[Cell]` diz que ele guarda células.
- `stack` é a pilha, uma lista que começa só com a entrada.

A entrada já começa visitada e na pilha. Uma `Cell` pode entrar num `set` porque é imutável: ela
é um `@dataclass(frozen=True)`, que o Python sabe comparar e guardar em conjuntos
([parte 4](../04-value-objects/04-cell.md)).
