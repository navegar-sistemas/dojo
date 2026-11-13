---
sidebar_position: 6
title: Coordenadas e o arquivo completo
---

# Coordenadas e o arquivo completo

`ENTRY=0,0` e `EXIT=19,14` dão a célula de entrada e a de saída. Chegam ao programa como texto
e precisam virar um par de números, a coluna `x` e a linha `y`. Esta página mostra o último
conversor do `ValueParser`, `to_coordinate`, e o arquivo completo da classe, com os
conversores das páginas [3](./02-inteiros-sem-surpresa.md),
[4](./06-fullmatch-e-limite-de-digitos.md) e [5](./07-booleanos.md).

## `to_coordinate`: `x,y`

Uma coordenada é o endereço de uma célula: `x` é a coluna (posição na horizontal) e `y` é a
linha (posição na vertical), os dois contando de 0 a partir do canto de cima à esquerda
([parte 1](../01-o-problema/01-a-grade-e-as-celulas.md)). No arquivo, ela vem como dois inteiros
separados por vírgula.

```python
parts = value.split(",")
if len(parts) != 2:
    raise ValueError(value)
return (ValueParser.to_int(parts[0]), ValueParser.to_int(parts[1]))
```

1. `split(",")` corta o texto em cada vírgula e devolve a lista dos pedaços.
2. Qualquer quantidade de pedaços diferente de duas é erro de formato.
3. Cada pedaço passa pelo `to_int`, com todas as regras das páginas 3 e 4: só dígitos de 0 a
   9, sem espaços, até 18 dígitos.
4. O resultado é a **tupla** `(x, y)`: um par de valores entre parênteses, que não pode ser
   alterado depois de criado.

O que o `split` devolve em cada caso:

| Texto | `split(",")` | Resultado | Motivo |
|---|---|---|---|
| `0,0` | `['0', '0']` | `(0, 0)` | |
| `19,14` | `['19', '14']` | `(19, 14)` | |
| `-1,0` | `['-1', '0']` | `(-1, 0)` | formato válido; a posição fora da grade é recusada depois |
| `0, 0` | `['0', ' 0']` | `ValueError` | o segundo pedaço tem um espaço, e o `to_int` recusa |
| `0;0` | `['0;0']` | `ValueError` | sem vírgula: um pedaço só |
| `0,0,0` | `['0', '0', '0']` | `ValueError` | três pedaços |
| `(0,0)` | `['(0', '0)']` | `ValueError` | `(0` não é um inteiro |

O `-1,0` mostra a divisão de trabalho: o `ValueParser` só confere o **formato** do texto. Se a
célula existe na grade depende da largura e da altura, que ele não conhece. Quem confere é o
`MazeConfig`, que tem todos os valores
([parte 11](../11-configuracao/03-a-ordem-das-validacoes.md)).

### O `OverflowError` passa direto

Se um dos pedaços tiver dígitos demais, o `to_int` levanta `OverflowError`, e o `to_coordinate`
não o captura: a exceção sobe até o `MazeConfig`. Não há o que fazer aqui, porque a mensagem
certa (`ENTRY has more than 18 digits`) precisa do nome da chave, que só o `MazeConfig` sabe.

## Por que uma classe e não funções soltas

Três funções no nível do arquivo funcionariam igual. A classe junta os conversores e a constante
`MAX_DIGITS` sob um nome só: quem lê `ValueParser.to_int(...)` sabe de onde a função vem sem
procurar o `import`. Os métodos são `@staticmethod` porque não usam nenhum dado de um objeto:
ninguém precisa escrever `ValueParser()`.

## O arquivo completo

As docstrings seguem o **estilo Google**: depois da descrição, as seções `Args:` (os
parâmetros), `Returns:` (o que a função devolve) e `Raises:` (as exceções que ela pode levantar).
`tuple[int, int]` na assinatura quer dizer "tupla de dois inteiros".

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

## Experimente

Com o arquivo completo, os três conversores rodam. Na raiz do projeto, primeiro o `to_int`, com
os casos das [páginas 3](./02-inteiros-sem-surpresa.md) e
[4](./06-fullmatch-e-limite-de-digitos.md):

```bash
.venv/bin/python - <<'EOF'
from amazeing.utils.value_parser import ValueParser

for text in ["20", "-3", "+007", "1_0", " 5", "２０", "2.5", "9" * 19]:
    try:
        print(repr(text), "->", ValueParser.to_int(text))
    except (ValueError, OverflowError) as error:
        print(repr(text), "->", type(error).__name__)
EOF
```

```text
'20' -> 20
'-3' -> -3
'+007' -> 7
'1_0' -> ValueError
' 5' -> ValueError
'２０' -> ValueError
'2.5' -> ValueError
'9999999999999999999' -> OverflowError
```

- `"9" * 19` repete o texto `"9"` 19 vezes: um número de 19 dígitos, um a mais que o limite.
- `except (ValueError, OverflowError) as error` captura qualquer uma das duas exceções (a tupla
  entre parênteses), e `type(error).__name__` é o nome da classe da exceção capturada, como texto.

Depois o `to_bool`:

```bash
.venv/bin/python - <<'EOF'
from amazeing.utils.value_parser import ValueParser

for text in ["True", "false", "TRUE", "yes", "1"]:
    try:
        print(repr(text), "->", ValueParser.to_bool(text))
    except ValueError as error:
        print(repr(text), "->", type(error).__name__)
EOF
```

```text
'True' -> True
'false' -> False
'TRUE' -> True
'yes' -> ValueError
'1' -> ValueError
```

E o `to_coordinate`, com os casos da tabela acima:

```bash
.venv/bin/python - <<'EOF'
from amazeing.utils.value_parser import ValueParser

for text in ["0,0", "19,14", "-1,0", "0, 0", "0;0", "0,0,0", "(0,0)"]:
    try:
        print(repr(text), "->", ValueParser.to_coordinate(text))
    except ValueError as error:
        print(repr(text), "->", type(error).__name__)
EOF
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
