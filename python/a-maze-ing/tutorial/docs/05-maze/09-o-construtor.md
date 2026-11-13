---
sidebar_position: 2
title: O construtor
---

# O construtor

Antes de abrir qualquer parede, o `Maze` (a grade de paredes, da
[página anterior](./01-a-grade-de-paredes.md)) precisa existir: saber o tamanho da grade, saber
quais células desenham o "42" e criar todas as células com as quatro paredes fechadas, o valor
`ALL_WALLS = 15`. Esta página escreve o construtor, `__init__`, e começa o arquivo
`mazegen/entities/maze.py`.

```python
    def __init__(self, width: int, height: int, pattern: Pattern42) -> None:
        self.width = width
        self.height = height
        self.pattern = pattern
        self._walls: list[list[int]] = [
            [ALL_WALLS] * width for _ in range(height)
        ]
```

- `width`, `height` e `pattern` ficam públicos: os algoritmos leem o tamanho da grade e as
  células do "42" (o `Pattern42`, construído na
  [parte 4](../04-value-objects/05-pattern42-posicao.md)).
- `_walls` é a grade: uma lista com uma lista por linha, cada uma com `width` números. A
  anotação `list[list[int]]` diz isso ao mypy: uma lista de listas de inteiros.
- `_walls[y][x]` são as paredes da célula `x,y`: primeiro se escolhe a linha (`y`), depois a
  coluna (`x`). É a mesma ordem do arquivo de saída, linha por linha.
- `-> None` diz que o construtor não devolve nada.

O `Maze` recebe o `Pattern42` pronto, em vez de calculá-lo. Quem cria o `Maze` (o
`MazeGenerator`, [parte 9](../09-gerador/01-a-fachada.md)) já calculou o padrão antes, para
conferir que a entrada e a saída não caem no "42", e o mesmo objeto serve aos dois.

Um `Maze` 3x2 recém-criado, com o valor de cada célula (as linhas grossas são paredes
fechadas):

![Um Maze 3 por 2 recém-criado, todas as células valendo 15](/img/maze/abrir-antes.svg)

### O `_` de `_walls`

O sublinhado no começo do nome é a convenção do Python para "interno: não mexa de fora". Os
algoritmos não escrevem em `_walls` diretamente. Eles leem com `walls(cell)` e mudam com
`open_wall` e `close_wall`, os únicos métodos que alteram a grade. É assim que a classe garante
as regras: todo caminho de mudança passa por código que as confere.

### Uma lista nova por linha

`[ALL_WALLS] * width` cria uma lista com `width` cópias de 15. A forma curta para a grade toda,
`[[ALL_WALLS] * width] * height`, parece igual, mas está errada: o `* height` repete **a mesma
lista** `height` vezes. Mudar uma linha muda todas:

```python
rows = [[15] * 3] * 2
rows[0][0] = 13
print(rows)
rows = [[15] * 3 for _ in range(2)]
rows[0][0] = 13
print(rows)
```

```text
[[13, 15, 15], [13, 15, 15]]
[[13, 15, 15], [15, 15, 15]]
```

Na primeira forma, mudar a célula `0,0` mudou também a `0,1`. A versão com
`for _ in range(height)` cria uma lista **nova** a cada volta. O `_` é o nome que se dá a uma
variável que não é usada: só importa repetir `height` vezes.

Essa forma, com um `for` dentro dos colchetes, se chama **compreensão de lista** (*list
comprehension*): ela monta uma lista calculando a expressão da esquerda (`[15] * 3`) a cada
volta do `for`. Equivale a começar com uma lista vazia e fazer um `append` por volta.

Dentro de uma linha, `[ALL_WALLS] * width` não tem esse problema: os elementos são inteiros, e um
inteiro não muda, só é trocado por outro.

## O começo do arquivo

O `Maze` é construído aos poucos, ao longo desta parte, num único arquivo. Crie agora
`mazegen/entities/maze.py` com o que esta página mostrou:

```python
"""Mutable grid of wall masks, the state the generator carves."""

from mazegen.value_objects.pattern42 import Pattern42

ALL_WALLS = 15


class Maze:
    def __init__(self, width: int, height: int, pattern: Pattern42) -> None:
        self.width = width
        self.height = height
        self.pattern = pattern
        self._walls: list[list[int]] = [
            [ALL_WALLS] * width for _ in range(height)
        ]
```

- A primeira linha é a docstring do módulo (o texto que documenta o arquivo).
- O `import` traz o `Pattern42`, usado na anotação do parâmetro `pattern`.

Cada página seguinte acrescenta métodos **dentro** da classe `Maze`, depois dos que já estão lá,
com a mesma indentação do `__init__` (4 espaços). Quando um método novo precisa de algo de outro
arquivo, a página mostra o `import` que entra no topo. A última página desta parte,
[A cópia da grade](./08-a-copia-da-grade.md), termina com o arquivo completo: o mesmo que se
monta aqui, mais as docstrings de cada método.

## Experimente

Com o arquivo acima gravado, na raiz do projeto (a página
[Como rodar os exemplos](../00-introducao/03-pre-requisitos.md#como-rodar-os-exemplos) explica
o formato):

```bash
.venv/bin/python - <<'EOF'
from mazegen.entities.maze import Maze
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(9, 7, Pattern42.for_size(9, 7))
print(maze.width, maze.height, len(maze.pattern.cells))
EOF
```

```text
9 7 18
```

Uma grade de 9 colunas por 7 linhas, com as 18 células do "42".
