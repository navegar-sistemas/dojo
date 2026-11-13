---
sidebar_position: 1
title: O problema
---

# O problema

Um jogo online recebe eventos o tempo todo: um jogador corre, outro come, outro nada. Os eventos
não acabam, e guardar todos numa lista antes de processá-los encheria a memória. O jeito é
produzir e processar **um de cada vez**, conforme forem pedidos. É o que fazem os
**generators** ("geradores").

## O que o enunciado pede

Um arquivo `ex5/ft_data_stream.py`, que pode usar `next()`, `range()`, `len()`, `print()`,
`import typing`, `typing.Generator`, `import random` e qualquer função de `random`.

1. Uma função geradora **sem fim**, `gen_event()`, que sorteia um nome de uma lista de jogadores e
   uma ação de uma lista de ações. Cada `next()` sobre ela devolve um evento novo, a tupla
   `(name, action)`.
2. Um laço de mil voltas que pega e mostra 1000 eventos de `gen_event()`.
3. Uma lista com mais dez eventos de `gen_event()`.
4. Uma segunda função geradora, `consume_event`, que recebe essa lista e, enquanto ela não estiver
   vazia, sorteia um elemento, o tira da lista e o entrega. Ela é usada direto num laço
   `for event in consume_event(events):`.

## A saída esperada

Os eventos são sorteados, e cada execução imprime outros. A forma, com as 1000 linhas de evento
cortadas no meio:

```text
=== Game Data Stream Processor ===
Event 0: Player bob did action run
Event 1: Player alice did action eat
Event 2: Player bob did action sleep
[...]
Event 997: Player bob did action grab
Event 998: Player bob did action move
Event 999: Player alice did action move
Built list of 10 events: [('charlie', 'move'), ('dylan', 'grab'), ('alice', 'use'), ('alice', 'use'), ('charlie', 'swim'), ('bob', 'run'), ('charlie', 'move'), ('dylan', 'climb'), ('alice', 'use'), ('bob', 'release')]
Got event from list: ('charlie', 'swim')
Remains in list: [('charlie', 'move'), ('dylan', 'grab'), ('alice', 'use'), ('alice', 'use'), ('bob', 'run'), ('charlie', 'move'), ('dylan', 'climb'), ('alice', 'use'), ('bob', 'release')]
Got event from list: ('alice', 'use')
Remains in list: [('charlie', 'move'), ('dylan', 'grab'), ('alice', 'use'), ('bob', 'run'), ('charlie', 'move'), ('dylan', 'climb'), ('alice', 'use'), ('bob', 'release')]
```

E assim por diante, até `Remains in list: []`. Os eventos são numerados a partir de 0. Depois de
cada evento tirado da lista, o programa mostra o que **restou** nela: a lista encolhe de um em um,
e o elemento que sai é sempre o que acabou de ser entregue.

O exemplo do enunciado mostra os jogadores `alice`, `bob`, `charlie` e `dylan`, e as ações
`run`, `eat`, `sleep`, `grab`, `move`, `climb`, `swim`, `use` e `release`. O exercício usa essas
listas.
