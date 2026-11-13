---
sidebar_position: 1
title: Conferir tudo
---

# Conferir tudo

Rode tudo a partir da pasta `the-matrix`, sem nenhum ambiente ativado.

## Os arquivos

```bash
LC_ALL=C ls -1A ex0 ex1 ex2
```

```text
ex0:
.mypy_cache
construct.py
matrix_env

ex1:
.mypy_cache
loading.py
matrix_analysis.png
matrix_env
poetry.lock
pyproject.toml
requirements.txt

ex2:
.env
.env.example
.gitignore
.mypy_cache
matrix_env
oracle.py
requirements.txt
```

O `-A` mostra também os nomes que começam com ponto (o `-a` mostraria ainda `.` e `..`, a
própria pasta e a de cima), e o `-1` põe um nome por linha. `LC_ALL=C` faz o `ls` ordenar os nomes
pelo valor de cada caractere, com os que começam com ponto primeiro; sem ele, no Linux, a ordem
segue o idioma do sistema e pode misturar os nomes com ponto aos outros. Os arquivos de entrega,
com os nomes exatos do enunciado:

| Pasta | Entregar | Fica de fora |
|---|---|---|
| `ex0` | `construct.py` | `matrix_env`, `.mypy_cache` |
| `ex1` | `loading.py`, `requirements.txt`, `pyproject.toml` | `matrix_env`, `.mypy_cache`, `poetry.lock`, `matrix_analysis.png` |
| `ex2` | `oracle.py`, `requirements.txt`, `.env.example`, `.gitignore` | `matrix_env`, `.mypy_cache`, `.env` |

Os ambientes virtuais ficam de fora porque o enunciado manda: cada um é recriado com
`python3 -m venv` e o arquivo de dependências
([Recriar tudo a partir do repositório](./03-perguntas-de-revisao.md#recriar-tudo-a-partir-do-repositório)).
O `poetry.lock` e o `matrix_analysis.png` são gerados pelo `poetry install` e
pelo programa, e não estão na lista de arquivos a entregar. O `.env` guarda o segredo.

## Estilo e tipos

As ferramentas recebem os arquivos um a um: com as pastas, o flake8 entraria nos ambientes
virtuais (`matrix_env`) e conferiria o código das bibliotecas instaladas.

```bash
.venv/bin/flake8 ex0/construct.py ex1/loading.py ex2/oracle.py
.venv/bin/mypy --disallow-untyped-defs --python-executable ex2/matrix_env/bin/python ex0/construct.py ex1/loading.py ex2/oracle.py
```

```text
Success: no issues found in 3 source files
```

O flake8 não imprime nada. O mypy confere os três arquivos de uma vez. O `oracle.py` importa o
python-dotenv, e o mypy precisa enxergar a biblioteca para conferir o uso dela; sem
`--python-executable`, ele a procuraria no `.venv` das ferramentas, onde ela não está, e acusaria
`import-not-found`. A opção aponta para o Python do ambiente do exercício 2, o único que o mypy
precisa enxergar: o `construct.py` só usa a biblioteca padrão, e o `loading.py` não tem `import`
de biblioteca externa
([Conferir estilo e tipos do exercício 2](../05-ex2/10-rodar-e-conferir.md#conferir-estilo-e-tipos)).

Os experimentos também estão limpos:

```bash
.venv/bin/flake8 experimentos
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
Success: no issues found in 4 source files
```

## Só os imports permitidos

```bash
grep -n "import" ex0/construct.py ex1/loading.py ex2/oracle.py
```

```text
ex0/construct.py:1:import os
ex0/construct.py:2:import site
ex0/construct.py:3:import sys
ex1/loading.py:1:import importlib
ex1/loading.py:2:import sys
ex1/loading.py:17:            module = importlib.import_module(name)
ex1/loading.py:41:    np = importlib.import_module("numpy")
ex1/loading.py:42:    pd = importlib.import_module("pandas")
ex1/loading.py:43:    matplotlib = importlib.import_module("matplotlib")
ex1/loading.py:45:    plt = importlib.import_module("matplotlib.pyplot")
ex2/oracle.py:1:import os
ex2/oracle.py:2:import sys
ex2/oracle.py:5:    from dotenv import dotenv_values, load_dotenv
```

O `grep` mostra cada linha com a palavra `import`, com o arquivo e o número da linha (`-n`). Cada
exercício usa só os módulos da sua lista: `os`, `site` e `sys` no 0; `importlib`, `sys`, numpy,
pandas e matplotlib no 1; `os`, `sys` e `dotenv` (o python-dotenv) no 2.

## As situações de cada programa

As páginas de rodar e conferir de cada exercício rodam os programas em todos os ambientes que o
enunciado pede: [exercício 0](../03-ex0/07-rodar-e-conferir.md) (fora do venv, dentro com e sem
ativação), [exercício 1](../04-ex1/12-rodar-e-conferir.md#resumo-das-situações) (sem as
bibliotecas, com parte, com o pip, com o Poetry) e [exercício 2](../05-ex2/10-rodar-e-conferir.md)
(sem o python-dotenv, sem configuração, desenvolvimento, produção). Os `diff` dessas páginas que
comparam com o enunciado continuam mostrando só as diferenças explicadas lá.
