---
sidebar_position: 3
title: Booleanos e coordenadas
---

# Booleanos e coordenadas

Os outros dois conversores do `ValueParser`: `to_bool`, para `PERFECT`, e `to_coordinate`, para
`ENTRY` e `EXIT`.

## `to_bool`: `True` ou `False`, em qualquer caixa

```python
lowered = value.lower()
if lowered == "true":
    return True
if lowered == "false":
    return False
raise ValueError(value)
```

O subject usa `PERFECT=True` no exemplo, e é natural alguém escrever `true` ou `TRUE`. Passar
tudo para minúsculas antes de comparar aceita qualquer caixa com duas comparações.

O que **não** é aceito: `yes`, `1`, `sim`, `on`. Cada um desses é uma convenção de outro
programa; aceitar uma e recusar outra seria arbitrário, e aceitar todas transformaria o
conversor numa lista sem fim. `True` e `False` são as palavras do subject e do próprio Python.

### Por que não `bool(value)`

`bool("False")` é `True`: em Python, toda string não vazia é verdadeira. É o erro clássico de
converter booleano a partir de texto.

## `to_coordinate`: `x,y`

```python
parts = value.split(",")
if len(parts) != 2:
    raise ValueError(value)
return (ValueParser.to_int(parts[0]), ValueParser.to_int(parts[1]))
```

1. `split(",")` corta o texto em cada vírgula. `0,0` dá duas partes; `0` dá uma; `0,0,0` dá três.
2. Qualquer quantidade diferente de duas é erro de formato.
3. Cada parte passa por `to_int`, com todas as regras da página anterior: ASCII, sem espaços,
   até 18 dígitos.

O resultado é a tupla `(x, y)`, coluna e linha, na convenção de todo o projeto.

| Texto | Resultado | Motivo |
|---|---|---|
| `0,0` | `(0, 0)` | |
| `19,14` | `(19, 14)` | |
| `-1,0` | `(-1, 0)` | formato válido; a posição fora da grade é acusada depois, pelo `MazeConfig` |
| `0, 0` | `ValueError` | a segunda parte é ` 0`, com espaço, e `to_int` recusa |
| `0;0` | `ValueError` | sem vírgula: uma parte só |
| `0,0,0` | `ValueError` | três partes |
| `(0,0)` | `ValueError` | `(0` não é inteiro |

O `-1,0` mostra a divisão de trabalho: o `ValueParser` só confere o **formato**. Se a coordenada
cabe na grade depende de `WIDTH` e `HEIGHT`, que ele não conhece.

### Por que `to_coordinate` não captura o `OverflowError`

Se uma das partes tiver dígitos demais, `to_int` levanta `OverflowError`, e ele passa direto por
`to_coordinate` até o `MazeConfig`. Não há nada a fazer aqui: a mensagem certa
(`ENTRY has more than 18 digits`) é montada por quem conhece a chave.

## Por que uma classe e não funções soltas

Três funções no nível do módulo funcionariam igual. A classe agrupa os conversores e a constante
`MAX_DIGITS` sob um nome só, e quem lê `ValueParser.to_int(...)` sabe de onde a função vem sem
procurar o `import`. Os métodos são `@staticmethod` porque não precisam de instância nem de
estado: ninguém escreve `ValueParser()`.

## Experimente

```bash
.venv/bin/python -c '
from amazeing.utils.value_parser import ValueParser

for text in ["0,0", "19,14", "-1,0", "0, 0", "0;0", "0,0,0", "(0,0)"]:
    try:
        print(repr(text), "->", ValueParser.to_coordinate(text))
    except ValueError as error:
        print(repr(text), "->", type(error).__name__)
'
```

```text
'0,0' -> (0, 0)
'19,14' -> (19, 14)
'-1,0' -> (-1, 0)
'0, 0' -> ValueError
'0;0' -> ValueError
'0,0,0' -> ValueError
'(0,0)' -> ValueError
```

## O arquivo completo

```python title="amazeing/utils/value_parser.py"
"""Strict parsers for the values of the configuration file."""

import re

_INTEGER = re.compile(r"[+-]?[0-9]+")


class ValueParser:
    """Convert configuration text into integers, booleans and coordinates.

    Attributes:
        MAX_DIGITS: Most significant digits accepted in an integer.
    """

    # CPython refuses int() above 4300 digits; no valid value needs 19.
    MAX_DIGITS = 18

    @staticmethod
    def to_int(value: str) -> int:
        """Parse an ASCII integer with an optional sign.

        Args:
            value: Text such as "20", "-3" or "+007".

        Returns:
            The integer.

        Raises:
            ValueError: The text is not [+-]?[0-9]+.
            OverflowError: The integer has more than MAX_DIGITS significant
                digits.
        """
        if not _INTEGER.fullmatch(value):
            raise ValueError(value)
        if len(value.lstrip("+-").lstrip("0")) > ValueParser.MAX_DIGITS:
            raise OverflowError(value)
        return int(value)

    @staticmethod
    def to_bool(value: str) -> bool:
        """Parse true or false in any case.

        Args:
            value: Text such as "True" or "false".

        Returns:
            The boolean.

        Raises:
            ValueError: The text is neither true nor false.
        """
        lowered = value.lower()
        if lowered == "true":
            return True
        if lowered == "false":
            return False
        raise ValueError(value)

    @staticmethod
    def to_coordinate(value: str) -> tuple[int, int]:
        """Parse "x,y" with two integers and no spaces.

        Args:
            value: Text such as "0,0" or "19,14".

        Returns:
            The pair (x, y).

        Raises:
            ValueError: The text is not two integers separated by a comma.
            OverflowError: One of the integers has more than MAX_DIGITS
                significant digits.
        """
        parts = value.split(",")
        if len(parts) != 2:
            raise ValueError(value)
        return (ValueParser.to_int(parts[0]), ValueParser.to_int(parts[1]))
```
