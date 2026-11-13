---
sidebar_position: 4
title: Consumir a lista
---

# Consumir a lista

`consume_event` recebe a lista de dez eventos e, enquanto ela tiver elementos, sorteia um, o tira
da lista e o entrega. Duas ferramentas novas: tirar um elemento de uma posição e sortear uma
posição.

```python title="experimentos/pop.py"
events = [("alice", "run"), ("bob", "eat"), ("dylan", "swim")]
removed = events.pop(1)
print(removed)
print(events)
print(events.pop(0), events)
```

```bash
python3 experimentos/pop.py
```

```text
('bob', 'eat')
[('alice', 'run'), ('dylan', 'swim')]
('alice', 'run') [('dylan', 'swim')]
```

- `events.pop(1)` tira o elemento do índice 1 **e o devolve**. A lista encolhe, e os elementos
  seguintes andam uma posição para a esquerda;
- `random.randrange(n)` sorteia um inteiro de 0 a `n - 1`, que são exatamente os índices de uma
  lista de tamanho `n`. Com `n = len(events)`, o sorteio sempre cai num índice que existe.

## consume_event

```python
def consume_event(events: list[Event]) -> typing.Generator[Event, None, None]:
    """Remove and yield random events from the list until it is empty."""
    while len(events) > 0:
        yield events.pop(random.randrange(len(events)))
```

A cada volta, a função sorteia um índice, tira o evento desse índice e o entrega com `yield`.
Quando a lista fica vazia, o `while` termina, a função chega ao fim, e o `for` que a usa acaba.

## A lista é a mesma

O programa usa o generator direto no `for`, e a cada evento mostra o que restou:

```python
for event in consume_event(events):
    print(f"Got event from list: {event}")
    print(f"Remains in list: {events}")
```

`Remains in list` imprime a variável `events` do `main`, e mesmo assim ela encolhe a cada volta.
Uma lista passada para uma função **não é copiada**: o parâmetro `events` de `consume_event` e a
variável `events` do `main` são dois nomes para a **mesma** lista. O `pop` dentro do generator
muda essa lista, e o `main` vê a mudança.

```python title="experimentos/mesma_lista.py"
def remove_first(items: list[str]) -> None:
    """Remove the first element of the list."""
    items.pop(0)


names = ["alice", "bob"]
remove_first(names)
print(names)
```

```bash
python3 experimentos/mesma_lista.py
```

```text
['bob']
```

![Cinco linhas mostram a lista de eventos do exemplo do enunciado encolhendo: a lista montada, com dez eventos, e o estado depois de cada um dos quatro primeiros eventos consumidos. Nas quatro primeiras linhas, o evento sorteado está destacado em laranja, com o yield ao lado; a linha seguinte não tem esse evento. O título diz que é a mesma lista events no main e em consume_event](/img/ex5/lista-encolhendo.svg)

A ordem dos acontecimentos em cada volta do `for`:

1. o `for` pede o próximo evento ao generator;
2. o generator sorteia um índice, faz o `pop` (a lista encolhe) e pausa no `yield`, entregando o
   evento;
3. o corpo do `for` imprime o evento e a lista, que **já** está sem ele.

É por isso que, no exemplo do enunciado, o evento de `Got event from list` nunca aparece na linha
`Remains in list` logo abaixo, a não ser que a lista tenha outro evento igual a ele.
