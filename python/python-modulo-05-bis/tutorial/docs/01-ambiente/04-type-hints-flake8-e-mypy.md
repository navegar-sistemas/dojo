---
sidebar_position: 4
title: Type hints, flake8 e mypy
---

# Type hints, flake8 e mypy

O enunciado pede duas conferências no código: o **estilo**, pelo flake8, e os **tipos**, pelo
mypy. Um arquivo de experimento com um defeito de cada tipo mostra o que cada uma acusa.

## Type hints

Um **type hint** (dica de tipo) anota o tipo de cada parâmetro e do valor devolvido:

```python
def double(number: int) -> int:
    return number * 2
```

- `number: int` diz que o parâmetro `number` é um inteiro;
- `-> int` diz que a função devolve um inteiro;
- uma função que não devolve nada leva `-> None`.

O Python **não** confere essas anotações quando roda o programa; elas servem para quem lê e para
o mypy. O enunciado exige type hints em **todo** o código: os parâmetros e o retorno de todas as
funções. As variáveis podem ficar sem anotação quando o mypy consegue deduzir o tipo pelo valor
(`count = 0` é um `int`); quando ele não consegue, a variável também é anotada, como em
`missing: list[str] = []` (uma lista vazia não diz de que são os itens).

Os type hints do projeto:

| Type hint | Quer dizer |
|---|---|
| `str`, `int`, `bool` | um texto, um inteiro, `True` ou `False` |
| `list[str]` | uma lista de textos |
| `dict[str, str]` | um dicionário com chaves e valores `str` |
| `str \| None` | um texto **ou** `None`; a barra junta dois tipos, e funciona a partir do Python 3.10 |

## Um arquivo com dois problemas

Crie `experimentos/estilo.py`:

```python title="experimentos/estilo.py"
def double(number: int) -> int:
    return number * 2
def triple(number):
    return number * 3
```

Ele tem dois defeitos: faltam as linhas em branco entre as funções, e `triple` não tem type hints.

## O flake8

```bash
.venv/bin/flake8 experimentos
```

```text
experimentos/estilo.py:3:1: E302 expected 2 blank lines, found 0
```

Cada aviso diz o arquivo, a linha, a coluna, um código e a explicação: na linha 3, o estilo
padrão do Python (chamado **PEP 8**) pede **duas linhas em branco entre** as funções de um
arquivo (não antes da primeira), e entre `double` e `triple` não havia nenhuma. Sem aviso nenhum,
o flake8 não imprime nada.

O flake8 recebe as pastas e os arquivos a conferir. Nunca rode `flake8 .` (o ponto é "a pasta
atual"): ele entraria também nas pastas dos ambientes virtuais e acusaria milhares de avisos no
código das bibliotecas instaladas.

## O mypy

O mypy, rodado sem opções, só confere as funções que **têm** type hints; uma função sem nenhuma
anotação passa calada. Para que ele também acuse a **falta** de type hints, que é o que o
enunciado exige, use a opção `--disallow-untyped-defs` ("não aceite funções sem tipos"):

```bash
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
experimentos/estilo.py:3: error: Function is missing a type annotation  [no-untyped-def]
Found 1 error in 1 file (checked 1 source file)
```

## Corrigir

Corrija `experimentos/estilo.py`, com duas linhas em branco e os type hints em `triple`:

```python title="experimentos/estilo.py"
def double(number: int) -> int:
    return number * 2


def triple(number: int) -> int:
    return number * 3
```

```bash
.venv/bin/flake8 experimentos
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy diz que não achou problema. É isso que se espera de cada
exercício, com uma exceção pedida pelo enunciado no exercício 2.
