---
sidebar_position: 6
title: Contar ciclos
---

# Contar ciclos

## O que mede

O modo Pac-Man exige pelo menos **dois ciclos independentes**: rotas alternativas, para o
jogador poder fugir dando a volta. `loop_count` conta esses ciclos, e o gerador (parte 9) confere
o resultado depois do braiding.

## A conta

Pense no labirinto como um grafo: as células são os pontos, e as passagens são as ligações entre
eles.

- Um labirinto **perfeito** é uma árvore: liga `n` células com exatamente `n - 1` passagens, e
  não tem ciclo nenhum.
- Cada passagem **a mais**, entre duas células já ligadas, cria uma rota nova: um ciclo
  independente.

Então, num labirinto em que toda célula é alcançável:

```text
ciclos = passagens - células + 1
```

Na serpentina 3x2, 6 células e 5 passagens: `5 - 6 + 1 = 0`.

![A serpentina 3 por 2: 5 passagens e nenhum ciclo](/img/maze/ciclos-serpentina.svg)

Abrindo as duas paredes Sul que faltam, 7 passagens: `7 - 6 + 1 = 2`. Os dois ciclos são os dois
quadrados 2x2, e o maior, em volta da grade inteira, não conta: ele é a combinação dos dois.

![A grade 3 por 2 com todas as paredes internas abertas: 2 ciclos](/img/maze/ciclos-dois.svg)

## O código

```python
    def loop_count(self) -> int:
        ends = 0
        count = 0
        for cell in self.cells():
            ends += len(self.passages(cell))
            count += 1
        return ends // 2 - count + 1
```

Um único passeio pelas células soma duas coisas:

- `ends`: as pontas de passagem. Cada passagem tem **duas** pontas, uma em cada célula, e é
  contada uma vez em cada uma. Por isso o número de passagens é `ends // 2`.
- `count`: as células fora do "42". O `cells()` já pula o "42", que não faz parte do grafo.

### A condição: tudo conectado

A fórmula só vale com todas as células alcançáveis. O `Carver` (parte 6) garante isso, porque
visita toda célula livre, e o braiding só abre paredes, nunca fecha uma passagem da árvore.
Numa grade recém-criada, sem passagem nenhuma, a conta não mede ciclo nenhum: dá
`0 - células + 1`, um número negativo.

## Experimente

```python
from mazegen.entities.maze import Maze
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(3, 2, Pattern42.for_size(3, 2))
for cell, side in [(Cell(0, 0), Direction.EAST), (Cell(1, 0), Direction.EAST),
                   (Cell(2, 0), Direction.SOUTH), (Cell(2, 1), Direction.WEST),
                   (Cell(1, 1), Direction.WEST)]:
    maze.open_wall(cell, side)
print(maze.loop_count())
maze.open_wall(Cell(0, 0), Direction.SOUTH)
maze.open_wall(Cell(1, 0), Direction.SOUTH)
print(maze.loop_count(), maze.dead_ends())
```

```text
0
2 []
```

Com os dois ciclos, os becos da serpentina também somem: toda célula passa a ter duas
passagens ou mais.
