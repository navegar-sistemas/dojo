---
sidebar_position: 4
title: fullmatch e o limite de dígitos
---

# fullmatch e o limite de dígitos

A expressão regular `_INTEGER` da [página anterior](./02-inteiros-sem-surpresa.md) descreve a
forma de um inteiro aceito, mas ainda falta usá-la direito e tratar o caso dos textos gigantes,
que o `int()` recusa com uma mensagem enorme. Esta página escreve o método `to_int` do
`ValueParser`: a conferência do texto inteiro, o limite de dígitos e o que a exceção carrega.

## `fullmatch`: o texto inteiro

```python
if not _INTEGER.fullmatch(value):
    raise ValueError(value)
```

`_INTEGER.fullmatch(value)` confere o texto `value` com o padrão já preparado por `re.compile`. Ele
só aceita se o **texto inteiro** tiver a forma do padrão; quando não tem, devolve `None`, que
conta como falso, e o `not` transforma isso no caso de erro. Os outros dois métodos do `re`
aceitariam pedaços:

| Texto | `match` (só o começo) | `search` (em qualquer lugar) | `fullmatch` (tudo) |
|---|---|---|---|
| `20` | casa | casa | casa |
| `20abc` | casa | casa | **não casa** |
| `abc20` | não casa | casa | **não casa** |
| `2.5` | casa (o `2`) | casa | **não casa** |

Quando o texto não serve, o conversor levanta (lança) `ValueError(value)`, a exceção do Python
para "valor com formato errado".

## O limite de dígitos

`MAX_DIGITS` é um **atributo de classe**: uma variável escrita no corpo da classe, fora de
qualquer método. Ela pertence à classe, e não a um objeto, e se lê pelo nome da classe:
`ValueParser.MAX_DIGITS`.

```python
class ValueParser:
    ...

    # CPython refuses int() above 4300 digits; no valid value needs 19.
    MAX_DIGITS = 18
```

(O `...` marca a docstring da classe, omitida aqui.) Por ser uma constante, o nome vai em
maiúsculas.

CPython é o nome do Python "oficial", o que se instala do python.org. Ele se recusa a converter
textos com mais de 4300 dígitos ([página anterior](./02-inteiros-sem-surpresa.md)). Nenhum valor
válido chega perto disso: `WIDTH` e `HEIGHT` vão até 100, e uma `SEED` de 18 dígitos chega a quase
um quintilhão. O limite de 18 é escolha do projeto, bem abaixo dos 4300:

```python
if len(value.lstrip("+-").lstrip("0")) > ValueParser.MAX_DIGITS:
    raise OverflowError(value)
return int(value)
```

- `lstrip("+-")` tira o sinal do começo, e `lstrip("0")` tira os zeros à esquerda. O que sobra
  são os dígitos que contam: `000000000000000000000000000005` tem 30 caracteres, mas vale 5 e
  é aceito.
- A conta vem **antes** do `int()`: um texto de 100 000 dígitos nunca chega a ser convertido.
- A exceção é outra, `OverflowError` ("número grande demais"), para quem chama poder escrever
  uma mensagem curta, sem repetir o valor: `WIDTH has more than 18 digits`.

Chegando ao `int(value)`, o texto já tem só dígitos de 0 a 9, sem espaços, e é curto: o `int()`
só faz a conta.

## A exceção leva o texto, não a frase

`raise ValueError(value)` não diz "WIDTH must be an integer": o `ValueParser` não sabe qual chave
do arquivo está convertendo. Ele só diz "este texto não serve". Quem sabe a chave é o
`MazeConfig`, que captura a exceção e escreve a mensagem final
([parte 11](../11-configuracao/02-convertendo-um-valor.md)).

O arquivo completo do `ValueParser`, com o `to_int` montado, está no fim da
[página 6](./03-booleanos-e-coordenadas.md), junto com um exemplo que o roda. Antes, a
[próxima página](./07-booleanos.md) escreve o conversor de booleanos.
