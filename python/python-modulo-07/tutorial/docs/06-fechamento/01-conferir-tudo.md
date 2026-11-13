---
sidebar_position: 1
title: Conferir tudo
---

# Conferir tudo

Rode tudo a partir da pasta `datadeck`.

## Os arquivos

```bash
ls -1 *.py ex0 ex1 ex2
```

```text
battle.py
capacitor.py
tournament.py

ex0:
__init__.py
__pycache__
creature.py
factory.py

ex1:
__init__.py
__pycache__
capability.py
creature.py
factory.py

ex2:
__init__.py
__pycache__
strategy.py
```

`*.py` quer dizer "todos os arquivos terminados em `.py` da pasta atual": os três programas de
teste, com os nomes exatos que o enunciado pede. Cada pasta de exercício tem o seu `__init__.py`,
obrigatório pelo enunciado. As pastas `__pycache__` são o cache que o Python criou ao importar os
pacotes; não fazem parte da entrega.

## Estilo e tipos

```bash
.venv/bin/flake8 battle.py capacitor.py tournament.py ex0 ex1 ex2
.venv/bin/mypy --disallow-untyped-defs battle.py capacitor.py tournament.py ex0 ex1 ex2
```

```text
Success: no issues found in 12 source files
```

O flake8 não imprime nada, e o mypy confere os doze arquivos: os três programas e os nove
arquivos dos pacotes.

## As saídas

Rode de novo os `diff` da página "Rodar e conferir" de cada exercício:
[0](../03-ex0/09-rodar-e-conferir.md), [1](../04-ex1/08-rodar-e-conferir.md) e
[2](../05-ex2/08-rodar-e-conferir.md). Nenhum deles pode imprimir nada.

## Nenhum programa quebra

Todos os programas terminam com código de saída `0`, o número que um programa devolve ao
terminar quando deu tudo certo:

```bash
for f in battle.py capacitor.py tournament.py; do
    python3 "$f" > /dev/null
    echo "$f: $?"
done
```

```text
battle.py: 0
capacitor.py: 0
tournament.py: 0
```

- `for f in ...; do ...; done` repete os comandos entre `do` e `done` uma vez para cada nome da
  lista, com o nome na variável `f`; `"$f"` é o valor dela;
- `> /dev/null` descarta a saída do programa, que já foi conferida pelos `diff`. `/dev/null` é
  um arquivo especial que joga fora tudo o que recebe;
- `$?` é o código de saída do último comando, e `echo` o mostra ao lado do nome.

O `tournament.py` também termina com `0`, mesmo com o torneio 1 abortado: a exceção foi tratada
dentro de `battle`.

## Só os imports permitidos

```bash
grep -n "import" *.py ex0/*.py ex1/*.py ex2/*.py | grep -v "from ex[0-2]\|from \."
```

```text
ex0/creature.py:1:from abc import ABC, abstractmethod
ex0/factory.py:1:from abc import ABC, abstractmethod
ex1/capability.py:1:from abc import ABC, abstractmethod
ex2/strategy.py:1:from abc import ABC, abstractmethod
```

- o primeiro `grep` procura a palavra `import` nos arquivos e mostra cada linha encontrada, com o
  arquivo e o número da linha (`-n`);
- o `|` (*pipe*) entrega essa lista ao segundo `grep`, e o `-v` dele mostra só as linhas que
  **não** combinam com o padrão: some tudo o que importa do próprio projeto (`from ex0`,
  `from ex1`, `from ex2` e os imports relativos, `from .`). O `\|` separa as alternativas do
  padrão, `[0-2]` quer dizer "um dígito de 0 a 2", e `\.` é um ponto de verdade (sem a barra, o
  ponto combinaria com qualquer caractere).

Sobram só os imports da biblioteca do Python: `abc`, autorizado (`from abc import ...` importa o
mesmo módulo que o `import abc` da lista). O `typing`, também autorizado, não foi preciso. Os
imports do próprio projeto não estão na lista de autorizados; a leitura do tutorial é que fazem
parte do pedido, porque o enunciado manda o exercício 1 "usar o conteúdo do pacote `ex0` e
construir sobre ele" e o exercício 2 "criar várias fábricas de Criaturas (de `ex0` e de `ex1`)".

## Nem eval nem exec

```bash
grep -n "eval\|exec" *.py ex0/*.py ex1/*.py ex2/*.py
```

O comando não imprime nada: as duas funções proibidas não aparecem em nenhum arquivo.
