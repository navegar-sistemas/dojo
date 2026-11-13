---
sidebar_position: 6
title: Passagens e becos
---

# Passagens e becos

Os algoritmos que andam pelo labirinto precisam saber por onde se pode sair de uma célula, e o
modo Pac-Man precisa achar os **becos sem saída** para abri-los. Esta página escreve os três
métodos que respondem: `passages`, `closed_sides` e `dead_ends`. Os três entram na classe
`Maze`, depois dos da [página anterior](./04-abrir-e-fechar.md), e não precisam de import novo.

## `passages`: os lados abertos

```python
    def passages(self, cell: Cell) -> list[Direction]:
        return [side for side in Direction if self.is_open(cell, side)]
```

Devolve os lados da célula por onde se pode andar: os que são passagem segundo o `is_open`
([Vizinhos](./03-vizinhos.md)).

A linha é uma compreensão de lista (a lista montada por um `for` entre colchetes, explicada no
[construtor](./09-o-construtor.md)), agora com um `if` no fim: "a lista de cada `side` de
`Direction` para o qual `is_open` é verdadeiro". Os lados em que o `if` dá falso ficam de fora. Como `for side in Direction` percorre os lados na ordem
`N, E, S, W` ([parte 4](../04-value-objects/02-direction-bits.md)), a lista sai sempre nessa
ordem. O `Solver` ([parte 7](../07-solver/01-busca-em-largura.md)) anda pelo labirinto com ela,
e a ordem fixa garante que o mesmo labirinto dê sempre o mesmo caminho mais curto.

## `closed_sides`: as paredes que **poderiam** abrir

```python
    def closed_sides(self, cell: Cell) -> list[Direction]:
        return [
            side for side in Direction
            if self.neighbour(cell, side) is not None
            and self.walls(cell) & side
        ]
```

Devolve os lados fechados **que têm uma célula do labirinto do outro lado**: há vizinha
(`neighbour` não é `None`) e o bit da parede está ligado (`walls(cell) & side` diferente de 0).

Uma parede da borda, ou voltada para o "42", está fechada, mas não entra na lista: ela nunca pode
ser aberta. Por isso `passages` e `closed_sides` juntos nem sempre cobrem os quatro lados. O que
falta são justamente as paredes permanentes.

## Beco sem saída

Relembrando a [parte 1](../01-o-problema/05-perfeito-e-pac-man.md): um **beco sem saída** é uma
célula com exatamente uma passagem. Quem entra só consegue sair por onde entrou. No modo Pac-Man,
o enunciado pede becos raros, no máximo um ou dois, porque num beco o jogador fica encurralado.
O `Braider` ([parte 8](../08-braider/01-becos-sem-saida.md)) precisa achá-los para abri-los, e o
gerador precisa contá-los.

Mas nem todo beco é igual:

- **beco real**: tem pelo menos uma parede fechada que dá para uma célula do labirinto. Abrir
  essa parede acaba com o beco.
- **beco cercado**: todas as suas paredes fechadas dão para a borda ou para o "42". Não há o que
  abrir, então ele não conta.

O "42" sempre cria dois becos cercados: as duas células dentro das curvas do "2" (no desenho
7x5 do "42", a coluna 5 das linhas 1 e 3) estão cercadas pelo "42" por três lados e só têm uma
vizinha livre. Na grade 9x7 da figura, o desenho começa em `1,1`, e essas duas células são a
`6,2` e a `6,4`, em amarelo. Em laranja estão os becos reais; em cinza, o "42":

![Labirinto 9 por 7 com os becos reais em laranja e os cercados em amarelo](/img/maze/becos-9x7.svg)

## `dead_ends`: só os reais

```python
    def dead_ends(self) -> list[Cell]:
        return [
            cell for cell in self.cells()
            if len(self.passages(cell)) == 1 and self.closed_sides(cell)
        ]
```

Devolve as células do labirinto (as de `cells()`, que já pula o "42") com uma passagem **e** pelo
menos uma parede que pode abrir.

No Python, uma lista vazia conta como **falso** num `if`, e uma lista com elementos conta como
verdadeiro. Então `and self.closed_sides(cell)` descarta os becos cercados (lista vazia) sem
precisar escrever `len(...) > 0`.

É a mesma definição que o `maze_analyzer.py` (o programa que vem com o enunciado para conferir o
arquivo de saída) usa: ele conta os becos cercados à parte, como tolerados.

## Experimente

A serpentina 3x2: um corredor só, que vai até o fim da primeira linha e volta pela segunda. Na
figura, as linhas grossas são paredes fechadas, as tracejadas são passagens, e os becos reais
estão em laranja:

![A serpentina 3 por 2, com os dois becos reais em laranja](/img/maze/ciclos-serpentina.svg)

Com os três métodos no `maze.py`, na raiz do projeto:

```bash
.venv/bin/python - <<'EOF'
from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(3, 2, Pattern42.for_size(3, 2))
for cell, side in [(Cell(0, 0), Direction.EAST), (Cell(1, 0), Direction.EAST),
                   (Cell(2, 0), Direction.SOUTH), (Cell(2, 1), Direction.WEST),
                   (Cell(1, 1), Direction.WEST)]:
    maze.open_wall(cell, side)
print([maze.walls(cell) for cell in maze.cells()])
print([side.letter for side in maze.passages(Cell(0, 0))],
      [side.letter for side in maze.closed_sides(Cell(0, 0))])
print([cell.as_tuple() for cell in maze.dead_ends()])
small = Maze(2, 1, Pattern42.for_size(2, 1))
small.open_wall(Cell(0, 0), Direction.EAST)
print(small.dead_ends())
EOF
```

```text
[13, 5, 3, 13, 5, 6]
['E'] ['S']
[(0, 0), (0, 1)]
[]
```

- O `for` abre as cinco paredes da serpentina, uma por par (célula, lado). A primeira linha
  impressa traz o valor de cada célula, na ordem de `cells()`: primeiro a linha 0, depois a 1.
- `0,0` tem uma passagem (Leste) e uma parede que pode abrir (Sul, para `0,1`): é um beco real.
  O Norte e o Oeste são borda, por isso não aparecem em nenhuma das duas listas.
- `0,1` é o outro beco real, na ponta de baixo da serpentina.
- Na grade 2x1 com a parede do meio aberta, as duas células também têm uma passagem só, mas todas
  as suas paredes fechadas dão para a borda: são becos cercados, e `dead_ends()` devolve uma lista
  vazia.
