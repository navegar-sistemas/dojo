---
sidebar_position: 2
title: Os dois elements.py
---

# Os dois elements.py

Os quatro elementos fundamentais ficam em dois módulos: fogo e água à mão, na raiz; terra e ar
dentro do pacote `alchemy`. Cada função só devolve uma frase fixa, como o enunciado pede para os
exercícios 2 a 4: o assunto é o caminho até elas.

## Na raiz

Na pasta `the-codex`, crie `elements.py`:

```python title="elements.py"
def create_fire() -> str:
    return "Fire element created"


def create_water() -> str:
    return "Water element created"
```

## No pacote

Crie a pasta do pacote:

```bash
mkdir alchemy
```

E dentro dela, `alchemy/elements.py`:

```python title="alchemy/elements.py"
def create_earth() -> str:
    return "Earth element created"


def create_air() -> str:
    return "Air element created"
```

A pasta `alchemy` só vira pacote com o `__init__.py`, na [próxima página](./03-o-init-de-alchemy.md).
As frases dos quatro elementos são as do enunciado, letra por letra; os exercícios 3 e 4 as
montam em frases maiores, e as saídas esperadas dependem delas.
