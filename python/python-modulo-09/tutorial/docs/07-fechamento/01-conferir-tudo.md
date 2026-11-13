---
sidebar_position: 1
title: Conferir tudo
---

# Conferir tudo

Rode tudo a partir da pasta `cosmic-data`.

## Os arquivos

```bash
ls ex0 ex1 ex2
```

```text
ex0:
space_station.py

ex1:
alien_contact.py

ex2:
space_crew.py
```

Um arquivo por pasta, com o nome exato que o enunciado pede. Um nome errado (uma letra trocada,
`.py` faltando) faz o exercício não ser encontrado. Se aparecer uma pasta `__pycache__`, ela é o
cache que o Python cria ao importar um arquivo; não faz parte da entrega e pode ser apagada.

## Estilo e tipos

```bash
.venv/bin/flake8 ex0 ex1 ex2 experimentos
.venv/bin/mypy --disallow-untyped-defs ex0 ex1 ex2
MYPYPATH=ex0:ex1:ex2 .venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
Success: no issues found in 3 source files
Success: no issues found in 13 source files
```

O flake8 não imprime nada. O mypy confere os três arquivos entregues e, à parte, os 13
experimentos, com a `MYPYPATH` para os que importam os exercícios.

## As saídas

Rode de novo os `diff` da página "Rodar e conferir" de cada exercício:
[0](../03-ex0/05-rodar-e-conferir.md), [1](../04-ex1/07-rodar-e-conferir.md) e
[2](../05-ex2/07-rodar-e-conferir.md). Nenhum deles pode imprimir nada.

## Nenhum programa trava

Todos os programas terminam com código de saída `0`, o número que um programa devolve ao
terminar quando deu tudo certo:

```bash
for f in ex0/space_station.py ex1/alien_contact.py ex2/space_crew.py; do
    .venv/bin/python "$f" > /dev/null
    echo "$f: $?"
done
```

```text
ex0/space_station.py: 0
ex1/alien_contact.py: 0
ex2/space_crew.py: 0
```

- `for f in ...; do ...; done` repete os comandos entre `do` e `done` uma vez para cada nome da
  lista, com o nome na variável `f`; `"$f"` é o valor dela;
- `> /dev/null` descarta a saída do programa, que já foi conferida pelos `diff`. `/dev/null` é
  um arquivo especial que joga fora tudo o que recebe;
- `$?` é o código de saída do último comando, e `echo` o mostra ao lado do nome.

O objeto inválido de cada demonstração não derruba o programa: a `ValidationError` é capturada, e
o código de saída continua `0`.

## Só os imports permitidos

```bash
grep -n "import" ex0/*.py ex1/*.py ex2/*.py
```

```text
ex0/space_station.py:1:from datetime import datetime
ex0/space_station.py:3:from pydantic import BaseModel, Field, ValidationError
ex1/alien_contact.py:1:from datetime import datetime
ex1/alien_contact.py:2:from enum import Enum
ex1/alien_contact.py:4:from pydantic import BaseModel, Field, ValidationError, model_validator
ex2/space_crew.py:1:from datetime import datetime
ex2/space_crew.py:2:from enum import Enum
ex2/space_crew.py:4:from pydantic import BaseModel, Field, ValidationError, model_validator
```

O `grep` procura a palavra nos arquivos e mostra cada linha encontrada, com o arquivo e o número
da linha (`-n`). Só aparecem `pydantic` e os módulos `datetime` e `enum` da biblioteca padrão
([Os `import` permitidos](../00-introducao/02-o-enunciado-em-linguagem-simples.md#os-import-permitidos)).

## Em outras versões do Python

O enunciado aceita qualquer Python a partir do 3.10. Os três programas e os experimentos dão a
mesma saída no Python 3.10, no 3.14 e no 3.15, com o mesmo Pydantic 2.14.3, que o `pip` instala
nas três: as mensagens de erro vêm do Pydantic, e não do Python. Só mudam os números de versão
que o `python3 --version` e o `flake8 --version` imprimem. Para conferir numa máquina com outra
versão, crie um segundo venv com o
Python 3.10 (por exemplo, `python3.10 -m venv .venv310`), instale nele as mesmas bibliotecas e
rode os `diff` com `.venv310/bin/python`.
