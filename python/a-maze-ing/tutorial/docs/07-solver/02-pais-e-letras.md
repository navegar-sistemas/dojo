---
sidebar_position: 2
title: Pais, letras e desempate
---

# Pais, letras e desempate

A busca em largura descobre **a que distância** está a saída. Para devolver o caminho, ela
precisa lembrar **de onde** veio cada célula.

## O dicionário `parents`

Quando uma célula é descoberta, o `Solver` anota no dicionário `parents`:

- a chave é a célula descoberta;
- o valor é o par `(célula anterior, lado do passo)`;
- a entrada tem valor `None`: ela não veio de lugar nenhum.

O mesmo dicionário serve para saber se uma célula já foi descoberta (`nxt not in parents`), então
não é preciso um `set` de visitadas à parte.

Num labirinto perfeito 6x4 (`seed=7`), a letra em cada célula é o lado do passo que a descobriu:
`E` quer dizer "cheguei aqui andando para Leste a partir da vizinha de Oeste".

![Labirinto 6 por 4 com a letra do passo de descoberta em cada célula e o caminho em ciano](/img/solver/pais.svg)

## Do fim para o começo

Com `parents` pronto, o caminho sai de trás para a frente:

1. começa na saída e lê o par `(anterior, lado)`;
2. anota a letra do lado e vai para a célula anterior;
3. repete até chegar à entrada, cujo valor é `None`;
4. inverte a lista de letras.

Na figura, partindo da saída `(5, 3)`, as letras lidas são `S`, `E`, `S`, `W`, ... Invertidas,
dão o caminho da entrada até a saída: `SEESENNEESWSES`. A letra de cada passo vem de
`Direction.letter` (parte 4).

## Vários caminhos do mesmo tamanho

No modo Pac-Man pode haver mais de um caminho mais curto. Numa grade 3x2 toda aberta, de `(0, 0)`
até `(2, 1)`, há três caminhos de 3 passos:

![Três quadros da grade 3 por 2: EES, o escolhido; ESE e SEE, do mesmo tamanho](/img/solver/empate-3x2.svg)

O `Solver` escolhe sempre o mesmo, por duas regras:

- **vizinhos na ordem N, E, S, W.** `maze.passages(cell)` devolve os lados abertos sempre nessa
  ordem (é a ordem de iteração de `Direction`), então as vizinhas entram na fila sempre na mesma
  ordem;
- **vale o pai da primeira descoberta.** Uma célula que já está em `parents` nunca é
  reescrita.

Na grade 3x2, a partir de `(0, 0)`, o Leste é visto antes do Sul, e o Leste continua sendo
preferido nas camadas seguintes: o resultado é `EES`. Na volta, de `(2, 1)` para `(0, 0)`, o
Norte vem primeiro: `NWW`.

A mesma grade dá sempre a mesma string. O arquivo de saída e a tela usam o mesmo `solution`, então
mostram o mesmo caminho.

## Experimente

Na raiz do projeto, com `.venv/bin/python`:

```python
from mazegen.entities.maze import Maze
from mazegen.services.solver import Solver
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(3, 2, Pattern42.for_size(3, 2))
for x in range(3):
    maze.open_wall(Cell(x, 0), Direction.SOUTH)
    if x < 2:
        maze.open_wall(Cell(x, 0), Direction.EAST)
        maze.open_wall(Cell(x, 1), Direction.EAST)
print(maze.rows())
print(Solver().shortest_path(maze, Cell(0, 0), Cell(2, 1)))
print(Solver().shortest_path(maze, Cell(2, 1), Cell(0, 0)))
```

```text
[[9, 1, 3], [12, 4, 6]]
EES
NWW
```
