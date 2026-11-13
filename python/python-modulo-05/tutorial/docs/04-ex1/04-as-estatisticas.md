---
sidebar_position: 4
title: As estatísticas
---

# As estatísticas

`print_processors_stats` imprime as estatísticas do fluxo: um cabeçalho e uma linha por
processador registrado, com o nome e os contadores da página
[Nome e contadores](./02-nome-e-contadores.md). O método entra em `DataStream`, depois de
`process_stream`.

```python
    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")
        if not self._processors:
            print("No processor found, no data")
        for processor in self._processors:
            print(f"{processor.name}: total {processor.total()} items "
                  f"processed, remaining {processor.remaining()} on processor")
```

- o cabeçalho `== DataStream statistics ==` sai sempre;
- `not self._processors` é verdadeiro quando a lista está vazia: uma lista vazia conta como
  "falso" num `if`. Sem processador registrado, a mensagem do enunciado é
  `No processor found, no data`;
- depois, uma linha por processador, na ordem do registro, com o `name`, o `total()` e o
  `remaining()` de cada um ([Nome e contadores](./02-nome-e-contadores.md)). Com a lista vazia,
  o `for` não roda nenhuma vez;
- a f-string foi dividida em duas partes, como a mensagem de erro de `process_stream`. Toda parte
  que tem `{}` precisa do seu próprio `f`: aqui as duas têm; na mensagem de erro, só a segunda.

As linhas em branco entre os blocos da saída não são impressas por este método: quem o chama
decide onde elas ficam ([A demonstração](./05-a-demonstracao.md)). Por isso o mesmo método
serve para o exercício 1, em que as estatísticas vêm coladas à linha anterior, e para o exercício
2, em que vêm depois de uma linha vazia.

## Os números depois do consumo

O cenário termina com `Numeric 3, Text 2, Log 1`: três `output` no processador de números, dois
no de textos e um no de logs.

| Processador | total | remaining antes | consumidos | remaining depois |
|---|---|---|---|---|
| Numeric | 8 | 8 | 3 | 5 |
| Text | 3 | 3 | 2 | 1 |
| Log | 2 | 2 | 1 | 1 |

O total não muda: ele conta os itens que **entraram**, e o `output` só tira itens da fila.
