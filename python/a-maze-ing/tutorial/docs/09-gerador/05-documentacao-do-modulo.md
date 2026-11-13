---
sidebar_position: 6
title: A documentação do módulo
---

# A documentação do módulo

Quem for usar o `mazegen` num projeto futuro vai receber só o pacote instalado, sem este tutorial
e sem acesso a quem o escreveu. Por isso o enunciado exige uma documentação curta que viaje junto
com o código. Esta página mostra onde ela fica (na **docstring** do pacote), o que ela diz e as
duas linhas que definem o que o pacote oferece a quem o importa.

## O que o enunciado pede

Uma documentação curta que mostre como:

- criar e usar o gerador, com pelo menos um exemplo básico;
- passar parâmetros escolhidos por quem usa (por exemplo, o tamanho e a semente);
- ler o labirinto gerado e pelo menos uma solução (um caminho da entrada à saída).

Ela precisa estar **dentro** do arquivo instalável do pacote (o arquivo `.whl` da
[página 9](./08-o-pacote.md)), junto com o código, e também no `README.md` do repositório.

## Onde ela mora: a docstring do pacote

Uma **docstring** é um texto entre três aspas (`"""`) colocado logo na primeira linha de um módulo,
de uma classe ou de uma função. O Python a guarda junto com o código, e ferramentas a mostram como
documentação. O enunciado exige docstrings em funções e classes; pôr uma também no começo de cada
arquivo (a docstring do módulo) é escolha do projeto
([parte 3](../03-ambiente/07-pacotes-do-mazegen.md)).

O arquivo `mazegen/__init__.py` é o que o Python roda quando alguém escreve `import mazegen`
([parte 3](../03-ambiente/07-pacotes-do-mazegen.md)). A docstring dele é a **docstring do
pacote**. Como ela é parte do código, vai dentro do pacote instalável e fica disponível em
qualquer instalação:

- `help(mazegen)` a mostra no terminal;
- `mazegen.__doc__` a devolve como texto;
- editores de código a exibem ao passar o mouse sobre o `import`.

Um arquivo `mazegen/README.md` separado não seria mostrado por nada disso. Pôr a documentação na
docstring é escolha do projeto; o `README.md` da raiz repete o mesmo texto
([página 8](./07-um-readme-inicial.md)).

## O conteúdo, item a item

| O que a documentação precisa dizer | Trecho da docstring |
|---|---|
| como instalar | `pip install mazegen-1.0.0-py3-none-any.whl` |
| como criar o gerador, com parâmetros | a assinatura `MazeGenerator(width, height, entry=(0, 0), exit=None, perfect=False, seed=None)` e um parágrafo por parâmetro, com tipo, padrão e um exemplo (`e.g. 20`, "por exemplo, 20") |
| o que pode dar errado | quando o construtor e `generate()` levantam `MazeError` |
| como ler o labirinto | `grid`: como ler as paredes de cada célula |
| como ler uma solução | `solution`: as letras do caminho mais curto |
| o "42" | `pattern` e o caso em que ele fica vazio |
| um exemplo básico | a seção `Example:`, que cria o gerador, gera e lê `grid`, `pattern` e `solution` |

Detalhes de forma:

- o exemplo é código puro, recuado com 4 espaços, sem os `>>>` do console interativo do Python.
  Dá para copiar e rodar como está;
- cada parâmetro traz o seu exemplo como `e.g. ...`; a palavra `Example:` fica reservada ao título
  da seção onde começa o código de exemplo;
- todas as linhas cabem em 79 caracteres, o limite de largura de linha do `flake8`, a ferramenta
  que confere o estilo do código ([parte 3](../03-ambiente/05-flake8-e-gitignore.md)).

## As duas linhas de import

```python
from mazegen.errors import MazeError
from mazegen.generator import MazeGenerator
```

