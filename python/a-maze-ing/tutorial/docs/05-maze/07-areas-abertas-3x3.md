---
sidebar_position: 7
title: Áreas abertas 3x3
---

# Áreas abertas 3x3

## A regra

O subject proíbe áreas abertas grandes: nenhum bloco de 3x3 células pode ter **todas** as
paredes internas abertas. Blocos 2x2, 2x3 e 3x2 abertos são permitidos.

Um bloco 3x3 tem 12 paredes internas: entre as 3 colunas há 2 linhas de paredes verticais, com 3
paredes cada (6), e entre as 3 linhas há 2 linhas de paredes horizontais, também com 3 cada (6).

![Um bloco 3 por 3 com as 12 paredes internas abertas](/img/maze/janela-3x3-aberta.svg)

Basta **uma** parede interna fechada para o bloco deixar de ser uma área aberta:

![O mesmo bloco com a parede entre 1,1 e 2,1 fechada](/img/maze/janela-3x3-fechada.svg)

O modo perfeito nunca forma um 3x3 aberto: 12 passagens entre 9 células exigiriam ciclos, e uma
árvore não tem ciclo. No modo Pac-Man, o `Braider` (parte 8) abre paredes extras, e depois de
cada uma pergunta ao `Maze` se algum 3x3 ficou aberto.

## `has_open_3x3`: todas as janelas

```python
    def has_open_3x3(self) -> bool:
        for y0 in range(self.height - 2):
            for x0 in range(self.width - 2):
                if self._window_open(x0, y0):
                    return True
        return False
```

Uma **janela** é um bloco 3x3 identificado pelo canto de cima à esquerda, `(x0, y0)`. O canto vai
até `width - 3` e `height - 3`, para a janela caber na grade: `range(self.width - 2)` para logo
antes de `width - 2`. Numa grade 5x4 há 3 x 2 = 6 janelas:

![Uma das seis janelas 3 por 3 de uma grade 5 por 4](/img/maze/janelas-5x4.svg)

Numa grade com menos de 3 colunas ou 3 linhas, o `range` fica vazio, e a resposta é `False`.

## `_window_open`: uma janela

```python
    def _window_open(self, x0: int, y0: int) -> bool:
        for y in range(y0, y0 + 3):
            for x in range(x0, x0 + 3):
                walls = self.walls(Cell(x, y))
                if x < x0 + 2 and walls & Direction.EAST:
                    return False
                if y < y0 + 2 and walls & Direction.SOUTH:
                    return False
        return True
```

Cada parede interna é contada **uma vez**, pela célula de cima ou da esquerda:

- as paredes verticais são o **Leste** das células das duas primeiras colunas (`x < x0 + 2`);
- as horizontais são o **Sul** das células das duas primeiras linhas (`y < y0 + 2`).

Pela coerência, olhar o Leste de `(x, y)` é o mesmo que olhar o Oeste de `(x + 1, y)`, então não
é preciso conferir os dois lados. A coluna da direita e a linha de baixo não têm parede interna
a conferir: o Leste e o Sul delas ficam fora da janela.

Uma janela com célula do "42" nunca está aberta: a célula do "42" tem as quatro paredes
fechadas, e a primeira leitura já devolve `False`.

### Parar na primeira parede fechada

O `return False` sai na **primeira** parede fechada encontrada. Num labirinto, quase toda janela
tem uma parede fechada logo no começo, então a maioria custa uma ou duas leituras, em vez de 12.

Isso importa porque o `Braider` chama `has_open_3x3` depois de **cada** parede que abre, e cada
chamada percorre todas as janelas. Numa grade 100x100 são 98 x 98 = 9 604 janelas por chamada;
com a saída antecipada, uma chamada leva poucos milissegundos.

### Por que olhar a grade inteira

Uma parede aberta só pode criar um 3x3 aberto nas janelas que a contêm, e bastaria olhar essas.
Seria mais rápido, mas exige calcular quais janelas tocam a parede, perto das bordas inclusive.
Percorrer todas é mais simples de ler e de conferir, e com a saída antecipada já é rápido o
bastante.

## Experimente

```python
from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(3, 3, Pattern42.for_size(3, 3))
for y in range(3):
    for x in range(3):
        if x < 2:
            maze.open_wall(Cell(x, y), Direction.EAST)
        if y < 2:
            maze.open_wall(Cell(x, y), Direction.SOUTH)
print(maze.rows(), maze.has_open_3x3(), maze.loop_count())
maze.close_wall(Cell(1, 1), Direction.EAST)
print(maze.has_open_3x3())
```

```text
[[9, 1, 3], [8, 0, 2], [12, 4, 6]] True 4
False
```

A célula do meio vale `0`: as quatro paredes abertas. Os 4 ciclos são os quatro quadrados 2x2
dentro do bloco.
