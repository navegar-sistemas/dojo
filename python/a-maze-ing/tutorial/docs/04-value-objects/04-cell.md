---
sidebar_position: 4
title: Cell
---

# `Cell`

Todo algoritmo do gerador trabalha com posições na grade: "estou na célula `3,4`", "a vizinha
de cima é `3,3`", "já visitei a `0,0`". Esta página cria o tipo que representa uma posição, a
classe `Cell`, em `mazegen/value_objects/cell.py`.

## O que é

Uma posição na grade: a coluna `x` e a linha `y`, as duas contadas a partir de 0, com a célula
`0,0` no canto de cima à esquerda e `y` crescendo para baixo. Dentro do `mazegen`, toda posição é
uma `Cell`. Fora dele (no arquivo de opções, na aplicação e para quem reutiliza o gerador), uma
posição é uma tupla comum `(x, y)`.

## Por que não uma tupla

Uma tupla `(3, 4)` funcionaria, mas:

- `cell.x` diz o que é; `pos[0]` obriga a lembrar que o primeiro número é a coluna;
- o mypy distingue uma `Cell` de qualquer outro par de inteiros, como um deslocamento
  `(dx, dy)` ou um tamanho `(largura, altura)`, e recusa trocar um pelo outro;
- a `Cell` tem um método, `step`, que dá a posição vizinha.

Numa grade de 100x100, o custo extra de memória e de tempo é desprezível.

## `@dataclass`: a classe escrita a partir dos campos

```python
@dataclass(frozen=True, slots=True)
class Cell:
    x: int
    y: int
```

`@dataclass` é um decorador da biblioteca padrão (do módulo `dataclasses`) que escreve sozinho os
métodos repetitivos de uma classe, a partir dos campos anotados (`x: int` e `y: int`):

- o `__init__`, que recebe os campos na ordem: `Cell(3, 4)`;
- o `__repr__`, que mostra o objeto como `Cell(x=3, y=4)`;
- o `__eq__`, que faz o `==` comparar os **campos**: `Cell(3, 4) == Cell(3, 4)` é `True`, mesmo
  sendo dois objetos diferentes.

Sem o `@dataclass`, seria preciso escrever esses três métodos à mão, e o `==` de uma classe comum
compara a **identidade** (se é o mesmo objeto), não o conteúdo.

### `frozen=True`: não muda, e pode entrar num `set`

`frozen` quer dizer "congelado": uma `Cell` não muda depois de criada. Tentar trocar um campo
levanta um erro:

```python
cell = Cell(3, 4)
cell.x = 5      # dataclasses.FrozenInstanceError: cannot assign to field 'x'
```

É o que faz da `Cell` um **value object**: um objeto que é só um valor, como o número 3. Quem
precisa de outra posição cria outra `Cell`.

O congelamento traz um segundo ganho, o **hash**. Um `set` (conjunto) e as chaves de um `dict`
só aceitam objetos que têm um hash: um número calculado a partir do conteúdo, que o Python usa
para achar o objeto rápido, sem percorrer tudo. Com `frozen=True` e o `==` por conteúdo, o
`@dataclass` também escreve o `__hash__`, calculado a partir de `x` e `y`.

Os algoritmos precisam disso. O que cava o labirinto guarda as células já visitadas num `set`:

```python
visited = {Cell(0, 0)}
Cell(0, 0) in visited    # True: mesmo conteúdo, mesmo hash
```

E se uma `Cell` pudesse mudar depois de entrar no `set`? O hash dela mudaria, mas ela continuaria
guardada no lugar calculado pelo hash antigo, e o `in` deixaria de encontrá-la. Por isso o
Python só dá hash automático a uma dataclass congelada.

### `slots=True`: só `x` e `y`, nada mais

Normalmente, cada objeto Python carrega um dicionário (`__dict__`) com os seus atributos, onde
cabe qualquer atributo novo. Com `slots=True`, a classe reserva espaço só para `x` e `y`, sem
dicionário: cada célula ocupa menos memória e não aceita atributos inventados, como um
`cell.cor = "azul"` por engano. O `slots=True` da dataclass existe desde o Python 3.10, a versão
mínima do projeto.