O `MazeGenerator` mora em `mazegen/generator.py`. Até aqui, o `mazegen/__init__.py` tinha só a
docstring de uma linha da [parte 3](../03-ambiente/07-pacotes-do-mazegen.md), e
`from mazegen import MazeGenerator` falhava com o erro
`ImportError: cannot import name 'MazeGenerator' from 'mazegen'`: o Python procura o nome no
`__init__.py`, e ele não estava lá. Por isso os
exemplos das páginas anteriores usavam o caminho completo,
`from mazegen.generator import MazeGenerator`.

Com estas duas linhas no `__init__.py`, os dois nomes passam a existir dentro do pacote, e
`from mazegen import MazeGenerator` funciona. Quem usa o pacote não precisa saber em que arquivo
cada coisa está, e o arquivo interno pode até mudar de nome numa versão futura sem quebrar quem
usa. Os exemplos daqui em diante usam a forma curta.

## `__all__`

```python
__all__ = ["MazeGenerator", "MazeError"]
```

`__all__` é uma lista com os nomes que o pacote oferece a quem o importa: a sua **API pública**
(*API* é o conjunto de nomes e funções que um código oferece para outro usar). Ela serve para três
coisas:

- é a lista que `from mazegen import *` importa. O `*` quer dizer "todos os nomes que o pacote
  oferece": em vez de listar `MazeGenerator, MazeError`, quem importa pega todos de uma vez;
- diz a quem lê, e às ferramentas, quais nomes fazem parte da promessa do pacote;
- é exigida pelo `mypy` no modo rigoroso. O `mypy` é a ferramenta que confere as anotações de tipo
  ([parte 3](../03-ambiente/04-pyproject.md)), e a regra `make lint-strict` do `Makefile` o roda
  com a opção `--strict`. Nesse modo, um nome que o `__init__.py` apenas importa **não** conta
  como oferecido pelo pacote. Sem `__all__`, cada `from mazegen import MazeGenerator` da aplicação
  vira erro:

```text
a_maze_ing.py:12: error: Module "mazegen" does not explicitly export attribute "MazeGenerator"  [attr-defined]
```

`Maze`, `Cell`, `Carver` e os outros continuam acessíveis pelo caminho completo (a aplicação usa
`from mazegen.value_objects.pattern42 import Pattern42` na
[parte 11](../11-configuracao/04-o-42-e-o-arquivo-completo.md)), mas não fazem parte da promessa:
podem mudar numa versão seguinte sem aviso. A aplicação pode usá-las porque mora no mesmo
repositório e muda junto com o `mazegen`: se o miolo mudar, ela é ajustada no mesmo commit. Um
projeto de fora, que só instala o pacote, deve usar apenas `MazeGenerator` e `MazeError`.

## O arquivo completo

A documentação está em inglês, como todo o resto do projeto entregue (escolha do projeto).

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

## Experimente

Com o `__init__.py` completo, a forma curta de importar funciona. Na raiz do projeto:

```bash
.venv/bin/python - <<'EOF'
import mazegen
from mazegen import MazeError, MazeGenerator

print(mazegen.__all__)
print(mazegen.__doc__.splitlines()[0])
gen = MazeGenerator(width=20, height=15, seed=42)
gen.generate()
print(gen.solution)
try:
    MazeGenerator(width=0, height=15)
except MazeError as error:
    print(error)
EOF
```

```text
['MazeGenerator', 'MazeError']
Generate random mazes with a "42" drawn by fully closed cells.
SSEEESSSSSENNNESSSSEESSSSEESSEEEENNESSEEEEE
width must be between 1 and 100, got 0
```

- A primeira linha é o `__all__`; a segunda, a primeira linha da docstring (`mazegen.__doc__` é o
  texto inteiro, `splitlines()` o quebra em linhas e `[0]` pega a primeira).
- As duas últimas mostram `MazeGenerator` e `MazeError` importados direto de `mazegen`: o mesmo
  caminho da semente 42 da [página 5](./04-o-arquivo-do-gerador.md) e a mesma recusa de largura 0.
