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
funções e métodos. As variáveis podem ficar sem anotação quando o mypy consegue deduzir o tipo
pelo valor (`count = 0` é um `int`).

No Pydantic, os type hints ganham um segundo papel: são eles que dizem ao Pydantic o tipo de cada
campo de um modelo. Aí sim o tipo é conferido enquanto o programa roda
([O primeiro modelo](../02-conceitos/01-o-primeiro-modelo.md)).

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
.venv/bin/flake8 experimentos/estilo.py
```

```text
experimentos/estilo.py:3:1: E302 expected 2 blank lines, found 0
```

Cada aviso diz o arquivo, a linha, a coluna, um código e a explicação: na linha 3, o estilo
padrão do Python (chamado **PEP 8**) pede **duas linhas em branco entre** as funções e as
classes de um arquivo (não antes da primeira), e entre `double` e `triple` não havia nenhuma.
Sem aviso nenhum, o flake8 não imprime nada.

O flake8 recebe os arquivos ou as pastas a conferir. Nunca rode `flake8 .` (o ponto é "a pasta
atual"): ele entraria também na `.venv` e acusaria milhares de avisos no código das bibliotecas
instaladas.

## O mypy

O mypy, rodado sem opções, só confere as funções que **têm** type hints; uma função sem nenhuma
anotação passa calada. Para que ele também acuse a **falta** de type hints, que é o que o
enunciado exige, use a opção `--disallow-untyped-defs` ("não aceite funções sem tipos"):

```bash
.venv/bin/mypy --disallow-untyped-defs experimentos/estilo.py
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
.venv/bin/flake8 experimentos/estilo.py
.venv/bin/mypy --disallow-untyped-defs experimentos/estilo.py
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy diz que não achou problema. É isso que se espera de cada
arquivo do projeto.

## O mypy e o Pydantic

O Pydantic traz um **plugin** para o mypy, um complemento que muda o jeito como o mypy enxerga
os modelos. O plugin só é ligado por um arquivo de configuração do mypy (a linha
`plugins = pydantic.mypy`), e esse arquivo não faria parte da entrega: o enunciado pede só os
três `.py`.

O que muda é a conferência do construtor. Sem o plugin, o mypy exige que cada argumento passado
ao criar um objeto tenha o tipo do campo, e recusa, por exemplo, uma data escrita como texto num
campo `datetime`. Com o plugin na configuração padrão, o mypy aceita qualquer tipo no construtor,
porque o Pydantic converteria o valor; com a opção `init_typed = True` do plugin, a recusa volta.
A página [Conversão de tipos](../02-conceitos/04-conversao-de-tipos.md#e-pelo-construtor) mostra
esse caso.

Escolha do tutorial: **mypy sem o plugin**, sempre com `--disallow-untyped-defs`, o modo mais
exigente com o construtor. Os três arquivos entregues passam no mypy dos dois jeitos: sem o
plugin e com ele, com `--disallow-untyped-defs` e também com `--strict`, a opção que liga de uma vez um
grupo de conferências extras do mypy.
