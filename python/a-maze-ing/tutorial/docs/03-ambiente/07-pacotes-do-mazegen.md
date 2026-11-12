---
sidebar_position: 7
title: Os pacotes do mazegen
---

# Os pacotes do `mazegen`

## Pasta, módulo e pacote

- Um **módulo** é um arquivo `.py`: `mazegen/errors.py` é o módulo `mazegen.errors`.
- Um **pacote** é uma pasta com um arquivo `__init__.py`: `mazegen/` é o pacote `mazegen`, e
  `mazegen/entities/` é o pacote `mazegen.entities`.

O `__init__.py` é o código que roda na primeira vez que alguém importa o pacote. Ele pode estar
quase vazio: a presença dele já diz ao Python, ao mypy e ao setuptools "esta pasta é um pacote
do projeto".

Sem ele, o Python 3 ainda importa a pasta, como um *namespace package*: um recurso feito para
espalhar um único pacote por várias pastas instaladas, que não é o caso aqui. O projeto declara
todo pacote de forma explícita, com o `__init__.py`.

## Uma docstring por pacote

Todo módulo do projeto começa com uma docstring, inclusive os `__init__.py`. Nas subpastas, ela
é uma frase que diz o que o pacote guarda, e não há mais nada no arquivo: as classes são
importadas pelo caminho completo (`from mazegen.entities.maze import Maze`), nunca pelo
`__init__.py` da subpasta.

## Criando as pastas

```bash
mkdir -p mazegen/entities mazegen/value_objects mazegen/services
```

```python title="mazegen/entities/__init__.py"
"""Mutable entities of the maze generator."""
```

Entidades: objetos que mudam de estado. Só o `Maze` (parte 5).

```python title="mazegen/value_objects/__init__.py"
"""Immutable value objects of the maze generator."""
```

Value objects: valores imutáveis. `Direction`, `Cell` e `Pattern42` (parte 4).

```python title="mazegen/services/__init__.py"
"""Stateless services that carve, braid and solve a maze."""
```

Services: operações sem estado. `Carver`, `Solver` e `Braider` (partes 6, 7 e 8).

## O `mazegen/__init__.py`, por enquanto

O `__init__.py` da raiz do pacote é diferente: ele vira a documentação do módulo e exporta
`MazeGenerator` e `MazeError`. Ainda não existe gerador para exportar, então ele começa só com o
resumo de uma linha:

```python
"""Generate random mazes with a "42" drawn by fully closed cells."""
```

A versão completa, com a documentação e os imports, é escrita na parte 9.

## `py.typed`

```bash
touch mazegen/py.typed
```

Um arquivo **vazio**, definido pela PEP 561. Quando outro projeto instala o `mazegen` e roda o
mypy, o mypy só lê as anotações de tipo de um pacote instalado se encontrar esse marcador. Sem
ele, o mypy do outro projeto trata o `mazegen` como uma biblioteca sem tipos e reclama:

```text
error: Skipping analyzing "mazegen": module is installed, but missing library stubs or py.typed marker  [import-untyped]
```

O `pyproject.toml` já inclui o `py.typed` no wheel (`[tool.setuptools.package-data]`).

## Como fica

```text
mazegen/
    __init__.py
    py.typed
    entities/
        __init__.py
    value_objects/
        __init__.py
    services/
        __init__.py
```
