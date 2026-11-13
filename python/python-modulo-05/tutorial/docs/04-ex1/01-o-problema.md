---
sidebar_position: 1
title: O problema
---

# O problema

No exercício 0, o teste sabia de que tipo era cada dado e chamava o processador certo à mão. Num
sistema de verdade, os dados chegam misturados numa sequência só, um **fluxo** (*stream*), e
alguém precisa entregar cada dado ao processador que sabe tratá-lo. O exercício 1 cria esse
distribuidor, a classe `DataStream`, sem que ela precise conhecer as classes dos processadores.

## O que o enunciado pede

Um arquivo `ex1/data_stream.py` que parte do código do exercício 0 e acrescenta a classe
**`DataStream`**, com três métodos de assinatura fixa:

| Método | O que faz |
|---|---|
| `register_processor(self, proc: DataProcessor) -> None` | **registra** um processador: a partir daí, ele recebe dados do fluxo |
| `process_stream(self, stream: list[typing.Any]) -> None` | percorre a lista recebida e entrega cada elemento ao processador registrado que sabe tratá-lo; se nenhum sabe, imprime uma mensagem de erro |
| `print_processors_stats(self) -> None` | imprime as estatísticas de cada processador registrado: quantos itens ele já recebeu no total e quantos ainda estão guardados |

A escolha do processador usa **polimorfismo**: `DataStream` só conhece a classe
`DataProcessor` e chama `validate` e `ingest` sem saber qual filha está do outro lado
([Polimorfismo](../02-conceitos/04-polimorfismo.md)).

## O ponto de partida

Copie o arquivo do exercício 0 com o nome novo:

```bash
cp ex0/data_processor.py ex1/data_stream.py
```

`cp origem destino` copia um arquivo. As quatro classes e as funções de conferência
(`is_number`, `is_text`, `is_log` e `is_list_of`) ficam inteiras; apague do arquivo novo as
funções de teste (`try_validate`, `extract`, `test_numeric`, `test_text`, `test_log`), o `main` e
o `if __name__ == "__main__":`. As próximas páginas acrescentam o que é novo.

## O teste pedido

Um cenário que mostra o fluxo funcionando: as estatísticas dos processadores registrados, o
consumo de alguns itens com o `output` de cada processador, e as estatísticas de novo.

## A saída esperada

```text
=== Code Nexus - Data Stream ===

Initialize Data Stream...
== DataStream statistics ==
No processor found, no data

Registering Numeric Processor

Send first batch of data on stream: ['Hello world', [3.14, -1, 2.71], [{'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'}, {'log_level': 'INFO', 'log_message': 'User wil is connected'}], 42, ['Hi', 'five']]
DataStream error - Can't process element in stream: Hello world
DataStream error - Can't process element in stream: [{'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'}, {'log_level': 'INFO', 'log_message': 'User wil is connected'}]
DataStream error - Can't process element in stream: ['Hi', 'five']
== DataStream statistics ==
Numeric Processor: total 4 items processed, remaining 4 on processor

Registering other data processors
Send the same batch again
== DataStream statistics ==
Numeric Processor: total 8 items processed, remaining 8 on processor
Text Processor: total 3 items processed, remaining 3 on processor
Log Processor: total 2 items processed, remaining 2 on processor

Consume some elements from the data processors: Numeric 3, Text 2, Log 1
== DataStream statistics ==
Numeric Processor: total 8 items processed, remaining 5 on processor
Text Processor: total 3 items processed, remaining 1 on processor
Log Processor: total 2 items processed, remaining 1 on processor
```

A sequência do cenário:

1. o fluxo começa sem processador nenhum;
2. só o processador de números é registrado, e um primeiro lote (*batch*) de cinco elementos é
   enviado: o texto, os logs e a lista de textos são recusados;
3. os processadores de texto e de log são registrados, e o **mesmo** lote é enviado de novo: os
   números entram outra vez, e agora textos e logs também;
4. alguns itens são consumidos com `output`: 3 de números, 2 de textos e 1 de log.

`User wil is connected` está escrito assim no enunciado, com `wil`, e a saída repete o texto
letra por letra.
