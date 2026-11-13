---
sidebar_position: 1
title: Conferir tudo
---

# Conferir tudo

Rode tudo a partir da pasta `funcmage`.

## Os arquivos

```bash
ls ex0 ex1 ex2 ex3 ex4
```

```text
ex0:
lambda_spells.py

ex1:
higher_magic.py

ex2:
scope_mysteries.py

ex3:
functools_artifacts.py

ex4:
decorator_mastery.py
```

Um arquivo por pasta, com o nome exato que o enunciado pede. Um nome errado (uma letra trocada,
`.py` faltando) faz o exercício não ser encontrado. Se aparecer uma pasta `__pycache__`, ela é o
cache que o Python cria ao importar um arquivo sem o `-B`; não faz parte da entrega e pode ser
apagada.

## Estilo e tipos

```bash
.venv/bin/flake8 ex0 ex1 ex2 ex3 ex4
.venv/bin/mypy --disallow-untyped-defs ex0 ex1 ex2 ex3 ex4
```

```text
Success: no issues found in 5 source files
```

O flake8 não imprime nada, e o mypy confere os cinco arquivos sem achar problema: todas as
funções, inclusive as de dentro de outras funções, têm type hints.

## As saídas

Rode de novo as comparações da página "Rodar e conferir" de cada exercício:
[0](../03-ex0/07-rodar-e-conferir.md), [1](../04-ex1/09-rodar-e-conferir.md),
[2](../05-ex2/08-rodar-e-conferir.md), [3](../06-ex3/08-rodar-e-conferir.md) e
[4](../07-ex4/08-rodar-e-conferir.md). Nenhum `diff` pode imprimir nada, e o `grep` do
exercício 4 precisa imprimir a linha do tempo.

## Nenhum programa trava

Todos os programas terminam com código de saída `0`, o número que um programa devolve ao terminar
quando deu tudo certo:

```bash
for f in ex0/lambda_spells.py ex1/higher_magic.py ex2/scope_mysteries.py ex3/functools_artifacts.py ex4/decorator_mastery.py; do
    python3 "$f" > /dev/null
    echo "$f: $?"
done
```

```text
ex0/lambda_spells.py: 0
ex1/higher_magic.py: 0
ex2/scope_mysteries.py: 0
ex3/functools_artifacts.py: 0
ex4/decorator_mastery.py: 0
```

- `for f in ...; do ...; done` repete os comandos entre `do` e `done` uma vez para cada nome da
  lista, com o nome na variável `f`; `"$f"` é o valor dela;
- `> /dev/null` descarta a saída do programa, que já foi conferida pelos `diff`. `/dev/null` é um
  arquivo especial que joga fora tudo o que recebe;
- `$?` é o código de saída do último comando, e `echo` o mostra ao lado do nome.

## Só os imports permitidos

```bash
grep -n "import" ex[0-4]/*.py
```

```text
ex1/higher_magic.py:1:from collections.abc import Callable
ex2/scope_mysteries.py:1:from collections.abc import Callable
ex2/scope_mysteries.py:2:from typing import Any
ex3/functools_artifacts.py:1:import functools
ex3/functools_artifacts.py:2:import operator
ex3/functools_artifacts.py:3:from collections.abc import Callable
ex3/functools_artifacts.py:4:from typing import Any
ex4/decorator_mastery.py:1:import time
ex4/decorator_mastery.py:2:from collections.abc import Callable
ex4/decorator_mastery.py:3:from functools import wraps
ex4/decorator_mastery.py:4:from typing import Any
```

`ex[0-4]/*.py` são os arquivos `.py` das pastas `ex0` a `ex4` (o `[0-4]` aceita um algarismo de 0
a 4; um `ex*` pegaria também a pasta `experimentos`). O exercício 0 não importa nada; `functools`
e `operator` só aparecem no exercício 3, e do `functools` o exercício 4 só traz `wraps`;
`Callable` vem sempre de `collections.abc`.

## Nada do que é proibido

```bash
grep -nwE "global|eval|exec|open" ex[0-4]/*.py || echo "nada encontrado"
```

```text
nada encontrado
```

`grep -w` procura palavras inteiras, e `-E` permite a lista de alternativas separadas por `|`:
`global` (variável global), `eval` e `exec` (proibidas), `open` (abrir arquivo, proibido). Quando
o `grep` não acha nada, ele termina com o código de saída 1, e o `||` roda o comando seguinte só
quando o anterior não termina com 0.
