---
sidebar_position: 2
title: Pré-requisitos
---

# Pré-requisitos

## Python 3.10 ou mais novo

O subject exige Python 3.10 ou posterior. Confira:

```bash
python3 --version
```

O código usa recursos que só existem a partir do 3.10, como `X | None` nas anotações de tipo e
`@dataclass(slots=True)`.

## O que você precisa saber de Python

- classes, métodos e `@property`;
- `dataclass` e `Enum`;
- listas, dicionários, conjuntos (`set`) e tuplas;
- `try`/`except` e `with open(...)`;
- anotações de tipo (`def f(x: int) -> str:`).

Os conceitos menos comuns, como `typing.Protocol`, `IntEnum`, `frozen=True` e busca em largura,
são explicados na página em que aparecem.

## Ferramentas

| Ferramenta | Para quê |
|---|---|
| `python3 -m venv` | ambiente virtual isolado, criado pelo `make install` |
| `make` | atalhos para instalar, rodar, limpar, verificar e empacotar |
| `flake8` | estilo de código (PEP 8), exigido pelo subject |
| `mypy` | verificação de tipos, exigida pelo subject |
| `build` | gera o pacote `mazegen-1.0.0-py3-none-any.whl` |

`flake8`, `mypy` e `build` são instalados dentro do ambiente virtual pelo `Makefile`; não é
preciso instalar nada globalmente.

## A pasta do projeto

Todo o código vive numa pasta só, que vira a raiz do repositório entregue. Neste tutorial ela é
chamada de **raiz do projeto**, e todo caminho de arquivo (`mazegen/errors.py`,
`amazeing/ui/menu.py`) é relativo a ela.
