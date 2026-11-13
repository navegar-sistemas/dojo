---
sidebar_position: 8
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 ex2/data_pipeline.py) - <<'FIM'
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
FIM
```

Sem nenhuma linha impressa, a saída é a esperada.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex2
.venv/bin/mypy --disallow-untyped-defs ex2
```

```text
Success: no issues found in 1 source file
```

## CSV e JSON com caracteres especiais

Os dados do cenário não têm vírgula, aspas nem quebra de linha. Este teste manda três textos que
têm:

```bash
python3 -B -c 'import sys; sys.path.insert(0, "ex2")
from data_pipeline import DataStream, TextProcessor, CSVExportPlugin, JSONExportPlugin
stream = DataStream()
stream.register_processor(TextProcessor())
data = ["a,b", "say \"hi\"", "line\nbreak"]
stream.process_stream([data, data])
stream.output_pipeline(3, CSVExportPlugin())
stream.output_pipeline(3, JSONExportPlugin())'
```

O lote tem a mesma lista duas vezes: a primeira cópia vai para o CSV, e a segunda para o JSON.

```text
CSV Output:
"a,b","say ""hi""","line
break"
JSON Output:
{"item_3": "a,b", "item_4": "say \"hi\"", "item_5": "line\u000abreak"}
```

- no CSV, os três campos estão entre aspas; as aspas internas estão dobradas, e a quebra de
  linha continua dentro do terceiro campo, que só termina na aspa de `break"`;
- no JSON, as aspas viraram `\"` e a quebra de linha virou `\u000a`. Os ranks continuam de 3 a 5,
  porque o processador já tinha recebido os três itens da primeira cópia.

Um leitor de JSON de verdade confirma que o texto é válido. O Python tem um, o módulo `json`; o
enunciado não o permite no código entregue, mas ele serve para conferir no terminal. O `python3
-m json.tool` lê um JSON da entrada e o imprime formatado, ou mostra um erro se o JSON for
inválido:

```bash
printf '%s\n' '{"item_3": "a,b", "item_4": "say \"hi\"", "item_5": "line\u000abreak"}' | python3 -m json.tool
```

```text
{
    "item_3": "a,b",
    "item_4": "say \"hi\"",
    "item_5": "line\nbreak"
}
```

- `printf '%s\n' '...'` imprime o texto entre as aspas simples exatamente como está, seguido de
  uma quebra de linha. O `echo` não serve aqui: em alguns *shells* (o programa que interpreta os
  comandos digitados no terminal), como o zsh, padrão do macOS, ele transforma o `\u000a` numa
  quebra de linha de verdade antes de o JSON chegar ao leitor;
- o `|` (*pipe*) liga a saída do `printf` à entrada do `json.tool`.

## Um plugin que não cumpre a regra \{#plugin-errado}

Crie um arquivo de experimento com um plugin cujo `process_output` recebe o tipo errado:

```python title="experimentos/plugin_errado.py"
from data_pipeline import DataStream


class BrokenPlugin:
    def process_output(self, data: list[str]) -> None:
        print(data)


DataStream().output_pipeline(1, BrokenPlugin())
```

O arquivo importa `DataStream` de `ex2/data_pipeline.py`, que está em outra pasta. O mypy não
acha o `data_pipeline` sozinho; a variável `MYPYPATH`, escrita antes do comando, diz a ele em que
pasta procurar os módulos importados:

```bash
MYPYPATH=ex2 .venv/bin/mypy --disallow-untyped-defs experimentos/plugin_errado.py
```

```text
experimentos/plugin_errado.py:9: error: Argument 2 to "output_pipeline" of "DataStream" has incompatible type "BrokenPlugin"; expected "ExportPlugin"  [arg-type]
experimentos/plugin_errado.py:9: note: Following member(s) of "BrokenPlugin" have conflicts:
experimentos/plugin_errado.py:9: note:     Expected:
experimentos/plugin_errado.py:9: note:         def process_output(self, data: list[tuple[int, str]]) -> None
experimentos/plugin_errado.py:9: note:     Got:
experimentos/plugin_errado.py:9: note:         def process_output(self, data: list[str]) -> None
Found 1 error in 1 file (checked 1 source file)
```

O mypy compara o método do plugin com o do `ExportPlugin` e mostra os dois: o esperado
(*Expected*) e o recebido (*Got*). É o `Protocol` conferindo o duck typing.
