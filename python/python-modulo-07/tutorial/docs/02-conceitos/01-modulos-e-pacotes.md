---
sidebar_position: 1
title: Módulos e pacotes
---

# Módulos e pacotes

O projeto espalha o código por vários arquivos e pastas: o programa `battle.py`, na raiz, usa
classes escritas dentro da pasta `ex0/`. Para isso, o Python precisa saber onde procurar cada
arquivo e o que cada pasta oferece a quem a importa.

## Módulo

Todo arquivo `.py` é um **módulo**. `import nome` carrega o arquivo `nome.py`, roda o código dele
uma vez e dá acesso ao que ele define:

- `import shapes` dá acesso aos nomes com o prefixo: `shapes.make_square`;
- `from shapes import make_square` traz o nome direto: `make_square`.

Os `import` ficam no começo do arquivo, antes de qualquer outro código; o flake8 acusa um
`import` escrito depois (aviso `E402`).

## Onde o Python procura

O Python procura os módulos importados numa lista de pastas. A primeira é a **pasta do programa
rodado**: com `python3 experimentos/pacote.py`, é a pasta `experimentos/`, e não a pasta onde o
terminal está. Com `python3 -c '...'`, que roda o código escrito entre as aspas, a primeira é a
pasta atual do terminal. Depois vêm as pastas da biblioteca do Python, onde estão `abc` e
`typing`.

Uma **variável de ambiente** é um valor com nome que o terminal entrega aos programas que roda.
A variável de ambiente `PYTHONPATH` acrescenta pastas a essa lista, logo depois da primeira e
antes das pastas da biblioteca do Python. Escrita antes do
comando, ela vale só para ele: `PYTHONPATH=experimentos python3 -c '...'` deixa o código entre
as aspas importar os arquivos de `experimentos/`.

## Pacote

Um **pacote** é uma pasta com um arquivo `__init__.py`. Ele é importado pelo nome da pasta, e os
módulos de dentro, com ponto: o arquivo `square.py` da pasta `shapes/` é o módulo
`shapes.square`. `import shapes` roda o `__init__.py`, e os nomes que o `__init__.py` define ou
importa são o que o pacote oferece a quem o importa.

## O experimento

Crie a pasta do pacote:

```bash
mkdir experimentos/shapes
```

Dentro dela, um módulo com uma classe e uma função que cria objetos da classe:

```python title="experimentos/shapes/square.py"
class Square:
    def __init__(self, side: int) -> None:
        self.side = side

    def area(self) -> int:
        return self.side * self.side


def make_square(side: int) -> Square:
    return Square(side)
```

E o `__init__.py`, que oferece só a função:

```python title="experimentos/shapes/__init__.py"
from .square import make_square
```

O ponto em `.square` é um **import relativo**: "o módulo `square` **deste** pacote". Ele só
funciona em arquivos que fazem parte de um pacote.

Fora do pacote, em `experimentos/`, o programa que o usa:

```python title="experimentos/pacote.py"
import shapes
from shapes import make_square
from shapes.square import Square

square = make_square(3)
print(square.area())
print(isinstance(square, Square))
print(hasattr(shapes, "make_square"))
print(hasattr(shapes, "Square"))
```

`hasattr(objeto, "nome")` responde se o objeto tem um atributo com aquele nome. Um pacote
importado também é um objeto, e os nomes que ele oferece são atributos dele.

```bash
python3 experimentos/pacote.py
```

```text
9
True
True
False
```

## O que aconteceu

- `import shapes` achou a pasta `experimentos/shapes/`, porque `experimentos/` é a pasta do
  programa rodado, e rodou o `__init__.py`;
- `make_square(3)` criou um `Square` de lado 3, de área 9. `isinstance(square, Square)` responde
  se o objeto é da classe `Square` (ou de uma filha dela): `True`;
- o pacote `shapes` tem o nome `make_square`, que o `__init__.py` importou, mas não tem `Square`:
  `from shapes import Square` falharia. A classe continua alcançável pelo módulo de dentro,
  `shapes.square`: o Python não esconde nada. O que o `__init__.py` controla é o que o pacote
  oferece pelo próprio nome.

## O aviso do flake8 no `__init__.py`

```bash
.venv/bin/flake8 experimentos
```

```text
experimentos/shapes/__init__.py:1:1: F401 '.square.make_square' imported but unused
```

O flake8 vê um nome importado que o arquivo nunca usa (aviso `F401`, "importado mas não
usado"). Num `__init__.py`, o nome é importado justamente para ser oferecido a quem importa o
pacote. A lista `__all__` diz isso: é a lista, em texto, dos nomes **públicos** do pacote, os que
ele oferece. O flake8 considera usado todo nome que está em `__all__`, e o mypy também a lê.
Corrija o `__init__.py`:

```python title="experimentos/shapes/__init__.py"
from .square import make_square

__all__ = ["make_square"]
```

Acrescente ao fim de `experimentos/pacote.py` uma linha que mostra a lista:

```python title="experimentos/pacote.py"
import shapes
from shapes import make_square
from shapes.square import Square

square = make_square(3)
print(square.area())
print(isinstance(square, Square))
print(hasattr(shapes, "make_square"))
print(hasattr(shapes, "Square"))
print(shapes.__all__)
```

```bash
python3 experimentos/pacote.py
.venv/bin/flake8 experimentos
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
9
True
True
False
['make_square']
Success: no issues found in 4 source files
```

## Um arquivo de pacote não é rodado sozinho

```bash
python3 experimentos/shapes/__init__.py
```

A última linha da saída é:

```text
ImportError: attempted relative import with no known parent package
```

("import relativo sem pacote pai conhecido"). Rodado direto, o arquivo não faz parte de pacote
nenhum, e o `.square` não tem a que se referir. Os arquivos de um pacote são sempre usados por
meio de um `import`, a partir de um programa de fora.

## O `__pycache__`

```bash
LC_ALL=C ls -1 experimentos/shapes
```

```text
__init__.py
__pycache__
square.py
```

O `-1` do `ls` lista um nome por linha. O `LC_ALL=C` antes do comando faz o `ls` ordenar os
nomes pelo código de cada caractere, a mesma ordem em qualquer sistema; sem ele, a ordem segue o
idioma configurado no terminal, e no Linux os nomes que começam com `_` podem aparecer depois
dos outros. Ao importar um módulo, o Python grava na pasta dele uma
`__pycache__/` com uma versão pré-processada do arquivo, para carregar mais rápido da próxima
vez. Ela é refeita sozinha quando o arquivo muda e pode ser apagada a qualquer momento.

## No projeto

A raiz `datadeck/` tem o mesmo papel da pasta `experimentos/`: `python3 battle.py` põe a raiz na
lista de busca, e `battle.py` importa o pacote `ex0`. Dentro de um pacote, um módulo importa o
vizinho com import relativo (`from .creature import Creature`); o `ex1` usa o `ex0` com o nome
completo (`from ex0.creature import Creature`), o que funciona porque o programa rodado está na
raiz. Por isso os três programas de teste ficam na raiz, e todos os comandos são rodados de lá.
