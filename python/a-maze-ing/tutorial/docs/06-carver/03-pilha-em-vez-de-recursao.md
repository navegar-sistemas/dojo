---
sidebar_position: 3
title: Pilha em vez de recursão
---

# Pilha em vez de recursão

## A versão recursiva

O nome "recursive backtracker" vem da forma mais curta de escrever o algoritmo: uma função que
chama a si mesma para cada célula nova.

```python
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
```

Aqui a pilha existe, mas é escondida: é a **pilha de chamadas** do Python. Cada `visit` em
andamento ocupa um nível dela; o `return` é o recuo.

## O limite de recursão do CPython

O CPython recusa passar de cerca de 1000 chamadas aninhadas:

```python
import sys

print(sys.getrecursionlimit())
```

```text
1000
```

A profundidade da recursão é o tamanho da pilha do backtracker, e ela cresce com o labirinto. O
subject aceita até 100x100, ou seja, 10 000 células. Numa escavação 100x100 com seed 42, a pilha
chega a 3006 células; no pior caso, chegaria perto das 10 000.

## Experimente

Com a função `visit` acima num arquivo, mais os imports de `random`, `Maze`, `Cell`,
`Direction` e `Pattern42`, escave uma grade 100x100:

```python
maze = Maze(100, 100, Pattern42.for_size(100, 100))
visit(maze, Cell(0, 0), set(), random.Random(42))
```

A última linha da saída:

```text
RecursionError: maximum recursion depth exceeded
```

## A pilha vira uma lista

A solução é guardar a pilha numa `list` comum, que só é limitada pela memória. A tradução é
direta:

| Recursivo | Iterativo |
|---|---|
| chamar `visit(maze, nxt, ...)` | `stack.append(nxt)` |
| `return` | `stack.pop()` |
| a variável `current` da chamada | `current = stack[-1]` |
| a recursão acaba quando a primeira chamada retorna | o laço acaba quando `stack` fica vazia |

O algoritmo é o mesmo, com os mesmos sorteios na mesma ordem: para a mesma seed, as duas versões
escavam a mesma árvore. Só muda onde a pilha mora.

## E aumentar o limite?

`sys.setrecursionlimit(20000)` faria a versão recursiva passar. Ficou de fora por dois motivos:

- o limite é uma configuração **global** do interpretador. O `mazegen` é uma biblioteca, e
  mudaria o comportamento de qualquer programa que o importasse;
- o limite existe para proteger o interpretador; o valor seguro depende da versão do Python e da
  plataforma. A lista não depende de nada disso.
