---
sidebar_position: 2
title: O caminho em células
---

# O caminho em células

O caminho mais curto vem do gerador como **letras**: `EES` quer dizer "um passo para a direita
(Leste), outro para a direita, um para baixo (Sul)". O arquivo de saída grava exatamente essas
letras. O desenho na tela, porém, precisa saber **por quais células** passa a linha ciano
([parte 13](../13-tela/05-o-caminho-em-ciano.md)). Esta página cria o método `path()` do
retrato, que traduz as letras em células.

## A tradução, passo a passo

Um exemplo pequeno: uma grade de 3 colunas por 2 linhas sem nenhuma parede por dentro (só a
borda), com a entrada em `0,0`, a saída em `2,1` e o caminho `EES`. É outro 3x2, diferente do
exemplo `d53`/`d56` da [parte 1](../01-o-problema/04-o-arquivo-de-saida.md): esta grade é
escrita à mão, toda aberta, para o caminho ficar simples.

![Grade 3 por 2 sem paredes internas, com o caminho EES e a posição de cada célula na lista do caminho](/img/geracao/caminho-3x2.svg)

Na figura, a linha cheia é a borda e o tracejado marca as paredes abertas. A célula magenta é a
entrada, a vermelha é a saída e a linha ciano é o caminho. O número em cada célula é a posição
dela na lista que `path()` devolve: 0 é a entrada, 3 é a saída.

`SEE` também chegaria à saída em 3 passos. O caminho aqui é dado, mas é o que o *solver* da
[parte 7](../07-solver/01-busca-em-largura.md) acharia: ele olha as vizinhas na ordem N, E, S,
W, e por isso anda para o Leste antes de descer.

Cada letra move um passo a partir da célula atual. Andar para a direita soma 1 ao `x` (a
coluna); andar para baixo soma 1 ao `y` (a linha), porque o `y` cresce para baixo:

| Passo | Letra | Quanto muda: `dx`, `dy` | Célula |
|---|---|---|---|
| início | | | `(0, 0)` |
| 1 | `E` | `dx = 1`, `dy = 0` | `(1, 0)` |
| 2 | `E` | `dx = 1`, `dy = 0` | `(2, 0)` |
| 3 | `S` | `dx = 0`, `dy = 1` | `(2, 1)` |

Três letras viram quatro células: a entrada, mais uma por passo. A última é a saída.

## Da letra à direção

O `mazegen` já tem a `Direction`, que representa os quatro lados de uma célula: `NORTH`,
`EAST`, `SOUTH` e `WEST` ([parte 4](../04-value-objects/03-direction-propriedades.md)). Cada um
sabe a sua letra (`letter`) e o seu deslocamento (`dx` e `dy`). `Direction.EAST.letter` é `"E"`,
`Direction.EAST.dx` é `1`.

Falta o caminho inverso: dada a letra, achar a direção. Um dicionário, montado uma vez quando o
arquivo é carregado, faz isso:

```python
_BY_LETTER = {side.letter: side for side in Direction}
```

- `Direction` é um `Enum` (um conjunto fechado de valores com nome), e percorrer um `Enum` com
  `for` dá os seus membros, um por vez.
- `{chave: valor for ...}` é uma *dict comprehension*: monta um dicionário com uma entrada por
  volta do `for`. O resultado é
  `{"N": Direction.NORTH, "E": Direction.EAST, "S": Direction.SOUTH, "W": Direction.WEST}`.

Montar o dicionário **a partir** da `Direction`, em vez de escrever as quatro entradas à mão,
garante que as letras e os deslocamentos são os mesmos que o gerador usou para escrever o
caminho.

## O método

```python
def path(self) -> list[tuple[int, int]]:
    x, y = self.entry
    cells = [(x, y)]
    for letter in self.solution:
        side = _BY_LETTER[letter]
        x, y = x + side.dx, y + side.dy
        cells.append((x, y))
    return cells
```

1. `x, y = self.entry` separa a tupla da entrada nos seus dois números.
2. `cells` começa com a entrada, que já é a primeira célula do caminho.
3. Para cada letra de `solution`, o dicionário dá a direção.
4. `x, y = x + side.dx, y + side.dy` calcula a célula seguinte: as duas somas são feitas antes
   de qualquer atribuição, e os dois nomes recebem os novos valores juntos.
