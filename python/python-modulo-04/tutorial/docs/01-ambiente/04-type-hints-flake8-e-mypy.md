---
sidebar_position: 4
title: Type hints, flake8 e mypy
---

# Type hints, flake8 e mypy

O enunciado pede duas conferências no código: o **estilo**, pelo flake8, e os **tipos**, pelo mypy.
Um arquivo de experimento com um defeito de cada tipo mostra o que cada uma acusa.

## Type hints

Um **type hint** (dica de tipo) anota o tipo de cada parâmetro e do valor devolvido:

```python
def double(number: int) -> int:
    return number * 2
```

- `number: int` diz que o parâmetro `number` é um inteiro;
- `-> int` diz que a função devolve um inteiro;
- uma função que não devolve nada leva `-> None`.

O Python **não** confere essas anotações quando roda o programa; elas servem para quem lê e para o
mypy. O enunciado exige type hints em **todas** as funções e métodos.

## Um arquivo com dois problemas

Crie `experimentos/estilo.py`:

```python
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

Cada aviso diz o arquivo, a linha, a coluna, um código e a explicação: na linha 3, o estilo padrão
do Python (chamado **PEP 8**) pede **duas linhas em branco em volta** de cada função e de cada
classe de um arquivo, separando-as dos `import`, umas das outras e do código que vem depois (só no
começo do arquivo elas não são necessárias), e entre `double` e `triple` não havia nenhuma. Sem
aviso nenhum, o flake8 não imprime nada.

O botão de copiar, no canto de cada bloco de código, não leva a quebra de linha do fim do arquivo.
Sem ela, o flake8 acusa também `W292 no newline at end of file` ("sem quebra de linha no fim do
arquivo") na última linha. Depois de colar, se o cursor ficar no fim de `    return number * 3`,
aperte Enter uma vez antes de salvar.

O flake8 recebe as pastas a conferir. Nunca rode `flake8 .` (o ponto é "a pasta atual"): ele
entraria também na `.venv` e acusaria milhares de avisos no código das bibliotecas instaladas.

## O mypy

O mypy, rodado sem opções, só confere as funções que **têm** type hints; uma função sem nenhuma
anotação passa calada. Para que ele também acuse a **falta** de type hints, que é o que o enunciado
exige, use a opção `--disallow-untyped-defs` ("não aceite funções sem tipos"):

```bash
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
experimentos/estilo.py:3: error: Function is missing a type annotation  [no-untyped-def]
Found 1 error in 1 file (checked 1 source file)
```

## Corrigir

Corrija `experimentos/estilo.py`, com duas linhas em branco e os type hints em `triple`:

```python
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
exercício.
