---
sidebar_position: 4
title: 'Vizinhos: a borda e o "42"'
---

# Vizinhos: a borda e o "42"

Para cavar, o algoritmo precisa saber quem está do outro lado de cada parede de uma célula: há
uma célula ali para onde ir, ou é a borda da grade, ou é o "42"? E, para andar pelo labirinto
pronto, precisa saber se uma parede está aberta. Esta página escreve os dois métodos que
respondem, `neighbour` e `is_open`.

Os dois entram na classe `Maze`, depois dos métodos da
[página anterior](./02-consultar-a-grade.md). Eles recebem um lado da célula, uma `Direction`
([parte 4](../04-value-objects/02-direction-bits.md)), então o topo do arquivo ganha mais um
import, junto dos outros do projeto:

```python
from mazegen.value_objects.direction import Direction
```

## `neighbour`: quem está do outro lado

```python
    def neighbour(self, cell: Cell, side: Direction) -> Cell | None:
        other = cell.step(side)
        if other not in self or other in self.pattern:
            return None
        return other
```

Recebe uma célula e um lado (`Direction`: Norte, Leste, Sul ou Oeste) e devolve a célula do
outro lado daquela parede, **se ela faz parte do labirinto**.

- `cell.step(side)` dá a posição vizinha, sem conferir nada
  ([parte 4](../04-value-objects/04-cell.md)).
- `other not in self` usa o `__contains__` da [página anterior](./02-consultar-a-grade.md): a
  posição caiu **fora da grade**?
- `other in self.pattern` pergunta ao `Pattern42`: a posição é uma **célula do "42"**?

Em qualquer dos dois casos, a resposta é `None`, o valor do Python para "nada".

O tipo de retorno `Cell | None` quer dizer "uma `Cell` ou `None`". O `|` entre tipos é a forma do
Python 3.10 de escrever "um ou outro".

A figura mostra os vizinhos da célula `0,1` numa grade 9x7: ela fica na borda esquerda,
encostada no "4". A célula tracejada à esquerda da grade é a posição `-1,1`, que o `step`
calcula mas que não existe na grade:

![Vizinhos de 0,1 numa grade 9 por 7: Norte e Sul existem, Leste é do 42 e Oeste está fora](/img/maze/vizinhos-9x7.svg)

## Por que a borda e o "42" dão a mesma resposta

Para os algoritmos, uma célula do "42" e uma posição fora da grade são a mesma coisa: um lugar
onde não se entra. Com `neighbour` devolvendo `None` nos dois casos, basta uma condição. O
`Carver`, que cava o labirinto ([parte 6](../06-carver/02-recursive-backtracker.md)), escolhe
para onde cavar assim:

```python
                nxt = maze.neighbour(current, side)
                if nxt is not None and nxt not in visited:
                    options.append(side)
```

No trecho, `current` é a célula onde o algoritmo está, `side` é o lado que ele está testando,
`visited` é o conjunto das células por onde ele já passou e `options` é a lista dos lados para
onde ele ainda pode cavar. `nxt` é a vizinha (abreviação de *next*, "próxima"; o nome `next`
inteiro já é uma função do Python).

A condição diz: "se existe vizinha, e ela ainda não foi visitada, esse lado é uma opção". O
`is not None` é o jeito de perguntar "não é `None`?".

O `Solver` e o `Braider` (partes [7](../07-solver/01-busca-em-largura.md) e
[8](../08-braider/01-becos-sem-saida.md)) usam `passages` e `closed_sides`
([Passagens e becos](./05-passagens-e-becos.md)), que chamam `neighbour` por dentro. Nenhum dos três
algoritmos conhece o desenho do "42" nem confere limites da grade: se o "42" mudasse de forma,
só o `Pattern42` mudaria.

O `Cell | None` também protege: o mypy recusa usar o resultado como `Cell` (por exemplo,
`nxt.x`) antes de o código descartar o `None` com um `if`. Esquecer a borda vira erro de tipo,
não um bug escondido.

## `is_open`: dá para passar?

```python
    def is_open(self, cell: Cell, side: Direction) -> bool:
        return (self.neighbour(cell, side) is not None
                and not self.walls(cell) & side)
```

Um lado é **passagem** quando há uma vizinha **e** a parede daquele lado está aberta.

`self.walls(cell) & side` isola o bit daquele lado nas paredes da célula (o `&` bit a bit,
explicado na [parte 4](../04-value-objects/02-direction-bits.md)): dá o valor do lado, diferente
de zero, se a parede está fechada, e `0` se está aberta. O `not` inverte: `not 0` é `True`
("aberta"), `not 2` é `False`.

A primeira condição parece sobrar, porque a borda e o "42" nunca são abertos. Mas, com ela, a
resposta não depende de o bit estar certo: uma parede da borda **nunca** é passagem, seja qual
for o bit guardado.

### Precedência

`not self.walls(cell) & side` é lido como `not (self.walls(cell) & side)`. No Python, o `&` é
calculado antes do `not`, então os parênteses não são necessários.

## Experimente

Com os dois métodos e o import no `maze.py`, na raiz do projeto:

```bash
.venv/bin/python - <<'EOF'
from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(9, 7, Pattern42.for_size(9, 7))
for side in Direction:
    print(side.letter, maze.neighbour(Cell(0, 1), side))
print(maze.is_open(Cell(0, 1), Direction.SOUTH),
      maze.is_open(Cell(0, 1), Direction.WEST))
EOF
```

```text
N Cell(x=0, y=0)
E None
S Cell(x=0, y=2)
W None
False False
```

- Norte e Sul existem. O Leste, `1,1`, é o canto de cima do "4" numa grade 9x7; o Oeste cai fora
  da grade. Os dois dão `None`.
- Numa grade recém-criada todas as paredes estão fechadas, então nenhum lado é passagem: o Sul
  tem vizinha, mas a parede está fechada; o Oeste nem tem vizinha. A
  [próxima página](./04-abrir-e-fechar.md) abre paredes, e o Sul passa a responder `True`.
