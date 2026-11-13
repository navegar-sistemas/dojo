---
sidebar_position: 3
title: O gerador sem fim
---

# O gerador sem fim

O primeiro generator do exercício nunca termina: cada pedido sorteia um evento novo, com um
jogador e uma ação. O programa pede mil eventos a ele e depois mais dez, guardados numa lista.

## gen_event

```python
import random
import typing

PLAYERS = ["alice", "bob", "charlie", "dylan"]
ACTIONS = ["run", "eat", "sleep", "grab", "move", "climb", "swim", "use",
           "release"]

Event = tuple[str, str]


def gen_event() -> typing.Generator[Event, None, None]:
    """Yield random (player, action) events forever."""
    while True:
        yield (random.choice(PLAYERS), random.choice(ACTIONS))
```

- `random.choice(lista)` sorteia um elemento da lista;
- `while True` nunca termina, e o `yield` dentro dele entrega um evento novo a cada pedido. Um
  laço sem fim numa função comum nunca terminaria, e o programa ficaria preso nele; num
  generator, a função pausa a cada `yield`, e só roda quando alguém pede o próximo evento;
- `Event = tuple[str, str]` dá um nome ao tipo "tupla de dois textos". Esse nome, um **apelido de
  tipo** (*type alias*), deixa as anotações curtas: `typing.Generator[Event, None, None]` em vez
  de `typing.Generator[tuple[str, str], None, None]`.

## Mil eventos

```python
stream = gen_event()
for number in range(1000):
    name, action = next(stream)
    print(f"Event {number}: Player {name} did action {action}")
```

- `stream` ("fluxo") é o generator, criado uma vez;
- `range(1000)` produz os números de 0 a 999, um por volta, e é ele que numera os eventos a
  partir de 0, como no enunciado. Assim como um generator, o `range` não monta uma lista de mil
  números: calcula cada um quando o laço pede. Ele não é um generator: aceita `len()` e índice, e
  pode ser percorrido mais de uma vez;
- `next(stream)` pede um evento, e o desempacotamento separa a tupla em nome e ação.

Um `for event in stream:` direto sobre o generator sem fim nunca terminaria. O `range(1000)` é que
limita o laço, e o `next` pede exatamente um evento por volta.

## Mais dez, numa lista

```python
events: list[Event] = []
for _ in range(10):
    events.append(next(stream))
print(f"Built list of 10 events: {events}")
```

O mesmo `stream` continua entregando eventos: um generator não recomeça, retoma de onde parou e
continua sorteando eventos novos, que podem coincidir por acaso com algum anterior. A lista
guarda os dez de uma vez, porque a parte seguinte do exercício precisa deles todos para sortear
entre eles.
