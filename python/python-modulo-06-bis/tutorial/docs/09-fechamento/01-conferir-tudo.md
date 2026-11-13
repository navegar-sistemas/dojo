---
sidebar_position: 1
title: Conferir tudo
---

# Conferir tudo

Rode tudo a partir da pasta `code-nexus`.

## Os arquivos

```bash
ls ex0 ex1 ex2
```

```text
ex0:
data_processor.py

ex1:
data_stream.py

ex2:
data_pipeline.py
```

Um arquivo por pasta, com o nome exato que o enunciado pede. Um nome errado (uma letra trocada,
`.py` faltando) faz o exercício não ser encontrado. Se aparecer uma pasta `__pycache__`, ela é
o cache que o Python cria ao importar um arquivo; não faz parte da entrega e pode ser apagada.

## Estilo e tipos

```bash
.venv/bin/flake8 ex0 ex1 ex2
.venv/bin/mypy --disallow-untyped-defs ex0 ex1 ex2
```

```text
ex0/data_processor.py:111: error: Argument 1 to "ingest" of "NumericProcessor" has incompatible type "str"; expected "int | float | list[int | float]"  [arg-type]
Found 1 error in 1 file (checked 3 source files)
```

O flake8 não imprime nada. O mypy confere os três arquivos e acusa só a chamada proposital do
exercício 0 ([O erro proposital do mypy](../03-ex0/06-o-erro-proposital-do-mypy.md)).

## As saídas

Rode de novo os `diff` da página "Rodar e conferir" de cada exercício:
[0](../03-ex0/09-rodar-e-conferir.md), [1](../04-ex1/07-rodar-e-conferir.md) e
[2](../05-ex2/08-rodar-e-conferir.md). Nenhum deles pode imprimir nada.

## Nenhum programa trava

Todos os programas terminam com código de saída `0`, o número que um programa devolve ao
terminar quando deu tudo certo:

```bash
for f in ex0/data_processor.py ex1/data_stream.py ex2/data_pipeline.py; do
    python3 "$f" > /dev/null
    echo "$f: $?"
done
```

```text
ex0/data_processor.py: 0
ex1/data_stream.py: 0
ex2/data_pipeline.py: 0
```

- `for f in ...; do ...; done` repete os comandos entre `do` e `done` uma vez para cada nome da
  lista, com o nome na variável `f`; `"$f"` é o valor dela;
- `> /dev/null` descarta a saída do programa, que já foi conferida pelos `diff`. `/dev/null` é
  um arquivo especial que joga fora tudo o que recebe;
- `$?` é o código de saída do último comando, e `echo` o mostra ao lado do nome.

## Só os imports permitidos

```bash
grep -n "import" ex0/*.py ex1/*.py ex2/*.py
```

```text
ex0/data_processor.py:1:from abc import ABC, abstractmethod
ex0/data_processor.py:2:from typing import Any, Callable
ex1/data_stream.py:1:from abc import ABC, abstractmethod
ex1/data_stream.py:2:from typing import Any, Callable
ex2/data_pipeline.py:1:from abc import ABC, abstractmethod
ex2/data_pipeline.py:2:from typing import Any, Callable, Protocol
```

O `grep` procura a palavra nos arquivos e mostra cada linha encontrada, com o arquivo e o número
da linha (`-n`). Só `abc` e `typing` aparecem.