## `step`: a vizinha, sem conferir limites

```python
    def step(self, direction: Direction) -> "Cell":
        return Cell(self.x + direction.dx, self.y + direction.dy)
```

Recebe um lado (`Direction`, da [página anterior](./03-direction-propriedades.md)) e soma o
deslocamento desse lado à posição: `dx` à coluna, `dy` à linha. Devolve uma `Cell` nova; a
original não muda.

![Os quatro passos a partir da célula 3,4: Norte dá 3,3, Leste 4,4, Sul 3,5 e Oeste 2,4](/img/value-objects/cell-step.svg)

A `Cell` não sabe o tamanho da grade, então `step` **não confere limites**. Do canto `0,0`, o
passo para o Norte dá `0,-1`, uma posição que não existe:

![Do canto 0,0, o passo para o Norte dá 0,-1 e o passo para o Oeste dá -1,0, as duas fora da grade](/img/value-objects/cell-step-canto.svg)

Quem sabe o tamanho da grade é o `Maze`, a grade de paredes
([parte 5](../05-maze/03-vizinhos.md)): o método `Maze.neighbour` chama `step` e devolve `None`
quando o resultado cai fora. Cada classe responde pelo que conhece.

## `as_tuple`: a saída do `mazegen`

```python
    def as_tuple(self) -> tuple[int, int]:
        return (self.x, self.y)
```

Quem usa o gerador de fora recebe as posições como tuplas: a entrada é passada como
`entry=(0, 0)`, e as células do "42" saem como um conjunto de tuplas. `as_tuple` faz a conversão
no ponto em que uma célula sai do pacote. `tuple[int, int]` é a anotação de "tupla de dois
inteiros".

## O arquivo completo

```python title="mazegen/value_objects/cell.py"
"""Position of a cell in the maze grid."""

from dataclasses import dataclass

from mazegen.value_objects.direction import Direction


@dataclass(frozen=True, slots=True)
class Cell:
    """Immutable grid position, origin at the top-left corner.

    Attributes:
        x: Column, from 0.
        y: Row, from 0.
    """

    x: int
    y: int

    def step(self, direction: Direction) -> "Cell":
        """Cell next to this one towards a side, without bounds checking.

        Args:
            direction: Side to move to.

        Returns:
            The neighbouring position; the Maze decides whether it exists.
        """
        return Cell(self.x + direction.dx, self.y + direction.dy)

    def as_tuple(self) -> tuple[int, int]:
        """Plain coordinates used outside the mazegen package.

        Returns:
            The pair (x, y).
        """
        return (self.x, self.y)
```

## Experimente

Com o arquivo acima gravado em `mazegen/value_objects/cell.py`, na raiz do projeto
([como rodar os exemplos](../00-introducao/03-pre-requisitos.md#como-rodar-os-exemplos)):

```bash
.venv/bin/python - <<'EOF'
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction

cell = Cell(3, 4)
print(cell.step(Direction.NORTH), cell.step(Direction.WEST).as_tuple())
print(Cell(0, 0).step(Direction.NORTH))
print(cell == Cell(3, 4), len({cell, Cell(3, 4)}))
print(hasattr(cell, "__dict__"))
EOF
```

```text
Cell(x=3, y=3) (2, 4)
Cell(x=0, y=-1)
True 1
False
```

- Um passo ao Norte de `3,4` dá `3,3`; um passo a Oeste dá `2,4`.
- Do canto `0,0`, o Norte dá `0,-1`, fora da grade, sem erro nenhum.
- `{cell, Cell(3, 4)}` monta um `set` com duas células de mesmo conteúdo. Elas são iguais e têm
  o mesmo hash, então o `set` guarda uma só, e o `len` dá 1.
- `hasattr(objeto, nome)` responde se o objeto tem aquele atributo. Com `slots=True`, a célula
  não tem `__dict__`.
