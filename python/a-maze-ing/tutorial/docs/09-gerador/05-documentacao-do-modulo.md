---
sidebar_position: 5
title: A documentação do módulo
---

# A documentação do módulo

## O que o subject pede

O capítulo VI exige uma documentação curta que mostre como:

- instanciar e usar o gerador, com pelo menos um exemplo básico;
- passar parâmetros personalizados (tamanho, seed);
- acessar a estrutura gerada e pelo menos uma solução.

Ela tem de viajar **junto** com o módulo, dentro do arquivo instalável, e também aparecer no
`README.md`.

## Onde ela mora: a docstring do pacote

A primeira string de `mazegen/__init__.py` é a **docstring do pacote**. Ela vai dentro do wheel
com o código e fica disponível em qualquer instalação:

- `help(mazegen)` a mostra no terminal;
- `mazegen.__doc__` a devolve como string;
- editores e IDEs a exibem ao passar o mouse sobre o `import`.

Um arquivo `mazegen/README.md` separado não seria importado nem exibido por nada disso. O
`README.md` da raiz repete o mesmo texto ([página 7](./07-um-readme-inicial.md)).

## O conteúdo, item a item

| Exigência do subject | Trecho da docstring |
|---|---|
| como instalar | `pip install mazegen-1.0.0-py3-none-any.whl` |
| instanciar, com parâmetros | a assinatura `MazeGenerator(width, height, entry=(0, 0), exit=None, perfect=False, seed=None)` e um parágrafo por parâmetro, com tipo, padrão e um exemplo (`e.g. 20`) |
| o que pode dar errado | quando o construtor e `generate()` levantam `MazeError` |
| acessar a estrutura | `grid`: como ler os bits de cada célula |
| acessar uma solução | `solution`: as letras do caminho mais curto |
| o "42" | `pattern` e o caso em que ele fica vazio |
| exemplo básico | a seção `Example:`, que cria, gera e lê `grid`, `pattern` e `solution` |

Detalhes de forma:

- o exemplo é código puro, indentado com 4 espaços, sem os `>>>` do console. Dá para copiar e
  rodar como está;
- cada parâmetro traz o seu exemplo como `e.g. ...`; `Example:` fica reservado ao título da
  seção onde começa o código de exemplo;
- todas as linhas cabem em 79 colunas, o limite do `flake8`.

## As duas linhas de import

```python
from mazegen.errors import MazeError
from mazegen.generator import MazeGenerator
```

Sem elas, quem usa o pacote teria de escrever `from mazegen.generator import MazeGenerator`.
Com elas, `from mazegen import MazeGenerator` funciona, e o caminho interno pode mudar sem
quebrar ninguém.

## `__all__`

```python
__all__ = ["MazeGenerator", "MazeError"]
```

`__all__` declara a **API pública** do pacote:

- é a lista que `from mazegen import *` importa;
- diz ao leitor e às ferramentas quais nomes fazem parte do contrato;
- satisfaz o `mypy --strict` da regra `make lint-strict`. No modo estrito, um nome que o
  `__init__.py` apenas importa **não** conta como exportado. Sem `__all__`, todo
  `from mazegen import MazeGenerator` da aplicação vira erro:

```text
a_maze_ing.py:12: error: Module "mazegen" does not explicitly export attribute "MazeGenerator"  [attr-defined]
```

`Maze`, `Cell`, `Carver` e os outros continuam acessíveis pelo caminho completo
(`from mazegen.value_objects.pattern42 import Pattern42`, que a aplicação usa na parte 11), mas
não fazem parte da promessa: podem mudar numa versão seguinte.

## Experimente

```python
import mazegen

print(mazegen.__all__)
print(mazegen.__doc__.splitlines()[0])
```

```text
['MazeGenerator', 'MazeError']
Generate random mazes with a "42" drawn by fully closed cells.
```

## O arquivo completo

```python title="mazegen/__init__.py"
"""Generate random mazes with a "42" drawn by fully closed cells.

The package exposes one class, MazeGenerator, and one exception,
MazeError. Install it with:

    pip install mazegen-1.0.0-py3-none-any.whl

MazeGenerator(width, height, entry=(0, 0), exit=None, perfect=False,
seed=None) takes:

    width (int, required): number of columns, 1 to 100, e.g. 20.
    height (int, required): number of rows, 1 to 100, e.g. 15.
    entry (tuple[int, int], default (0, 0)): entry cell as (x, y),
        where x is the column and y is the row, e.g. (0, 0).
    exit (tuple[int, int] | None, default None): exit cell as (x, y),
        e.g. (19, 14); None means the bottom-right cell.
    perfect (bool, default False): True builds a perfect maze, with
        exactly one path between any two cells; False builds a
        Pac-Man board, with loops and at most two dead ends; e.g. True.
    seed (int | None, default None): seed of the random source, e.g. 42;
        the same seed gives the same sequence of mazes; None gives a
        different one on every run.

The constructor raises MazeError when a parameter is impossible: width
or height outside 1..100, entry or exit outside the grid or on the
"42", entry equal to exit, or perfect=False with
(width - 1) * (height - 1) < 2. The message names the parameter.

Each call to generate() builds a new maze and fills:

    grid (list[list[int]]): height rows of width integers; grid[y][x]
        holds the closed walls of cell (x, y) as bits N=1, E=2, S=4,
        W=8, so 15 is a fully closed cell. The output file writes each
        value as one hexadecimal digit.
    solution (str): the shortest path from entry to exit, one letter
        N, E, S or W per step.

With perfect=False, generate() raises MazeError if 20 attempts in a
row fail to build a Pac-Man board.

pattern (set[tuple[int, int]]) holds the (x, y) cells of the "42" from
the constructor on. It is empty when the maze is smaller than 9x7 and
the "42" does not fit; the maze is generated without it.

Example:
    from mazegen import MazeGenerator

    gen = MazeGenerator(width=20, height=15, seed=42)
    gen.generate()
    walls = gen.grid[0][0]
    print("north wall of (0, 0) closed:", bool(walls & 1))
    print(len(gen.pattern), "cells draw the 42")
    print(gen.solution)
"""

from mazegen.errors import MazeError
from mazegen.generator import MazeGenerator

__all__ = ["MazeGenerator", "MazeError"]
```
