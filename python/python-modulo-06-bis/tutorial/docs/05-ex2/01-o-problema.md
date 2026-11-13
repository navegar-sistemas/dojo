---
sidebar_position: 1
title: O problema
---

# O problema

O fluxo do exercício 1 recebe e guarda os dados, mas eles só saem um a um, pelo `output` de cada
processador. Falta a saída do sistema: tirar os dados processados e entregá-los num formato que
outro programa entenda, como CSV ou JSON. Os formatos possíveis são muitos, e o fluxo não deveria
mudar a cada formato novo. O exercício 2 resolve isso com **plugins**: objetos que sabem exportar
dados num formato e se encaixam no fluxo sem que ele saiba qual é o formato.

## O que o enunciado pede

Um arquivo `data_pipeline.py`, na raiz do projeto, que parte do código do exercício 1 e
acrescenta:

- a classe **`ExportPlugin`**, filha da classe especial `Protocol` (de `typing`), com um único
  método, que serve de regra para todo plugin de exportação:

  ```python
  def process_output(self, data: list[tuple[int, str]]) -> None:
  ```

  O parâmetro `data` é uma lista de tuplas `(rank, texto)`, o mesmo formato que o `output` dos
  processadores devolve;

- em `DataStream`, o método

  ```python
  def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
  ```

  que, depois de um `process_stream`, tira até `nb` itens de **cada** processador registrado e os
  exporta com o plugin recebido;

- pelo menos dois plugins: um que exporta em **CSV** e outro em **JSON**, com o texto de cada
  formato montado à mão, sem `import` de bibliotecas de CSV ou JSON.

## O ponto de partida

Copie o arquivo do exercício 1 com o nome novo:

```bash
cp data_stream.py data_pipeline.py
```

As classes e as funções de conferência ficam inteiras, e a função `first_batch` também. Apague
`consume`, o `main` e o `if __name__ == "__main__":`, que dão lugar ao cenário novo
([A demonstração](./06-a-demonstracao.md)).

## Duck typing

Os plugins são compatíveis com `ExportPlugin` por **duck typing**: não herdam dele, só têm o
método certo ([Protocol e duck typing](./02-protocol-e-duck-typing.md)).

## A saída esperada

```text
=== Code Nexus - Data Pipeline ===

Initialize Data Stream...

== DataStream statistics ==
No processor found, no data

Registering Processors

Send first batch of data on stream: ['Hello world', [3.14, -1, 2.71], [{'log_level': 'WARNING', 'log_message': 'Telnet access! Use ssh instead'}, {'log_level': 'INFO', 'log_message': 'User wil is connected'}], 42, ['Hi', 'five']]

== DataStream statistics ==
Numeric Processor: total 4 items processed, remaining 4 on processor
Text Processor: total 3 items processed, remaining 3 on processor
Log Processor: total 2 items processed, remaining 2 on processor

Send 3 processed data from each processor to a CSV plugin:
CSV Output:
3.14,-1,2.71
CSV Output:
Hello world,Hi,five
CSV Output:
WARNING: Telnet access! Use ssh instead,INFO: User wil is connected

== DataStream statistics ==
Numeric Processor: total 4 items processed, remaining 1 on processor
Text Processor: total 3 items processed, remaining 0 on processor
Log Processor: total 2 items processed, remaining 0 on processor

Send another batch of data: [21, ['I love AI', 'LLMs are wonderful', 'Stay healthy'], [{'log_level': 'ERROR', 'log_message': '500 server crash'}, {'log_level': 'NOTICE', 'log_message': 'Certificate expires in 10 days'}], [32, 42, 64, 84, 128, 168], 'World hello']

== DataStream statistics ==
Numeric Processor: total 11 items processed, remaining 8 on processor
Text Processor: total 7 items processed, remaining 4 on processor
Log Processor: total 4 items processed, remaining 2 on processor

Send 5 processed data from each processor to a JSON plugin:
JSON Output:
{"item_3": "42", "item_4": "21", "item_5": "32", "item_6": "42", "item_7": "64"}
JSON Output:
{"item_3": "I love AI", "item_4": "LLMs are wonderful", "item_5": "Stay healthy", "item_6": "World hello"}
JSON Output:
{"item_2": "ERROR: 500 server crash", "item_3": "NOTICE: Certificate expires in 10 days"}

== DataStream statistics ==
Numeric Processor: total 11 items processed, remaining 3 on processor
Text Processor: total 7 items processed, remaining 0 on processor
Log Processor: total 4 items processed, remaining 0 on processor
```

A sequência do cenário:

1. o fluxo começa vazio, e os três processadores são registrados;
2. o mesmo primeiro lote do exercício 1 é enviado;
3. até 3 itens de cada processador vão para o plugin CSV;
4. um segundo lote é enviado;
5. até 5 itens de cada processador vão para o plugin JSON. O processador de textos só tinha 4, e
   exporta os 4; o de logs, 2.

Diferentemente do exercício 1, aqui as estatísticas vêm sempre depois de uma linha vazia.
