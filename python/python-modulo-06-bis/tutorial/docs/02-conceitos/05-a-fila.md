---
sidebar_position: 5
title: A fila
---

# A fila

Cada processador do projeto guarda os itens que recebe e os devolve **um de cada vez, do mais
antigo para o mais novo**, como uma fila de banco: quem chegou primeiro sai primeiro. Essa
estrutura se chama **fila** (em inglês, *queue*, ou *FIFO*, de *first in, first out*: "primeiro
a entrar, primeiro a sair").

Junto de cada item, o processador guarda o **rank**: o número de ordem em que o item chegou. O
primeiro item que o processador recebe na vida tem rank 0, o segundo rank 1, e assim por diante.
O rank não volta para trás quando um item sai: ele conta todos os itens que já passaram.

## Uma lista como fila

Uma lista do Python faz o papel de fila com dois métodos:

- `append(item)` acrescenta o item no **fim** da lista;
- `pop(0)` tira o item da posição 0, o **começo** da lista, e o devolve. Os outros itens andam
  uma posição para a frente.

Crie `experimentos/fila.py`. Cada item é uma tupla `(rank, texto)`:

```python title="experimentos/fila.py"
queue: list[tuple[int, str]] = []
rank = 0
for value in ["10", "20", "30"]:
    queue.append((rank, value))
    rank += 1
print(queue)
print(queue.pop(0))
print(queue)
queue.append((rank, "40"))
rank += 1
print(queue)
print(queue.pop(0))
print(queue.pop(0))
print(queue.pop(0))
try:
    queue.pop(0)
except IndexError as error:
    print(f"IndexError: {error}")
```

## O tipo de uma lista que começa vazia

Por `[]`, o mypy não sabe o tipo dos itens. Ele espera o primeiro uso da variável:

- se o primeiro uso é um `append`, no mesmo trecho de código (a mesma função, ou o corpo do
  arquivo), o tipo vem do item acrescentado. Aqui, sem a anotação, `queue` também seria
  `list[tuple[int, str]]`, por causa do `queue.append((rank, value))`;
- se o primeiro uso é outro (como `len(queue)`), ou se o `append` fica em outro método, o mypy
  pede a anotação, com o erro `Need type annotation for "queue"`.

Neste experimento a anotação não é obrigatória, mas deixa o tipo escrito para quem lê.

```bash
python3 experimentos/fila.py
```

```text
[(0, '10'), (1, '20'), (2, '30')]
(0, '10')
[(1, '20'), (2, '30')]
[(1, '20'), (2, '30'), (3, '40')]
(1, '20')
(2, '30')
(3, '40')
IndexError: pop from empty list
```

## O que aconteceu

![Os quatro passos do experimento. 1: três append deixam na fila os itens de rank 0, 1 e 2, e o próximo rank é 3. 2: pop(0) tira do começo o item de rank 0, '10', e ficam os de rank 1 e 2. 3: append de '40' põe no fim um item de rank 3. 4: três pop(0) esvaziam a fila, e mais um pop(0) lança IndexError](/img/conceitos/a-fila.svg)

- os três primeiros itens entram com ranks 0, 1 e 2;
- o primeiro `pop(0)` devolve `(0, '10')`, o mais antigo;
- o item `"40"` entra com rank **3**, e não 2: o rank conta os itens que já passaram pela fila,
  e não as posições ocupadas agora;
- quando a fila está vazia, `pop(0)` lança `IndexError` ("tirar de uma lista vazia").

## No projeto

O método `output` do exercício 0 é exatamente o `pop(0)` da fila do processador: devolve a tupla
`(rank, texto)` mais antiga e a remove ([A classe base](../03-ex0/02-a-classe-base.md)). No
exercício 2, a saída em JSON mostra os ranks: `{"item_3": "42", ...}` quer dizer que o `"42"`
foi o quarto item (rank 3) que o processador de números recebeu, e os três primeiros já tinham
saído antes.
