---
sidebar_position: 4
title: A seed e o random.Random único
---

# A seed e o random.Random único

## O que o subject exige

"O labirinto deve ser gerado aleatoriamente, mas a reprodutibilidade via seed é obrigatória."
Com a mesma `SEED`, o programa tem de gerar o mesmo labirinto, byte a byte, em qualquer execução.

## Um gerador de números só seu

O módulo `random` tem funções soltas (`random.choice`, `random.shuffle`) que usam um gerador
**global**, compartilhado com qualquer outro código do processo. Se outra biblioteca sorteia
alguma coisa no meio, a sequência muda.

`random.Random(seed)` cria um gerador **independente**, com o próprio estado. Duas instâncias
criadas com a mesma seed produzem exatamente a mesma sequência de números.

O `mazegen` usa um único `random.Random`:

1. o `MazeGenerator` cria esse objeto no construtor, com a seed recebida (parte 9);
2. ele é passado como parâmetro `rng` ao `Carver` e, no modo Pac-Man, ao `Braider`;
3. nenhum outro lugar do pacote sorteia nada nem cria outro `Random`.

O `Carver` não guarda o `rng` nem cria o seu: recebe por parâmetro. Assim, quem decide de onde
vem a aleatoriedade é quem chama, e a seed controla a geração inteira.

![Três labirintos 8 por 5: Random(1), Random(2) e de novo Random(1), o primeiro e o terceiro iguais](/img/carver/seeds.svg)

## O que mais precisa ser fixo

A seed só garante a mesma sequência de números. Para o labirinto sair igual, cada número tem de
ser usado do mesmo jeito em toda execução:

- **A lista sorteada está sempre na mesma ordem.** `rng.choice(options)` sorteia uma posição da
  lista. `options` é montada percorrendo `Direction`, sempre na ordem Norte, Leste, Sul, Oeste.
  Se a ordem mudasse, o mesmo número escolheria outro lado.
- **O `set` só é consultado.** `visited` é um `set`, e a ordem em que um `set` entrega seus
  elementos não é algo em que o código deva confiar. O `Carver` só pergunta `nxt not in visited`;
  nunca percorre o conjunto, então essa ordem não decide nada.
- **Cada sorteio acontece no mesmo ponto do laço**, um por avanço.

## Experimente

Na raiz do projeto, com `.venv/bin/python`:

```python
import random

from mazegen.entities.maze import Maze
from mazegen.services.carver import Carver
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.pattern42 import Pattern42


def carved(seed):
    maze = Maze(20, 15, Pattern42.for_size(20, 15))
    Carver().carve(maze, Cell(0, 0), random.Random(seed))
    return maze


print(carved(7).rows() == carved(7).rows())
print(carved(7).rows() == carved(8).rows())
maze = carved(7)
print(maze.loop_count(), len(list(maze.cells())))
```

```text
True
False
0 282
```

A mesma seed dá a mesma grade, outra seed dá outra, e o resultado é uma árvore: 0 ciclos
cobrindo as 282 células livres (300 da grade menos as 18 do "42").
