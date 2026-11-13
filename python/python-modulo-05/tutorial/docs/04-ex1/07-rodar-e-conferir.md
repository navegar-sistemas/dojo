---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 ex1/data_stream.py) - <<'FIM'
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
FIM
```

Sem nenhuma linha impressa, a saída é a esperada.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex1
.venv/bin/mypy --disallow-untyped-defs ex1
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy não acha problema: o exercício 1 não tem a chamada
proposital do exercício 0.

## A ordem do registro

Um elemento vai para o **primeiro** processador registrado que o aceita, e a ordem do registro
decide o destino de um elemento aceito por mais de um. Com os três processadores atuais, só a
lista vazia `[]` está nesse caso: os três a aceitam, porque `is_list_of` dá `True` para uma lista
sem itens, e ela vai para o primeiro registrado sem guardar nada. Nenhum outro elemento é aceito
por mais de um. O teste abaixo registra os três em ordem inversa e manda o lote do enunciado:

```bash
python3 -B -c 'import sys; sys.path.insert(0, "ex1")
from data_stream import DataStream, LogProcessor, NumericProcessor, TextProcessor, first_batch
stream = DataStream()
stream.register_processor(LogProcessor())
stream.register_processor(TextProcessor())
stream.register_processor(NumericProcessor())
stream.process_stream(first_batch())
stream.print_processors_stats()'
```

```text
== DataStream statistics ==
Log Processor: total 2 items processed, remaining 2 on processor
Text Processor: total 3 items processed, remaining 3 on processor
Numeric Processor: total 4 items processed, remaining 4 on processor
```

Os totais são os mesmos; só a ordem das linhas das estatísticas muda, porque elas seguem a
ordem do registro.
