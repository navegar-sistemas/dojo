---
sidebar_position: 2
title: Inteiros sem surpresa
---

# Inteiros sem surpresa

O `ValueParser` (`amazeing/utils/value_parser.py`) converte o texto de um valor do config no tipo
que ele representa: inteiro, booleano ou coordenada. Ele é uma classe **utilitária**: só métodos
`@staticmethod` e constantes, sem estado. Quem o usa é o `MazeConfig` (parte 11).

O primeiro conversor é `to_int`, usado por `WIDTH`, `HEIGHT`, `SEED` e pelas duas metades de uma
coordenada.

## Por que não usar `int()` direto

`int(texto)` parece suficiente, mas aceita coisas que nenhuma pessoa escreveria num config de
propósito:

```bash
.venv/bin/python -c '
for v in ["1_0", " 5", "٢٠", "２０", "+7", "007"]:
    print(repr(v), "->", int(v))
'
```

```text
'1_0' -> 10
' 5' -> 5
'٢٠' -> 20
'２０' -> 20
'+7' -> 7
'007' -> 7
```

| Texto | O que `int()` faz | Problema |
|---|---|---|
| `1_0` | lê 10 | o `_` é separador de milhar do Python, não de um arquivo de config |
| ` 5` | lê 5 | ignora espaços em volta; a coordenada `0, 0` passaria, e o formato pede `x,y` sem espaços |
| `٢٠`, `２０` | lê 20 | aceita dígitos de outros alfabetos (árabe, largura dupla) |
| `+7`, `007` | lê 7 | inofensivos; esses ficam aceitos |

E há o caso extremo: o CPython se recusa a converter textos com mais de 4300 dígitos, para não
travar numa conversão gigante.

```text
Exceeds the limit (4300 digits) for integer string conversion: value has 5000 digits; use sys.set_int_max_str_digits() to increase the limit
```

Esse erro é um `ValueError`, e a mensagem ao usuário citaria o valor inteiro entre aspas: uma
linha de erro com 5000 caracteres.

## A regra: uma expressão regular

```python
_INTEGER = re.compile(r"[+-]?[0-9]+")
```

| Pedaço | Significa |
|---|---|
| `[+-]?` | um sinal opcional |
| `[0-9]+` | um ou mais dígitos, só os ASCII de `0` a `9` |

A classe `[0-9]` lista os dez caracteres exatos. O atalho `\d` não serviria: em Python ele casa
com qualquer dígito Unicode, inclusive `٢` e `２`.

A expressão é compilada uma vez, como constante do módulo, e não a cada chamada. O `_` no nome
diz que ela é interna ao arquivo.

```python
if not _INTEGER.fullmatch(value):
    raise ValueError(value)
```

`fullmatch` exige que **o texto inteiro** case com a expressão. Com `match`, `20abc` passaria,
porque o começo casa; com `search`, até `abc20` passaria.

## O limite de dígitos

```python
# CPython refuses int() above 4300 digits; no valid value needs 19.
MAX_DIGITS = 18
```

Nenhum valor válido do config chega perto: `WIDTH` e `HEIGHT` vão até 100, e uma `SEED` de 18
dígitos já é maior do que qualquer pessoa digitaria. O limite fica bem abaixo dos 4300 do CPython
e corta o problema antes de ele existir.

```python
if len(value.lstrip("+-").lstrip("0")) > ValueParser.MAX_DIGITS:
    raise OverflowError(value)
return int(value)
```

- `lstrip("+-")` tira o sinal e `lstrip("0")` tira os zeros à esquerda: o que sobra são os
  dígitos **significativos**. `000000000000000000000000000005` tem 30 caracteres mas vale 5, e é
  aceito.
- O teste vem **antes** do `int()`: um texto de 100 000 dígitos nunca chega a ser convertido.
- A exceção é outra, `OverflowError`, para quem chama poder montar uma mensagem diferente
  (`WIDTH has more than 18 digits`), curta, sem repetir o valor.

Chegando ao `int(value)`, o texto já é ASCII, sem espaços e curto: `int()` agora só faz a conta.

## A exceção leva o texto, não a frase

`raise ValueError(value)` não escreve "WIDTH must be an integer": o `ValueParser` não sabe qual
chave está convertendo. Ele só diz "este texto não serve". Quem conhece a chave é o `MazeConfig`,
que captura a exceção e escreve a mensagem final.

## Experimente

```bash
.venv/bin/python -c '
from amazeing.utils.value_parser import ValueParser

for text in ["20", "-3", "+007", "1_0", " 5", "２０", "2.5", "9" * 19]:
    try:
        print(repr(text), "->", ValueParser.to_int(text))
    except (ValueError, OverflowError) as error:
        print(repr(text), "->", type(error).__name__)
'
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

O arquivo completo do `ValueParser` está na [próxima página](./03-booleanos-e-coordenadas.md).
