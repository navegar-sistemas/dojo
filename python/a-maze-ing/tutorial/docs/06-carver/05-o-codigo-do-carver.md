---
sidebar_position: 7
title: O código do Carver
---

# O código do Carver

Com a pilha `stack` e o conjunto `visited` prontos, ambos começando só com a entrada
([página anterior](./07-a-assinatura-do-carver.md)), falta o laço que derruba as paredes:
olhar o topo da pilha, recuar quando não há vizinha nova e avançar quando há. Esta página
escreve esse laço e mostra o arquivo `mazegen/services/carver.py` inteiro.

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

- `while stack:` repete enquanto a pilha não estiver vazia. Uma lista vazia vale como falso num
  `while` ou num `if`.
- `stack[-1]` **lê** o topo sem tirá-lo: a célula só sai da pilha quando não tiver mais vizinha
  nova.
- `maze.neighbour(current, side)` devolve a vizinha daquele lado, ou `None` para a borda e para o
  "42". Sobra testar se a vizinha ainda não foi visitada.
- `options` guarda **lados** (`Direction`), não células: o lado é o que `open_wall` precisa
  para saber qual parede derrubar.

## Recuar

```python
            if not options:
                stack.pop()
                continue
```

Sem vizinha nova, a célula atual sai da pilha. O `continue` pula o resto do laço e volta ao
`while`, que olha o novo topo: a célula de onde se tinha vindo.

## Avançar

```python
            side = rng.choice(options)
            maze.open_wall(current, side)
            nxt = current.step(side)
            visited.add(nxt)
            stack.append(nxt)
```

1. sorteia um dos lados livres;
2. derruba a parede. `open_wall` muda as duas células que dividem a parede, então as duas
   continuam concordando sobre ela ([parte 5](../05-maze/04-abrir-e-fechar.md));
3. calcula a célula nova com `step`, que soma ao `x,y` o deslocamento daquele lado;
4. marca a célula nova como visitada **ao empilhar**, não ao desempilhar. Se a marca só viesse
   quando a célula sai da pilha, ela continuaria "não visitada" durante todo o tempo em que está
   lá dentro. Uma célula empilhada depois, vizinha dela, poderia sorteá-la de novo: ela entraria
   uma segunda vez na pilha e ganharia uma segunda parede derrubada, ligando duas células que já
   estavam ligadas, o que forma um ciclo. Marcando ao empilhar, nenhuma célula entra duas vezes;
5. empilha: a célula nova vira a atual na próxima volta.

Cada célula livre entra uma vez e sai uma vez da pilha. O trabalho é proporcional ao número de
células: o dobro de células, o dobro de tempo. Uma grade 100x100 é escavada num instante.

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

A docstring do método (o texto entre `"""` logo abaixo do `def`) registra por que a pilha é uma
lista, para quem ler o código sem este tutorial ao lado: o Python para a recursão em cerca de 1000
chamadas (*CPython* é o nome do interpretador Python padrão), e uma grade 100x100 precisaria de
até 10 000. O 10 000 é o total de células da grade, um teto redondo; descontadas as 18 do "42",
são 9982 células livres, e a pilha nunca passa disso
([página 4](./03-pilha-em-vez-de-recursao.md)).

## Experimente

Com o arquivo pronto, confira o que a [página 5](./04-a-seed.md) prometeu: a mesma semente dá o
mesmo labirinto, e o resultado é uma árvore. Na raiz do projeto:

```bash
.venv/bin/python - <<'EOF'
import random

from mazegen.entities.maze import Maze
from mazegen.services.carver import Carver
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42


def carved(seed):
    maze = Maze(20, 15, Pattern42.for_size(20, 15))
    Carver().carve(maze, Cell(0, 0), random.Random(seed))
    return maze


print(carved(7).rows() == carved(7).rows())
print(carved(7).rows() == carved(8).rows())
maze = carved(7)
cells = list(maze.cells())
passages = sum(len(maze.passages(cell)) for cell in cells) // 2
print(maze.loop_count(), len(cells), passages)
EOF
```

```text
True
False
0 282 281
```

- `carved(seed)` cria um `Maze` 20x15 todo fechado, cava com a semente pedida e devolve o
  labirinto. `Pattern42.for_size(20, 15)` calcula as células do "42" para esse tamanho
  ([parte 4](../04-value-objects/05-pattern42-posicao.md)).
- `maze.rows()` devolve a grade de paredes como listas de números
  ([parte 5](../05-maze/08-a-copia-da-grade.md)); comparar duas com `==` diz se as paredes são
  idênticas.
- `maze.loop_count()` conta os ciclos ([parte 5](../05-maze/06-contar-ciclos.md)), e
  `maze.cells()` percorre as células livres.
- `maze.passages(cell)` lista os lados abertos de uma célula
  ([parte 5](../05-maze/05-passagens-e-becos.md)). Somando os de todas as células, cada passagem
  é contada duas vezes (uma por célula de cada lado), daí o `// 2`.

A mesma semente dá a mesma grade (`True`), outra semente dá outra (`False`), e o resultado é uma
árvore que cobre tudo: 282 células livres (as 300 da grade menos as 18 do "42") ligadas por
281 passagens, sem nenhum ciclo. Não sobra célula de fora porque
cada passagem que o `Carver` abre leva a uma célula ainda não visitada
([o backtracker](./02-recursive-backtracker.md)): 281 passagens trazem 281 células novas, que,
com a entrada, são as 282. Ligadas e com uma passagem a menos que o número de células, elas
formam uma árvore, e o `0` do `loop_count()` confirma.
