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
def create_fire() -> str:
    return "Fire element created"
```

- `-> str` diz que a função devolve um texto;
- um parâmetro também leva o tipo, como em `def greet(name: str) -> str:`;
- uma função que não devolve nada leva `-> None`.

O Python **não** confere essas anotações quando roda o programa; elas servem para quem lê e para
o mypy. O enunciado exige type hints em **todo** o código: os parâmetros e o retorno de todas as
funções.

## Um arquivo com dois problemas

Crie `experimentos/estilo.py`:

```python title="experimentos/estilo.py"
def create_salt() -> str:
    return "Salt created"
def create_sulfur():
    return "Sulfur created"
```

Ele tem dois defeitos: faltam as linhas em branco entre as funções, e `create_sulfur` não diz o
tipo que devolve.

## O flake8

```bash
.venv/bin/flake8 experimentos
```

```text
experimentos/estilo.py:3:1: E302 expected 2 blank lines, found 0
```

Cada aviso diz o arquivo, a linha, a coluna, um código e a explicação: na linha 3, o estilo
padrão do Python (chamado **PEP 8**) pede **duas linhas em branco entre** as funções de um
arquivo (não antes da primeira), e entre `create_salt` e `create_sulfur` não havia nenhuma. Sem
aviso nenhum, o flake8 não imprime nada.

O flake8 recebe as pastas e os arquivos a conferir. Nunca rode `flake8 .` (o ponto é "a pasta
atual"): ele entraria também na `.venv` e acusaria milhares de avisos no código das bibliotecas
instaladas. Neste projeto, os arquivos entregues ficam na própria pasta `the-codex`, ao lado da
`.venv`; a [Parte I](../03-parte-1/08-rodar-e-conferir.md) mostra como passar só eles.

## O mypy

O mypy, rodado sem opções, só confere as funções que **têm** type hints; uma função sem nenhuma
anotação passa calada. Para que ele também acuse a **falta** de type hints, que é o que o
enunciado exige, use a opção `--disallow-untyped-defs` ("não aceite funções sem tipos"):

```bash
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
experimentos/estilo.py:3: error: Function is missing a return type annotation  [no-untyped-def]
Found 1 error in 1 file (checked 1 source file)
```

"A função não tem a anotação do tipo de retorno." O código entre colchetes, `no-untyped-def`, é
o nome da regra que acusou.

## Corrigir

Corrija `experimentos/estilo.py`, com duas linhas em branco e o tipo do retorno em
`create_sulfur`:

```python title="experimentos/estilo.py"
def create_salt() -> str:
    return "Salt created"


def create_sulfur() -> str:
    return "Sulfur created"
```

```bash
.venv/bin/flake8 experimentos
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy diz que não achou problema. É isso que se espera de cada
parte do projeto, com uma única exceção que o enunciado pede de propósito, na Parte I.
