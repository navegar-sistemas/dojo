---
sidebar_position: 5
title: A demonstração
---

# A demonstração

As funções de teste do exercício 0 foram apagadas do arquivo
([O ponto de partida](./01-o-problema.md#o-ponto-de-partida)); no lugar delas, no fim do arquivo,
entra o cenário do fluxo.

## O lote

```python
def first_batch() -> list[Any]:
    return [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {"log_level": "WARNING",
             "log_message": "Telnet access! Use ssh instead"},
            {"log_level": "INFO", "log_message": "User wil is connected"},
        ],
        42,
        ["Hi", "five"],
    ]
```

Uma função que devolve o lote deixa o `main` curto e o tipo explícito: `list[Any]`, uma lista com
elementos de qualquer tipo, que é o que `process_stream` recebe. O primeiro dicionário foi
quebrado em duas linhas para caber nos 79 caracteres.

## Consumir itens

```python
def consume(processor: DataProcessor, count: int) -> None:
    for _ in range(count):
        processor.output()
```

`consume` chama `output` `count` vezes e descarta o que ele devolve. O enunciado pede que os
itens sejam consumidos com o `output` de cada processador; o resultado não aparece na saída.

## O main

```python
def main() -> None:
    print("=== Code Nexus - Data Stream ===")
    print("\nInitialize Data Stream...")
    stream = DataStream()
    stream.print_processors_stats()

    print("\nRegistering Numeric Processor")
    numeric = NumericProcessor()
    stream.register_processor(numeric)
    batch = first_batch()
    print(f"\nSend first batch of data on stream: {batch}")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nRegistering other data processors")
    text = TextProcessor()
    log = LogProcessor()
    stream.register_processor(text)
    stream.register_processor(log)
    print("Send the same batch again")
    stream.process_stream(batch)
    stream.print_processors_stats()

    print("\nConsume some elements from the data processors: "
          "Numeric 3, Text 2, Log 1")
    consume(numeric, 3)
    consume(text, 2)
    consume(log, 1)
    stream.print_processors_stats()
```

- o `\n` no começo de um texto é uma **quebra de linha**: `print("\nRegistering ...")` imprime
  uma linha vazia e depois o texto. É assim que saem as linhas vazias da saída do enunciado;
- `numeric`, `text` e `log` guardam os processadores em variáveis porque o `main` precisa deles
  duas vezes: para registrar no fluxo e, no fim, para consumir itens. O fluxo e o `main` apontam
  para os **mesmos** objetos: o que `consume` tira aparece nas estatísticas do fluxo;
- as linhas em branco entre os grupos de comandos do `main` só separam os passos do cenário para
  quem lê; elas não aparecem na saída.

O `main` termina com o `if __name__ == "__main__":` de sempre.
