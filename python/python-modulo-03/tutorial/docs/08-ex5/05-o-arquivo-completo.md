---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

As duas funções geradoras ficam no topo do arquivo, e o `main` faz as três partes do exercício na
ordem: os mil eventos, a lista de dez e o consumo da lista.

```python title="ex5/ft_data_stream.py"
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


def consume_event(events: list[Event]) -> typing.Generator[Event, None, None]:
    """Remove and yield random events from the list until it is empty."""
    while len(events) > 0:
        yield events.pop(random.randrange(len(events)))


def main() -> None:
    """Show 1000 streamed events, then consume a list of ten."""
    print("=== Game Data Stream Processor ===")
    stream = gen_event()
    for number in range(1000):
        name, action = next(stream)
        print(f"Event {number}: Player {name} did action {action}")
    events: list[Event] = []
    for _ in range(10):
        events.append(next(stream))
    print(f"Built list of 10 events: {events}")
    for event in consume_event(events):
        print(f"Got event from list: {event}")
        print(f"Remains in list: {events}")


if __name__ == "__main__":
    main()
```

Como no [exercício 0](../03-ex0/05-o-arquivo-completo.md), o arquivo termina com uma única quebra
de linha depois da última linha, `    main()`, que o botão de copiar não leva.

A lista de ações passa de 79 caracteres numa linha só, e continua na linha de baixo, alinhada
depois do colchete.

O arquivo usa `next()`, `range()`, `len()`, `print()`, `typing.Generator`, `random.choice` e
`random.randrange`. A tupla e a lista vêm dos exercícios anteriores, e os métodos `append` e
`pop` da lista estão liberados pela regra geral desde que a lista foi apresentada, no
exercício 0.
