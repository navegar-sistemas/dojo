---
sidebar_position: 1
title: Conferir tudo
---

# Conferir tudo

Rode tudo a partir da pasta `code-nexus`.

## Os arquivos

```bash
ls -1 *.py ex3 ex4
```

```text
battle.py
capacitor.py
data_pipeline.py
data_processor.py
data_stream.py
tournament.py

ex3:
__init__.py
__pycache__
capability.py
creature.py
factory.py
flame.py
transform.py

ex4:
__init__.py
__pycache__
aggressive.py
normal.py
strategy.py
```

- `*.py` é expandido pelo terminal para todos os arquivos `.py` da pasta atual; `ex3` e `ex4`
  são listadas por dentro. O `-1` põe um nome por linha;
- os seis arquivos da raiz e os dois `__init__.py` têm os nomes exatos do enunciado. Um nome
  errado (uma letra trocada, `.py` faltando) faz o exercício não ser encontrado;
- as pastas `__pycache__` são o cache que o Python cria ao importar os módulos dos pacotes; não
  fazem parte da entrega e podem ser apagadas.

A ordem dos nomes pode mudar de um sistema para outro: no Linux, o `ls` costuma ignorar o `_` ao
ordenar, e `__init__.py` e `__pycache__` aparecem no meio da lista.

## Estilo e tipos

```bash
.venv/bin/flake8 *.py ex3 ex4
.venv/bin/mypy --disallow-untyped-defs *.py ex3 ex4
```

```text
data_processor.py:111: error: Argument 1 to "ingest" of "NumericProcessor" has incompatible type "str"; expected "int | float | list[int | float]"  [arg-type]
Found 1 error in 1 file (checked 16 source files)
```

O flake8 não imprime nada. O mypy confere os dezesseis arquivos entregues (seis na raiz, seis em
`ex3` e quatro em `ex4`) e acusa só a chamada proposital do exercício 0
([O erro proposital do mypy](../03-ex0/07-o-erro-proposital-do-mypy.md)).

## As saídas

Rode de novo os `diff` da página "Rodar e conferir" de cada exercício:
[0](../03-ex0/09-rodar-e-conferir.md), [1](../04-ex1/07-rodar-e-conferir.md),
[2](../05-ex2/08-rodar-e-conferir.md), [3](../07-ex3/11-rodar-e-conferir.md) e
[4](../08-ex4/09-rodar-e-conferir.md). Nenhum deles pode imprimir nada.

## Nenhum programa trava

Todos os programas terminam com código de saída `0`, o número que um programa devolve ao
terminar quando deu tudo certo:

```bash
for f in data_processor.py data_stream.py data_pipeline.py battle.py capacitor.py tournament.py; do
    python3 "$f" > /dev/null
    echo "$f: $?"
done
```

```text
data_processor.py: 0
data_stream.py: 0
data_pipeline.py: 0
battle.py: 0
capacitor.py: 0
tournament.py: 0
```

- `for f in ...; do ...; done` repete os comandos entre `do` e `done` uma vez para cada nome da
  lista, com o nome na variável `f`; `"$f"` é o valor dela;
- `> /dev/null` descarta a saída do programa, que já foi conferida pelos `diff`. `/dev/null` é
  um arquivo especial que joga fora tudo o que recebe;
- `$?` é o código de saída do último comando, e `echo` o mostra ao lado do nome.

O torneio com erro também termina com `0`: o `StrategyError` é capturado pelo `except` de
`battle`, e o programa segue até o fim.

## Só os imports permitidos

```bash
grep -n "import" *.py ex3/*.py ex4/*.py
```

```text
battle.py:1:from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
capacitor.py:1:from ex3 import TransformCreatureFactory
capacitor.py:2:from ex3.capability import TransformCapability
capacitor.py:3:from ex3.creature import Creature
data_pipeline.py:1:from abc import ABC, abstractmethod
data_pipeline.py:2:from typing import Any, Callable, Protocol
data_processor.py:1:from abc import ABC, abstractmethod
data_processor.py:2:from typing import Any, Callable
data_stream.py:1:from abc import ABC, abstractmethod
data_stream.py:2:from typing import Any, Callable
tournament.py:1:from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
tournament.py:2:from ex4 import (
ex3/__init__.py:1:from .factory import CreatureFactory, FlameFactory, TransformCreatureFactory
ex3/capability.py:1:from abc import ABC, abstractmethod
ex3/creature.py:1:from abc import ABC, abstractmethod
ex3/factory.py:1:from abc import ABC, abstractmethod
ex3/factory.py:3:from .creature import Creature
ex3/factory.py:4:from .flame import Flameling, Pyrodon
ex3/factory.py:5:from .transform import Morphagon, Shiftling
ex3/flame.py:1:from .creature import Creature
ex3/transform.py:1:from .capability import TransformCapability
ex3/transform.py:2:from .creature import Creature
ex4/__init__.py:1:from .aggressive import AggressiveStrategy
ex4/__init__.py:2:from .normal import NormalStrategy
ex4/__init__.py:3:from .strategy import BattleStrategy, StrategyError
ex4/aggressive.py:1:from ex3.capability import TransformCapability
ex4/aggressive.py:2:from ex3.creature import Creature
ex4/aggressive.py:4:from .strategy import BattleStrategy, StrategyError
ex4/normal.py:1:from ex3.creature import Creature
ex4/normal.py:3:from .strategy import BattleStrategy, StrategyError
ex4/strategy.py:1:from abc import ABC, abstractmethod
ex4/strategy.py:3:from ex3.creature import Creature
```

O `grep` procura a palavra nos arquivos e mostra cada linha encontrada, com o arquivo e o número
da linha (`-n`). Da biblioteca do Python, só `abc` e `typing` aparecem. O resto são imports entre
os arquivos do próprio projeto: os de `ex3` e `ex4` e os relativos, com ponto, dentro de cada
pacote. A linha `from ex4 import (` continua nas linhas seguintes do `tournament.py`, com os nomes
das estratégias e da exceção. A ordem dos arquivos de `ex3` e `ex4` pode mudar no Linux, como a
do `ls`.

## Nem eval nem exec

```bash
grep -n -w -E "eval|exec" *.py ex3/*.py ex4/*.py
```

O comando não imprime nada: nenhum arquivo usa as duas funções proibidas pelo enunciado. O `-w`
procura só a palavra inteira (`exec`, e não um pedaço de outra palavra), e o `-E` permite o `|`,
que quer dizer "uma ou outra".
