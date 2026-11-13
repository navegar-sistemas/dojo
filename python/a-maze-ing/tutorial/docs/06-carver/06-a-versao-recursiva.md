---
sidebar_position: 3
title: A versão recursiva
---

# A versão recursiva

O nome do algoritmo diz *recursive*, "recursivo": o jeito mais curto de escrever o backtracker
da [página anterior](./02-recursive-backtracker.md) é com uma função que chama a si mesma. Só
que essa versão quebra em labirintos grandes. Esta página explica o que é recursão e escreve o
backtracker recursivo; a [próxima](./03-pilha-em-vez-de-recursao.md) mostra onde ele quebra e
como o `Carver` evita o problema.

## O que é recursão

Uma função **recursiva** é uma função que chama a si mesma. Um exemplo pequeno:

```python
def descer(n):
    print("entra", n)
    if n > 0:
        descer(n - 1)
    print("sai", n)


descer(2)
```

```text
entra 2
entra 1
entra 0
sai 0
sai 1
sai 2
```

`descer(2)` imprime "entra 2" e chama `descer(1)`. Essa chamada precisa terminar antes de
`descer(2)` imprimir "sai 2". Enquanto isso, o Python precisa lembrar onde cada chamada parou. Ele
guarda as chamadas em andamento numa pilha própria, a **pilha de chamadas**: cada chamada nova
entra no topo, e cada `return` (ou o fim da função) a tira de lá.

![Seis estados da pilha de chamadas de descer(2): as chamadas entram até descer(0) e saem na ordem inversa](/img/carver/pilha-de-chamadas.svg)

Como na pilha da página anterior: a caixa laranja é a chamada em andamento (o topo), as azuis são
as chamadas que esperam por ela e a caixa tracejada é a chamada que acabou de terminar.

## A versão recursiva do backtracker

O backtracker se escreve muito curto com recursão. Cada célula nova vira uma chamada de `visit`:

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

- `visited` é um `set` (conjunto) com as células já visitadas; `visited.add(current)` marca a
  atual.
- `while True:` repete o bloco para sempre; só o `return` lá dentro encerra a chamada.
- O `for side in Direction` percorre os quatro lados, Norte, Leste, Sul e Oeste (`Direction` é a
  classe dos lados, da [parte 4](../04-value-objects/02-direction-bits.md)). `options` fica com
  os lados cujo vizinho existe e ainda não foi visitado. `maze.neighbour(current, side)` devolve a
  célula vizinha daquele lado, ou `None` quando o lado dá para fora da grade ou para o "42"
  ([parte 5](../05-maze/03-vizinhos.md)).
- Sem opção, `return`: a chamada termina, e quem a chamou continua de onde parou. É o **recuo**.
- `rng.choice(options)` sorteia um lado da lista (o `rng` é o sorteador, explicado na
  [página 5](./04-a-seed.md)), e `maze.open_wall` derruba a parede daquele lado.
- `current.step(side)` é a célula vizinha naquele lado ([parte 4](../04-value-objects/04-cell.md)).
  Chamar `visit` com ela é o **avanço**.

O `while True` é o que faz a célula voltar a procurar depois de um avanço. A chamada da vizinha
cava tudo o que consegue a partir dela e, quando termina, devolve o controle para a linha seguinte,
que é o fim do bloco do `while`. O laço então recomeça: a célula atual monta de novo a lista de
vizinhas não visitadas (algumas podem ter sido visitadas pela chamada que acabou) e, se ainda
houver alguma, avança por ela. Só quando a lista sai vazia a chamada retorna. Sem o laço, cada
célula abriria um único caminho e a escavação pararia no primeiro beco.

Aqui a pilha do backtracker existe, mas escondida: é a pilha de chamadas do Python. Cada `visit`
em andamento é uma célula na pilha. Essa pilha de chamadas tem um limite, e a
[próxima página](./03-pilha-em-vez-de-recursao.md) mostra o que acontece quando o labirinto é
grande.