5. A célula nova entra no fim da lista.

O resultado tem sempre `len(solution) + 1` células, da entrada à saída.

### Por que recalcular em vez de guardar

As células do caminho poderiam ser mais um campo do retrato. Mas elas saem das letras: guardar
as duas formas abriria espaço para elas discordarem, por um erro em algum lugar. Com `path()`,
há uma fonte só, o `solution`, e a tela desenha exatamente o caminho que o arquivo grava.
Recalcular é barato: uma soma por passo, e mesmo numa grade 100x100 o caminho tem no máximo
10 000 células.

## O arquivo completo

`MazeGenerator` é importado de `mazegen`, o nome público do pacote. `Direction` é importada pelo
caminho interno (`mazegen.value_objects.direction`), porque o pacote só oferece diretamente
`MazeGenerator` e `MazeError`. A aplicação mora no mesmo repositório e muda junto com o
`mazegen`, por isso pode usar o caminho interno; um projeto de fora, que instala o pacote, não
deveria ([parte 11](../11-configuracao/08-o-maze-config-completo.md)).

```python title="amazeing/domain/value_objects/generated_maze.py"
"""Immutable snapshot of one generation."""

from dataclasses import dataclass

from mazegen import MazeGenerator
from mazegen.value_objects.direction import Direction

_BY_LETTER = {side.letter: side for side in Direction}


@dataclass(frozen=True)
class GeneratedMaze:
    """What the output file stores and the screen draws for one maze.

    The file and the screen always start from the same snapshot, so they
    cannot disagree.

    Attributes:
        grid: height rows of width wall masks.
        entry: Entry cell as (x, y).
        exit: Exit cell as (x, y).
        solution: Shortest path from entry to exit, one letter per step.
        pattern: (x, y) cells of the "42"; empty when it does not fit.
    """

    grid: tuple[tuple[int, ...], ...]
    entry: tuple[int, int]
    exit: tuple[int, int]
    solution: str
    pattern: frozenset[tuple[int, int]]

    @classmethod
    def from_generator(cls, generator: MazeGenerator, entry: tuple[int, int],
                       exit: tuple[int, int]) -> "GeneratedMaze":
        """Copy the result of the last generate() call.

        Args:
            generator: Generator right after generate().
            entry: Entry cell as (x, y).
            exit: Exit cell as (x, y).

        Returns:
            The snapshot.
        """
        return cls(tuple(tuple(row) for row in generator.grid), entry, exit,
                   generator.solution, frozenset(generator.pattern))

    def path(self) -> list[tuple[int, int]]:
        """Cells of the shortest path, rebuilt from entry and solution.

        Returns:
            len(solution) + 1 cells, from entry to exit.
        """
        x, y = self.entry
        cells = [(x, y)]
        for letter in self.solution:
            side = _BY_LETTER[letter]
            x, y = x + side.dx, y + side.dy
            cells.append((x, y))
        return cells
```

## Experimente

Os exemplos rodam na raiz do projeto. O primeiro mostra que o retrato não muda quando o gerador
gera de novo, e que a grade dele não aceita alteração:

```bash
.venv/bin/python -c '
from amazeing.domain.value_objects.generated_maze import GeneratedMaze
from mazegen import MazeGenerator

generator = MazeGenerator(6, 4, seed=1)
generator.generate()
maze = GeneratedMaze.from_generator(generator, (0, 0), (5, 3))
print(maze.solution)
generator.generate()
print(generator.solution)
print(maze.solution)
try:
    maze.grid[0][0] = 15
except TypeError as error:
    print(error)
'
```

```text
EESEEESS
EEEEESSS
EESEEESS
'tuple' object does not support item assignment
```

A segunda geração trocou o caminho do gerador; o retrato continua com o da primeira.

O segundo cria o retrato direto pelo construtor, sem gerar labirinto nenhum, com a grade da
figura: duas linhas de três células, cada uma com o número das suas paredes fechadas.

```bash
.venv/bin/python -c '
from amazeing.domain.value_objects.generated_maze import GeneratedMaze

maze = GeneratedMaze(((9, 1, 3), (12, 4, 6)), (0, 0), (2, 1), "EES",
                     frozenset())
print(maze.path())
'
```

```text
[(0, 0), (1, 0), (2, 0), (2, 1)]
```
