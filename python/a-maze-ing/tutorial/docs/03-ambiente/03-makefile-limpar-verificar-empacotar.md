---
sidebar_position: 4
title: "Makefile: verificar o código"
---

# Makefile: verificar o código

O enunciado exige que o código siga o padrão do flake8 e passe no mypy sem erros, duas
ferramentas de verificação. Esta página explica o que cada uma confere e escreve as duas regras
do `Makefile` que as rodam: `lint`, com as opções que o enunciado fixa, e `lint-strict`, a versão
mais rigorosa. Como na [página anterior](./02-makefile-instalar-e-rodar.md), cada trecho entra no
fim do `Makefile`.

## `lint`: o que o flake8 e o mypy fazem

**Lint** é o nome que se dá a verificar o código sem executá-lo, à procura de erros e de desvios
do padrão.

O **flake8** confere o **estilo**, segundo a PEP 8, o guia de estilo oficial do Python (linhas
de até 79 caracteres, espaços em volta de operadores, duas linhas em branco entre funções...).
Ele também acusa erros simples, como um `import` que não é usado. Um exemplo, só para ver a
saída (não precisa criar o arquivo), num `estilo.py` com um `import os` que nunca é usado e um
`=` sem espaços em volta:

```python
import os


def area(largura: int, altura: int) -> int:
    resultado=largura * altura
    return resultado
```

`flake8 estilo.py` responde:

```text
estilo.py:1:1: F401 'os' imported but unused
estilo.py:5:14: E225 missing whitespace around operator
```

Cada linha diz o arquivo, a linha, a coluna, o código do problema e a explicação.

O **mypy** confere as **anotações de tipo**: o `: int` de um parâmetro e o `-> int` do retorno de
uma função. O Python ignora essas anotações na hora de rodar; o mypy as lê e acusa quando o
código as contradiz. Outro exemplo, num `exemplo.py` com uma função anotada `-> int` que devolve
um texto (`str`), e outra função sem anotação nenhuma:

```python
def dobro(numero: int) -> int:
    return str(numero * 2)


def metade(numero):
    return numero // 2
```

Com as opções da regra `lint` (logo abaixo), o mypy responde:

```text
exemplo.py:2: error: Incompatible return value type (got "str", expected "int")  [return-value]
exemplo.py:5: error: Function is missing a type annotation  [no-untyped-def]
Found 2 errors in 1 file (checked 1 source file)
```

## `lint`: a regra

O enunciado fixa os dois comandos, com estas opções exatas:

```makefile
MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports \
	--disallow-untyped-defs --check-untyped-defs
```

```makefile
lint:
	$(PY) -m flake8 .
	$(PY) -m mypy . $(MYPY_FLAGS)
```

O `.` quer dizer "a pasta atual e tudo dentro dela". As opções ficam numa variável só porque a
linha não caberia na tela: a `\` no fim da primeira linha continua a variável na linha de baixo,
e na hora de rodar o `make` junta tudo numa linha só.

| Opção do mypy | Efeito |
|---|---|
| `--warn-return-any` | acusa uma função com tipo de retorno declarado que devolve um valor de tipo `Any` ("qualquer coisa", sem tipo conhecido) |
| `--warn-unused-ignores` | acusa um `# type: ignore` (o comentário que manda o mypy pular uma linha) que não está pulando erro nenhum |
| `--ignore-missing-imports` | não acusa bibliotecas de terceiros que não têm anotações de tipo |
| `--disallow-untyped-defs` | acusa toda função ou método sem anotação de tipo |
| `--check-untyped-defs` | confere também o corpo das funções sem anotação |

As duas últimas parecem repetidas: se toda função precisa ter anotação, não sobra função sem
anotação para conferir. O projeto usa as duas porque o enunciado fixa a linha do `mypy` com as
cinco opções, palavra por palavra.

O `flake8 .` confere todos os arquivos `.py` do projeto; as pastas que ele deve pular ficam no
arquivo `.flake8` ([explicado adiante](./05-flake8-e-gitignore.md)).

## `lint-strict`

```makefile
lint-strict:
	$(PY) -m flake8 .
	$(PY) -m mypy . --strict
```

`--strict` liga quase todas as verificações do mypy, inclusive quatro das cinco do `lint`; só
`--ignore-missing-imports` fica de fora, e o projeto não precisa dela, porque não usa biblioteca
de terceiros. O enunciado deixa a regra `lint-strict` opcional, mas "fortemente recomendada".

O projeto passa nas duas regras sem nenhum `# type: ignore` nem `# noqa` (o comentário que manda
o flake8 pular uma linha). Isso é uma escolha: calar a ferramenta numa linha esconderia o
problema em vez de resolvê-lo.

## Experimente

```bash
make -n lint lint-strict
```

```text
.venv/bin/python -m flake8 .
.venv/bin/python -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
.venv/bin/python -m flake8 .
.venv/bin/python -m mypy . --strict
```

A segunda linha é o comando do enunciado, palavra por palavra, só que com o Python do `.venv`.

Faltam duas regras, `clean`, que apaga os arquivos que as ferramentas criam sozinhas, e
`build`, que monta o pacote do gerador. As duas e o `Makefile` completo estão na
[próxima página](./09-makefile-empacotar.md).

