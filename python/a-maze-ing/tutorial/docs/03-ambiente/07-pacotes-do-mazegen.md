---
sidebar_position: 9
title: Os pacotes do mazegen
---

# Os pacotes do `mazegen`

As classes do gerador vão morar em pastas: `mazegen/entities/`, `mazegen/value_objects/` e
`mazegen/services/` (a [parte 2](../02-arquitetura/05-arvore-de-arquivos.md) mostra a árvore
inteira). Para o Python conseguir importar uma classe de dentro dessas pastas, cada uma precisa
virar um **pacote**. Esta página cria as pastas e os arquivos que fazem isso.

## Módulo e pacote

- Um **módulo** é um arquivo `.py`. O arquivo `mazegen/errors.py` é o módulo `mazegen.errors`:
  o caminho com `.` no lugar de `/` e sem o `.py`.
- Um **pacote** é uma pasta com um arquivo chamado `__init__.py`. A pasta `mazegen/` é o pacote
  `mazegen`, e `mazegen/entities/` é o pacote `mazegen.entities`.

É esse nome com pontos que aparece nos imports:

```python
from mazegen.entities.maze import Maze
```

quer dizer "da pasta `mazegen/entities/`, arquivo `maze.py`, traga a classe `Maze`".

## O `__init__.py`

O `__init__.py` é o código que roda na primeira vez que alguém importa o pacote. Ele pode ter
quase nada: a simples presença dele já diz ao Python, ao mypy e ao setuptools "esta pasta é um
pacote do projeto".

E sem ele? O Python 3 ainda consegue importar a pasta, mas a trata de outro jeito, como um
*namespace package*. Esse tipo de pacote existe para um caso especial: um mesmo pacote espalhado
por várias pastas, instaladas em lugares diferentes do computador. Não é o caso aqui.

O projeto escolhe não depender desse caso especial: toda pasta de código tem o seu
`__init__.py`, e assim fica explícito, para quem lê e para as ferramentas, que ela é um pacote
comum do projeto.

## Docstring: a documentação dentro do código

Uma **docstring** é um texto entre três aspas (`"""`) escrito logo na primeira linha de um
módulo, de uma classe ou de uma função. O Python a guarda junto com o objeto, e ela aparece no
`help()`:

```python
def area(width: int, height: int) -> int:
    """Number of cells of a grid."""
    return width * height
```

O enunciado exige docstrings nas funções e nas classes, seguindo a PEP 257 (o guia oficial de
como escrevê-las), e cita dois estilos como exemplo: o do Google e o do NumPy. O projeto escolhe
o do **Google**: um resumo de uma linha e, quando há o que dizer, seções como `Args:` (os
parâmetros) e `Returns:` (o que a função devolve). A
[parte 4](../04-value-objects/03-direction-propriedades.md) mostra as primeiras com essas seções.

O projeto vai um passo além, também por escolha: **todo módulo** começa com uma docstring,
inclusive os `__init__.py`. Nas subpastas, essa docstring é uma frase que diz o que o pacote
guarda, e não há mais nada no arquivo.

Por isso as classes são importadas sempre pelo caminho completo, com o nome do arquivo:

```python
from mazegen.entities.maze import Maze
```

e nunca pelo nome da subpasta, como `from mazegen.entities import Maze`. Essa segunda forma só
funcionaria se o `__init__.py` de `entities/` importasse o `Maze`, e ele não importa nada. Com o
caminho completo, todo import diz o arquivo exato de onde a classe vem.

## Criando as pastas

```bash
mkdir -p mazegen/entities mazegen/value_objects mazegen/services
```

`mkdir -p` cria a pasta e as pastas-mãe que faltarem, de uma vez. Depois, um `__init__.py` em
cada subpasta:

```python title="mazegen/entities/__init__.py"
"""Mutable entities of the maze generator."""
```

As **entidades**: objetos cujo estado muda, mas que protegem as próprias regras. Só o `Maze`, a
grade de paredes ([parte 5](../05-maze/01-a-grade-de-paredes.md)).

```python title="mazegen/value_objects/__init__.py"
"""Immutable value objects of the maze generator."""
```

Os **value objects**: valores que não mudam depois de criados. `Direction`, `Cell` e `Pattern42`
([parte 4](../04-value-objects/01-maze-error.md)).

```python title="mazegen/services/__init__.py"
"""Stateless services that carve, braid and solve a maze."""
```

Os **services**: operações que não guardam estado. `Carver`, que cava o labirinto; `Braider`,
que o transforma em tabuleiro Pac-Man; e `Solver`, que acha o caminho mais curto (partes
[6](../06-carver/01-labirinto-perfeito.md), [8](../08-braider/01-becos-sem-saida.md) e
[7](../07-solver/01-busca-em-largura.md)).

## O `mazegen/__init__.py`, por enquanto

O `__init__.py` da pasta `mazegen/` é diferente dos outros: na versão final, ele é a
documentação de uso do gerador e exporta `MazeGenerator` e `MazeError`, as duas classes que quem
reutiliza o pacote precisa conhecer. Ainda não existe gerador para exportar, então, **por
enquanto**, crie o `mazegen/__init__.py` só com esta linha, um resumo de uma linha:

```python
"""Generate random mazes with a "42" drawn by fully closed cells."""
```

Ele ganha o conteúdo final, com a documentação e os imports, na
[parte 9](../09-gerador/05-documentacao-do-modulo.md). Por isso este bloco não é o arquivo
completo, ao contrário dos três acima.

## `py.typed`

```bash
touch mazegen/py.typed
```

`touch` cria um arquivo **vazio**. O nome `py.typed` é um combinado definido pela PEP 561 (o
documento oficial do Python sobre o assunto): quando outro projeto instala o `mazegen` e roda o
mypy, o mypy só lê as anotações de tipo do pacote instalado se encontrar esse arquivo nele. Sem
o `py.typed`, o mypy do outro projeto trata o `mazegen` como uma biblioteca sem tipos e
reclama:

```text
error: Skipping analyzing "mazegen": module is installed, but missing library stubs or py.typed marker  [import-untyped]
```

O `pyproject.toml` já inclui o `py.typed` no pacote, na seção
[`[tool.setuptools.package-data]`](./04-pyproject.md).

## Como fica

```text
mazegen/
    __init__.py
    py.typed
    entities/
        __init__.py
    value_objects/
        __init__.py
    services/
        __init__.py
```
