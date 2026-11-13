---
sidebar_position: 4
title: Pilha em vez de recursão
---

# Pilha em vez de recursão

O backtracker recursivo da [página anterior](./06-a-versao-recursiva.md) guarda a pilha do
algoritmo na pilha de chamadas do Python, e essa pilha tem limite. Esta página mostra onde a
versão recursiva quebra, como a pilha da [página 2](./02-recursive-backtracker.md), guardada
numa lista comum, substitui a pilha de chamadas, e por que não basta aumentar o limite.

## O limite de recursão do Python

O Python não deixa a pilha de chamadas crescer sem limite. Por padrão, ele recusa passar de cerca
de 1000 chamadas em andamento ao mesmo tempo:

```python
import sys

print(sys.getrecursionlimit())
```

```text
1000
```

Passando do limite, o Python interrompe o programa com o erro `RecursionError`. O limite existe
porque cada chamada em andamento ocupa memória: sem ele, uma função que chama a si mesma para
sempre derrubaria o próprio interpretador.

No backtracker, o número de chamadas em andamento é o tamanho da pilha, e ele cresce com o
labirinto. O enunciado não fixa um tamanho máximo; este projeto aceita até 100x100, ou seja,
10 000 células (escolha explicada na [parte 1](../01-o-problema/03-o-arquivo-de-configuracao.md)).
Numa escavação 100x100 com a semente 42, a pilha chega a 3006 células; no pior caso, chegaria
perto das 9982 células livres.

## Experimente

O script abaixo tem a função `visit` da página anterior e os imports das peças das partes 4 e 5.
Ele cava uma grade 20x15, que funciona, e depois tenta uma 100x100. Na raiz do projeto, cole tudo
no terminal (o `<<'EOF'` entrega ao Python as linhas até o `EOF` final, como explicado em
[como rodar os exemplos](../00-introducao/03-pre-requisitos.md)):

```bash
.venv/bin/python - <<'EOF'
import random

from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
from mazegen.value_objects.pattern42 import Pattern42


def visit(maze, current, visited, rng):
    visited.add(current)
    while True:
        options = []
        for side in Direction:
            nxt = maze.neighbour(current, side)
            if nxt is not None and nxt not in visited:
                options.append(side)
        if not options:
            return
        side = rng.choice(options)
        maze.open_wall(current, side)
        visit(maze, current.step(side), visited, rng)


small = Maze(20, 15, Pattern42.for_size(20, 15))
seen = set()
visit(small, Cell(0, 0), seen, random.Random(7))
print(small.loop_count(), len(seen))
big = Maze(100, 100, Pattern42.for_size(100, 100))
try:
    visit(big, Cell(0, 0), set(), random.Random(42))
except RecursionError as error:
    print("RecursionError:", error)
EOF
```

```text
0 282
RecursionError: maximum recursion depth exceeded
```

- A grade 20x15 sai inteira: `loop_count()` (que conta os ciclos,
  [parte 5](../05-maze/06-contar-ciclos.md)) dá 0, e o conjunto `seen`, que a `visit` vai
  preenchendo, termina com 282 células: todas as células livres (as 300 da grade menos as 18 do
  "42") foram visitadas.
- A 100x100 passa do limite. O `try`/`except RecursionError` captura o erro só para imprimir a
  mensagem numa linha; sem ele, o Python mostraria a listagem inteira do erro.

## A pilha vira uma lista

A solução é guardar a pilha numa `list` comum, que só é limitada pela memória do computador. A
tradução é direta:

| Versão recursiva | Versão com lista |
|---|---|
| chamar `visit(maze, current.step(side), visited, rng)` | `stack.append(current.step(side))` (no código final, em duas linhas: `nxt = current.step(side)` e `stack.append(nxt)`) |
| `return` | `stack.pop()` |
| a variável `current` de cada chamada | `current = stack[-1]` (o topo) |
| termina quando a primeira chamada retorna | termina quando `stack` fica vazia |

O algoritmo é o mesmo, com os mesmos sorteios na mesma ordem: com a mesma semente, as duas
versões escavam o mesmo labirinto. Só muda onde a pilha mora.

## E aumentar o limite?

`sys.setrecursionlimit(20000)` faria a versão recursiva passar. Ficou de fora por dois motivos:

- o limite vale para o **programa inteiro**, não só para o `mazegen`. Como o `mazegen` é uma
  biblioteca que outros projetos importam, mudar o limite mudaria o comportamento do programa de
  quem a importa;
- o limite protege o interpretador, e o valor seguro depende da versão do Python e do sistema
  operacional. A lista não depende de nada disso.
