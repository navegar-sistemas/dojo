---
sidebar_position: 3
title: Consultar a grade
---

# Consultar a grade

Antes de abrir qualquer parede, os algoritmos fazem três perguntas simples ao `Maze` (a grade de
paredes, [apresentada no início desta parte](./01-a-grade-de-paredes.md)): esta posição existe
na grade? quais são as células do labirinto? quais paredes desta célula estão fechadas? Esta
página escreve os três métodos que respondem.

## Onde cada trecho entra

Os três métodos entram **dentro** da classe `Maze`, em `mazegen/entities/maze.py`, logo depois
do `__init__` escrito no [construtor](./09-o-construtor.md), com a mesma indentação (4 espaços).
Eles usam duas coisas de outros arquivos, então o topo do arquivo passa a ter três imports:

```python
from collections.abc import Iterator

from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42
```

- `Cell` é a posição `x,y` de uma célula ([parte 4](../04-value-objects/04-cell.md)).
- `Iterator` serve só para a anotação do método `cells`, explicada abaixo.
- A linha em branco separa os módulos da biblioteca padrão (o `collections`, que vem com o
  Python) dos módulos do próprio projeto, como pede a PEP 8, o guia de estilo do Python.

## `__contains__`: a posição está dentro da grade?

```python
    def __contains__(self, cell: object) -> bool:
        return (isinstance(cell, Cell) and 0 <= cell.x < self.width
                and 0 <= cell.y < self.height)
```

`__contains__` é o método especial que o Python chama no operador `in`: `cell in maze` vira
`maze.__contains__(cell)`. A resposta é `True` quando a posição existe: coluna de `0` a
`width - 1` e linha de `0` a `height - 1`.

- `isinstance(cell, Cell)` vem primeiro, como no `Pattern42`
  ([parte 4](../04-value-objects/06-pattern42-consulta.md)): só uma `Cell` pode estar dentro, e
  uma tupla ou uma lista respondem `False` sem erro.
- `0 <= cell.x < self.width` é uma **comparação encadeada**: o Python a lê como
  `0 <= cell.x and cell.x < self.width`, do jeito que se escreve em matemática.
- Os parênteses em volta da expressão inteira deixam quebrá-la em duas linhas, para não passar
  de 79 caracteres (o limite do flake8).

É a pergunta que a `Cell` não sabe responder: o `step` da `Cell`
([parte 4](../04-value-objects/04-cell.md)) devolve qualquer posição, inclusive fora da grade, e
o `Maze`, que conhece o tamanho, decide se ela existe.

## `cells`: as células do labirinto

```python
    def cells(self) -> Iterator[Cell]:
        for y in range(self.height):
            for x in range(self.width):
                cell = Cell(x, y)
                if cell not in self.pattern:
                    yield cell
```

Percorre a grade linha por linha (`y` por fora, `x` por dentro), a mesma ordem de leitura do
arquivo de saída, e **pula as células do "42"**. Elas não fazem parte do labirinto: não têm
passagem, não são becos, não contam nos ciclos.

Na figura, o número de cada célula é a ordem em que `cells()` a entrega, de 1 a 45; as células
cinza são as do "42", que ele pula:

![A ordem de cells() numa grade 9 por 7: linha por linha, pulando as 18 células do 42](/img/maze/cells-ordem-9x7.svg)

`cell not in self.pattern` usa o `__contains__` do `Pattern42`: "esta célula não é do 42?".

### `yield`: uma célula de cada vez

Uma função com `yield` é uma **função geradora** (em inglês, *generator*; não tem nada a ver com
o `MazeGenerator`, a classe que gera labirintos). Em vez de montar uma lista inteira e devolvê-la
no fim, ela entrega uma célula de cada vez, quando o `for` de quem chamou pede a próxima. Entre
um pedido e outro, a função fica pausada no `yield`, com as variáveis `x` e `y` guardadas.

O tipo de retorno é `Iterator[Cell]`: "algo que se percorre com `for` e entrega `Cell`s". O
`Iterator` vem do módulo `collections.abc`, o import que entrou no topo do arquivo.

Quem só quer percorrer as células (`for cell in maze.cells():`) não paga uma lista de 10 000
posições numa grade de 100x100. Quem precisa da lista inteira pede `list(maze.cells())`.

## `walls`: as paredes de uma célula

```python
    def walls(self, cell: Cell) -> int:
        return self._walls[cell.y][cell.x]
```

Devolve o número de 0 a 15 com as paredes fechadas da célula, um bit por lado. Note a ordem dos
índices: primeiro a linha (`y`), depois a coluna (`x`), porque `_walls` é uma lista de linhas.

`walls` só lê, e não confere limites: quem chama já sabe que a célula está na grade. Uma posição
fora daria `IndexError`, um erro do Python para índice inexistente.

## Experimente

Com os três métodos e os imports no `maze.py`, na raiz do projeto:

```bash
.venv/bin/python - <<'EOF'
from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(9, 7, Pattern42.for_size(9, 7))
print(Cell(8, 6) in maze, Cell(9, 0) in maze, (0, 0) in maze)
print(len(list(maze.cells())), 9 * 7 - len(maze.pattern.cells))
print([cell.as_tuple() for cell in maze.cells()][:5])
print(maze.walls(Cell(0, 0)))
EOF
```

```text
True False False
45 45
[(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
15
```

- `8,6` é o canto de baixo à direita de uma grade 9x7: está dentro. `9,0` está uma coluna além
  da última. A tupla `(0, 0)` não é uma `Cell`, então responde `False`.
- Uma grade 9x7 tem 63 posições; tirando as 18 do "42", o labirinto tem 45 células.
- `[cell.as_tuple() for cell in maze.cells()]` é uma compreensão de lista: a posição de cada
  célula, como tupla. O `[:5]` pega só as cinco primeiras, que vêm da linha 0, da esquerda para
  a direita.
- Uma grade recém-criada tem todas as paredes fechadas: 15.
