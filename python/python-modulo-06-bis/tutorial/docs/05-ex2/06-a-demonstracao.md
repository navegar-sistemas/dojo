---
sidebar_position: 6
title: A demonstração
---

# A demonstração

No lugar do cenário do exercício 1, apagado no [ponto de partida](./01-o-problema.md#o-ponto-de-partida),
entra o cenário do pipeline, no fim do arquivo. A função `first_batch` continua, e entra uma
segunda, logo depois dela, com o outro lote do enunciado:

```python
def second_batch() -> list[Any]:
    return [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {"log_level": "ERROR", "log_message": "500 server crash"},
            {"log_level": "NOTICE",
             "log_message": "Certificate expires in 10 days"},
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello",
    ]
```

## As estatísticas com a linha vazia

Neste exercício, todo bloco de estatísticas vem depois de uma linha vazia. Uma função curta
junta as duas coisas:

```python
def show_stats(stream: DataStream) -> None:
    print()
    stream.print_processors_stats()
```

## O main

```python
def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")
    print("\nInitialize Data Stream...")
    stream = DataStream()
    show_stats(stream)

    print("\nRegistering Processors")
    stream.register_processor(NumericProcessor())
    stream.register_processor(TextProcessor())
    stream.register_processor(LogProcessor())

    batch = first_batch()
    print(f"\nSend first batch of data on stream: {batch}")
    stream.process_stream(batch)
    show_stats(stream)

    print("\nSend 3 processed data from each processor to a CSV plugin:")
    stream.output_pipeline(3, CSVExportPlugin())
    show_stats(stream)

    batch = second_batch()
    print(f"\nSend another batch of data: {batch}")
    stream.process_stream(batch)
    show_stats(stream)

    print("\nSend 5 processed data from each processor to a JSON plugin:")
    stream.output_pipeline(5, JSONExportPlugin())
    show_stats(stream)
```

- os processadores são criados direto dentro do `register_processor`: o `main` não precisa mais
  deles depois, porque quem tira os itens agora é o `output_pipeline`;
- `CSVExportPlugin()` e `JSONExportPlugin()` criam os plugins na hora da chamada. O mypy confere
  que cada um combina com o `ExportPlugin` pedido pela assinatura.

## Os números do cenário

| Momento | Numeric (total / restam) | Text | Log |
|---|---|---|---|
| depois do primeiro lote | 4 / 4 | 3 / 3 | 2 / 2 |
| depois do CSV com até 3 | 4 / 1 | 3 / 0 | 2 / 0 |
| depois do segundo lote | 11 / 8 | 7 / 4 | 4 / 2 |
| depois do JSON com até 5 | 11 / 3 | 7 / 0 | 4 / 0 |

O segundo lote dá 7 números (o `21` e os seis da lista), 4 textos (os três da lista e
`'World hello'`) e 2 logs. No JSON, o processador de números começa pelo item de rank 3, o `"42"`
que sobrou do primeiro lote, e os ranks seguem a ordem de chegada: `item_3` a `item_7`.
