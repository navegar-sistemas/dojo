---
sidebar_position: 8
title: Os pacotes do amazeing
---

# Os pacotes do `amazeing`

## Uma pasta por camada

A aplicação tem uma subpasta para cada papel da parte 2, e cada uma é um pacote com o seu
`__init__.py`:

```bash
mkdir -p amazeing/domain/entities amazeing/domain/value_objects amazeing/use_cases \
    amazeing/repositories amazeing/services amazeing/ui amazeing/utils
```

Como no `mazegen`, cada `__init__.py` tem só uma docstring de uma frase.

```python title="amazeing/__init__.py"
"""A-Maze-ing application built on top of the mazegen package."""
```

A raiz da aplicação. Ela guarda também o `errors.py` (parte 10).

```python title="amazeing/domain/__init__.py"
"""Domain layer of the application."""
```

O domínio da aplicação: os conceitos do programa, sem arquivo e sem terminal.

```python title="amazeing/domain/entities/__init__.py"
"""Mutable entities of the application domain."""
```

`ViewState`, o estado da sessão do menu (parte 13).

```python title="amazeing/domain/value_objects/__init__.py"
"""Immutable value objects of the application domain."""
```

`MazeConfig` (parte 11) e `GeneratedMaze` (parte 12).

```python title="amazeing/use_cases/__init__.py"
"""Application use cases and the ports they depend on."""
```

`GenerateMaze` e a porta `MazeRepository` (parte 12).

```python title="amazeing/repositories/__init__.py"
"""Repositories that read and write files."""
```

`FileConfigRepository` (parte 11) e `FileMazeRepository` (parte 12), os únicos que abrem
arquivos.

```python title="amazeing/services/__init__.py"
"""Stateless application services."""
```

`RenderService`, que transforma um labirinto em texto colorido (parte 13).

```python title="amazeing/ui/__init__.py"
"""Terminal user interface."""
```

`Menu` (parte 14), o único que usa `print` e `input`.

```python title="amazeing/utils/__init__.py"
"""Stateless helpers shared by the application layers."""
```

`ValueParser` e `Ansi` (parte 10).

## O esqueleto completo

```text
.flake8
.gitignore
Makefile
config.txt
pyproject.toml
mazegen/
    __init__.py
    py.typed
    entities/__init__.py
    value_objects/__init__.py
    services/__init__.py
amazeing/
    __init__.py
    domain/__init__.py
    domain/entities/__init__.py
    domain/value_objects/__init__.py
    use_cases/__init__.py
    repositories/__init__.py
    services/__init__.py
    ui/__init__.py
    utils/__init__.py
```

## Experimente

O esqueleto ainda não faz nada, mas já passa no lint:

```bash
make install
make lint-strict
```

```text
.venv/bin/python -m flake8 .
.venv/bin/python -m mypy . --strict
Success: no issues found in 13 source files
```

O flake8 não imprime nada quando não encontra problema. Os 13 arquivos do mypy são os 13
`__init__.py`. A partir daqui, toda peça nova entra num projeto que já está limpo, e o
`make lint-strict` continua sem nenhuma linha de erro a cada arquivo acrescentado.
