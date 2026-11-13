---
sidebar_position: 2
title: Nome e contadores
---

# Nome e contadores

As estatísticas do fluxo têm uma linha por processador:

```text
Numeric Processor: total 4 items processed, remaining 4 on processor
```

Para escrevê-la, `DataStream` precisa perguntar a cada processador três coisas: o nome, quantos
itens ele já recebeu no total e quantos ainda estão guardados. Como `DataStream` só conhece a
classe `DataProcessor`, as três respostas entram nela. O enunciado só fixa os três métodos de
`DataStream`; o atributo `name` e os métodos `total` e `remaining` são escolha do tutorial para
montar essa linha.

## O nome

Cada classe ganha um **atributo de classe** `name`, escrito no corpo da classe, fora dos
métodos:

```python
class DataProcessor(ABC):
    name = "Data Processor"

    def __init__(self) -> None:
        # (o corpo continua igual)


class NumericProcessor(DataProcessor):
    name = "Numeric Processor"

    def validate(self, data: Any) -> bool:
        # (o corpo continua igual)
```

`TextProcessor` e `LogProcessor` recebem `"Text Processor"` e `"Log Processor"` do mesmo jeito.
O comentário `# (o corpo continua igual)` só marca, nesta página, o código que não muda; no
arquivo, os métodos continuam inteiros. O `name` fica na primeira linha do corpo de cada classe.

Um atributo de classe funciona como um método: a filha que define o seu `name` **sobrescreve** o
da mãe. Assim, `processor.name` dá o nome da classe do objeto, seja ela qual for. O valor da mãe,
`"Data Processor"`, só existe para que todo `DataProcessor` tenha um `name`; nenhum objeto de
`DataProcessor` puro chega a ser criado.

## Os contadores

Os dois números já existem dentro de cada processador:

- o **total** de itens recebidos é o `self._rank`: ele começa em 0 e avança 1 a cada item
  guardado, e nunca volta, nem quando um item sai pelo `output`;
- os itens que **restam** são os que estão na fila: o tamanho de `self._items`.

Dois métodos comuns em `DataProcessor` os mostram para fora:

```python
    def total(self) -> int:
        return self._rank

    def remaining(self) -> int:
        return len(self._items)
```

Eles ficam logo antes de `_store`. `DataStream` chama `processor.total()` e
`processor.remaining()` em vez de ler `_rank` e `_items` direto: os atributos com `_` são
internos do processador, e quem está fora usa os métodos.

`remaining` também resolve o problema da fila vazia
([A classe base](../03-ex0/02-a-classe-base.md#output)): antes de chamar `output`, quem usa o
processador pode perguntar se ainda há itens. O exercício 2 faz isso.
