---
sidebar_position: 3
title: Any, união e isinstance
---

# Any, união e isinstance

Os processadores do projeto recebem dados de qualquer tipo e precisam descobrir, enquanto o
programa roda, se o dado serve. Três ferramentas fazem isso: o type hint `Any`, o type hint de
**união** (`int | float`) e a função `isinstance`.

## Any: qualquer tipo

`Any` vem do módulo `typing`, o segundo `import` permitido. Como type hint, quer dizer "qualquer
tipo":

```python
from typing import Any


def show(value: Any) -> None:
    print(value)
```

`show(42)`, `show("abc")` e `show([1, 2])` são todas aceitas pelo mypy. O mypy também não
confere o que o código faz com um valor `Any`: ele confia. O enunciado usa `Any` no parâmetro de
`validate`, porque esse método existe justamente para receber qualquer coisa e responder se ela
serve.

O enunciado às vezes escreve `typing.Any` (com `import typing`) e às vezes só `Any` (com
`from typing import Any`): é o mesmo objeto, escrito de dois jeitos. O tutorial usa
`from typing import Any`.

## União: um tipo ou outro

`int | float` quer dizer "um `int` **ou** um `float`". A barra `|` junta tipos numa **união**.
Combinada com os tipos de coleção:

| Type hint | Aceita |
|---|---|
| `int \| float` | `42` ou `3.14` |
| `list[int \| float]` | uma lista em que cada item é `int` ou `float`, como `[3.14, -1, 2]` |
| `str \| list[str]` | um texto, ou uma lista de textos |
| `dict[str, str]` | um dicionário com chaves `str` e valores `str` |
| `tuple[int, str]` | uma tupla de dois itens: um `int` e depois um `str` |

A barra entre tipos funciona a partir do Python 3.10, a versão mínima do enunciado.

## isinstance: o tipo enquanto o programa roda

`isinstance(valor, tipo)` devolve `True` se o valor é daquele tipo (ou de um tipo filho dele) e
`False` se não é. Com uma tupla de tipos, responde se o valor é de **algum** deles:
`isinstance(3.14, (int, float))` dá `True`.

Crie `experimentos/tipos.py`:

```python title="experimentos/tipos.py"
from typing import Any


def describe(value: Any) -> str:
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "text"
    if isinstance(value, list):
        return "list"
    return "something else"


for value in [42, 3.14, "42", [1, 2], {"a": "b"}, True]:
    print(f"{value!r}: {describe(value)}")
print(f"isinstance(True, int): {isinstance(True, int)}")
```

O `!r` dentro das chaves mostra o valor como ele seria escrito no código: um texto aparece entre
aspas (`'42'`), e assim dá para distinguir o texto `"42"` do número `42`.

```bash
python3 experimentos/tipos.py
```

```text
42: number
3.14: number
'42': text
[1, 2]: list
{'a': 'b'}: something else
True: bool
isinstance(True, int): True
```

## A armadilha do bool

A última linha diz que `True` **é** um `int`. No Python, `bool` é uma classe filha de `int`:
`True` vale `1` e `False` vale `0` em contas. Por isso `describe` testa `bool` **antes** de
`(int, float)`: na ordem contrária, `True` cairia em `"number"`.

No projeto, o processador de números recusa `True` e `False`: um valor verdadeiro ou falso não é
uma medida numérica. Essa é uma escolha do tutorial; o enunciado não fala de `bool`
([Numeric Processor](../03-ex0/03-numeric-processor.md)).

## A lista de int não é uma lista de int | float \{#lista-invariante}

Crie `experimentos/uniao.py`:

```python title="experimentos/uniao.py"
def total(values: list[int | float]) -> float:
    result = 0.0
    for value in values:
        result += value
    return result


mixed: list[int | float] = [1, 2.5]
ints = [1, 2, 3]
print(total(mixed))
print(total(ints))
```

```bash
python3 experimentos/uniao.py
```

```text
3.5
6.0
```

O programa roda: o Python não confere type hints. Mas o mypy recusa a última chamada:

```bash
.venv/bin/mypy --disallow-untyped-defs experimentos/uniao.py
```

```text
experimentos/uniao.py:11: error: Argument 1 to "total" has incompatible type "list[int]"; expected "list[int | float]"  [arg-type]
experimentos/uniao.py:11: note: "list" is invariant -- see https://mypy.readthedocs.io/en/stable/common_issues.html#variance
experimentos/uniao.py:11: note: Consider using "Sequence" instead, which is covariant
Found 1 error in 1 file (checked 1 source file)
```

Sem anotação, o mypy deduz o tipo de `ints` pelo valor: `list[int]`, uma lista **só de
inteiros**. Uma função que recebe `list[int | float]` tem o direito de acrescentar um `3.5` na
lista; se ela recebesse `ints`, a lista "só de inteiros" ganharia um `float`. Por isso o mypy não
aceita uma `list[int]` onde se pede `list[int | float]` (é isso que *invariant* quer dizer: o tipo
dos itens tem de ser exatamente o pedido).

A variável `mixed` passa porque foi **anotada** como `list[int | float]`. A solução é anotar
`ints` do mesmo jeito. O arquivo fica assim:

```python title="experimentos/uniao.py"
def total(values: list[int | float]) -> float:
    result = 0.0
    for value in values:
        result += value
    return result


mixed: list[int | float] = [1, 2.5]
ints: list[int | float] = [1, 2, 3]
print(total(mixed))
print(total(ints))
```

```bash
.venv/bin/mypy --disallow-untyped-defs experimentos/uniao.py
```

```text
Success: no issues found in 1 source file
```

O projeto usa a mesma solução: anotar a variável com o tipo que a função pede
([A demonstração](../03-ex0/07-a-demonstracao.md)). A nota sobre `Sequence` sugere outro tipo de
type hint, que o projeto não precisa.
