---
sidebar_position: 1
title: Conferir tudo
---

# Conferir tudo

Rode tudo a partir da pasta `the-codex`. Os comandos chamam o Python do laboratório pelo caminho,
`lab_env/bin/python`, e funcionam com ou sem o ambiente ativado.

## Os arquivos

```bash
ls -1a ex0 ex1
```

```text
ex0:
.
..
construct.py
loading.py
poetry.lock
pyproject.toml
requirements.txt

ex1:
.
..
.env
.env.example
.gitignore
oracle.py
requirements.txt
```

Os quatro arquivos de cada pasta do enunciado, mais dois que não são entregues: o `poetry.lock`,
gerado pelo Poetry, e o `.env`, com a configuração de verdade. A
[página de entrega](./02-entregar.md) copia só os arquivos pedidos.

```bash
find alchemy -name '*.py' | sort
ls -1 *.py
```

```text
alchemy/__init__.py
alchemy/elements.py
alchemy/grimoire/__init__.py
alchemy/grimoire/dark_spellbook.py
alchemy/grimoire/dark_validator.py
alchemy/grimoire/light_spellbook.py
alchemy/grimoire/light_validator.py
alchemy/potions.py
alchemy/transmutation/__init__.py
alchemy/transmutation/recipes.py
elements.py
ft_alembic_0.py
ft_alembic_1.py
ft_distillation_0.py
ft_kaboom_0.py
ft_kaboom_1.py
ft_transmutation_0.py
```

- `find alchemy -name '*.py'` lista, em todas as pastas dentro de `alchemy`, os arquivos cujo nome
  termina em `.py`; `sort` põe a lista em ordem alfabética;
- `ls -1 *.py` lista os arquivos `.py` da raiz: o `*` casa com qualquer começo de nome.

É a árvore do enunciado ([O enunciado em linguagem simples](../00-introducao/02-o-enunciado-em-linguagem-simples.md#a-árvore-final)).

## Estilo e tipos

```bash
.venv/bin/flake8 ex0 ex1 alchemy *.py
.venv/bin/mypy --disallow-untyped-defs --python-executable lab_env/bin/python ex0 ex1 alchemy *.py
```

```text
ft_alembic_1.py:10: error: Module has no attribute "create_earth"; maybe "create_air"?  [attr-defined]
Found 1 error in 1 file (checked 20 source files)
```

O flake8 não imprime nada. O mypy confere os vinte arquivos `.py` (com o `--python-executable`, que
deixa ele achar o `python-dotenv` do `lab_env`, [Rodar e conferir do exercício 1](../03-ex1/09-rodar-e-conferir.md#estilo-e-tipos))
e acusa só a linha proposital do exercício 2.

Os experimentos também passam, se quiser conferi-los:

```bash
.venv/bin/flake8 experimentos
.venv/bin/mypy --disallow-untyped-defs --python-executable lab_env/bin/python experimentos
```

```text
Success: no issues found in 15 source files
```

## Os programas

```bash
for f in ex0/construct.py ex0/loading.py ex1/oracle.py ft_alembic_0.py ft_alembic_1.py ft_distillation_0.py ft_transmutation_0.py ft_kaboom_0.py ft_kaboom_1.py; do
    lab_env/bin/python "$f" > /dev/null 2>&1
    echo "$f: $?"
done
```

```text
ex0/construct.py: 0
ex0/loading.py: 0
ex1/oracle.py: 0
ft_alembic_0.py: 0
ft_alembic_1.py: 1
ft_distillation_0.py: 0
ft_transmutation_0.py: 0
ft_kaboom_0.py: 0
ft_kaboom_1.py: 1
```

- `for f in ...; do ...; done` repete os comandos entre `do` e `done` uma vez para cada nome da
  lista, com o nome na variável `f`; `"$f"` é o valor dela;
- `> /dev/null 2>&1` descarta as duas saídas, já conferidas pelos `diff` de cada exercício, e
  `echo "$f: $?"` mostra o código de saída.

Os dois `1` são os programas que precisam falhar, de propósito: `ft_alembic_1.py` e
`ft_kaboom_1.py`. Todos os outros terminam normalmente. Para as saídas, rode de novo os `diff` das
páginas "Rodar e conferir": [0](../02-ex0/12-rodar-e-conferir.md),
[1](../03-ex1/09-rodar-e-conferir.md), [2](../05-ex2/07-rodar-e-conferir.md),
[3](../06-ex3/07-rodar-e-conferir.md) e [4](../07-ex4/07-rodar-e-conferir.md).

## Só os imports permitidos

```bash
grep -rnE '^ *(import|from) ' --include='*.py' ex0 ex1 alchemy *.py | sort
```

```text
alchemy/__init__.py:1:from .elements import create_air
alchemy/grimoire/__init__.py:1:from .light_spellbook import light_spell_record
alchemy/grimoire/dark_spellbook.py:1:from .dark_validator import validate_ingredients
alchemy/grimoire/dark_validator.py:1:from .dark_spellbook import dark_spell_allowed_ingredients
alchemy/grimoire/light_spellbook.py:1:from .light_validator import validate_ingredients
alchemy/grimoire/light_validator.py:2:    from .light_spellbook import light_spell_allowed_ingredients
alchemy/potions.py:1:from elements import create_fire, create_water
alchemy/potions.py:3:from .elements import create_air, create_earth
alchemy/transmutation/recipes.py:1:from alchemy.potions import strength_potion
alchemy/transmutation/recipes.py:2:from elements import create_fire
alchemy/transmutation/recipes.py:4:from ..elements import create_air
ex0/construct.py:1:import os
ex0/construct.py:2:import site
ex0/construct.py:3:import sys
ex0/loading.py:1:import importlib
ex1/oracle.py:1:import os
ex1/oracle.py:3:from dotenv import load_dotenv
ft_alembic_0.py:1:import elements
ft_alembic_1.py:1:import alchemy
ft_distillation_0.py:1:from alchemy.potions import healing_potion, strength_potion
ft_kaboom_0.py:1:from alchemy.grimoire import light_spell_record
ft_kaboom_1.py:5:    from alchemy.grimoire.dark_spellbook import dark_spell_record
ft_transmutation_0.py:1:import alchemy.transmutation.recipes
```

O `grep` procura em todos os arquivos `.py` (`-r` entra nas pastas, `--include` filtra os nomes)
as linhas que começam, depois de espaços, com `import ` ou `from ` (`-E` permite o `(a|b)`), e
mostra o arquivo e o número da linha (`-n`). O exercício 0 só importa `os`, `site`, `sys` e
`importlib` (a `pandas` e o `numpy` entram pelo `import_module`); o 1, `os` e `dotenv`; e os
exercícios 2 a 4, só `elements` e `alchemy`, os módulos do projeto.

## Nada de sys.path, eval ou exec

```bash
grep -rn -e "sys.path" -e "eval(" -e "exec(" --include='*.py' ex0 ex1 alchemy *.py
echo $?
```

```text
1
```

O `grep` não acha nenhuma linha, e o código de saída `1` é o jeito dele de dizer "nada
encontrado". Cada `-e` é um texto procurado.
