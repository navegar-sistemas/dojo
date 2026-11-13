---
sidebar_position: 4
title: Type hints, flake8 e mypy
---

# Type hints, flake8 e mypy

O código passa por duas conferências: o **estilo**, pelo flake8, e os **tipos**, pelo mypy. Cada
função também leva uma docstring, que a documenta.

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
o mypy. Todas as funções do projeto têm type hints.

## Docstrings

Uma **docstring** é um texto entre três aspas duplas logo na primeira linha de uma função. Ela
diz o que a função faz:

```python
def double(number: int) -> int:
    """Return twice the number."""
    return number * 2
```

O Python guarda esse texto junto da função, e ferramentas de documentação e editores o mostram
para quem usa a função. O enunciado pede código bem documentado; cada função dos exercícios tem
uma docstring de uma linha, em inglês como o resto do código.

## Um arquivo com dois problemas

```python title="experimentos/estilo.py"
def double(number: int) -> int:
    return number * 2
def triple(number):
    return number * 3
```

Ele tem dois defeitos: faltam linhas em branco entre as funções, e `triple` não tem type hints.

## O flake8

```bash
.venv/bin/flake8 experimentos
```

```text
experimentos/estilo.py:3:1: E302 expected 2 blank lines, found 0
```

Cada aviso diz o arquivo, a linha, a coluna, um código e a explicação: na linha 3, o estilo
padrão do Python (chamado **PEP 8**) pede **duas linhas em branco** antes de cada função do
arquivo (as que ficam fora de classes), e não havia nenhuma. Sem aviso nenhum, o flake8 não
imprime nada.

O flake8 também acusa linhas com mais de **79 caracteres** (aviso `E501`). Várias mensagens dos
exercícios são compridas e precisam ser quebradas em mais de uma linha de código.

O flake8 recebe as pastas a conferir. Nunca rode `flake8 .` (o ponto é "a pasta atual"): ele
entraria também na `.venv` e acusaria milhares de avisos no código das bibliotecas instaladas.

## O mypy

O mypy, rodado sem opções, só confere as funções que **têm** type hints; uma função sem nenhuma
anotação passa calada. Para que ele também acuse a **falta** de type hints, use a opção
`--disallow-untyped-defs` ("não aceite funções sem tipos"):

```bash
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
experimentos/estilo.py:3: error: Function is missing a type annotation  [no-untyped-def]
Found 1 error in 1 file (checked 1 source file)
```

## Corrigir

Com duas linhas em branco, type hints em `triple` e uma docstring em cada função:

```python title="experimentos/estilo.py"
def double(number: int) -> int:
    """Return twice the number."""
    return number * 2


def triple(number: int) -> int:
    """Return three times the number."""
    return number * 3
```

```bash
.venv/bin/flake8 experimentos
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy diz que não achou problema.
