---
sidebar_position: 5
title: Abrir e fechar paredes
---

# Abrir e fechar paredes

Gerar o labirinto é abrir paredes, e o modo Pac-Man às vezes precisa fechar uma de volta. Cada
uma dessas mudanças pode quebrar uma regra do enunciado se for feita pela metade ou no lugar
errado. Esta página escreve os dois únicos métodos que mudam a grade, `open_wall` e
`close_wall`, e a guarda que os protege.

Os três métodos entram na classe `Maze`, depois dos da [página anterior](./03-vizinhos.md). A
guarda usa o `MazeError`, a exceção do gerador ([parte 4](../04-value-objects/01-maze-error.md)),
então o topo do arquivo ganha mais um import:

```python
from mazegen.errors import MazeError
```

## O erro mais fácil: mudar só um lado

Relembrando a **coerência**: a parede Leste de uma célula é **a mesma** parede que a Oeste da
vizinha da direita, mas o `Maze` a guarda duas vezes, uma em cada célula. O enunciado exige que
as duas anotações concordem.

Se o código abrir só o Leste da célula `0,0` (que passa de 15 para 13) e esquecer o Oeste da
`1,0` (que continua 15), a grade fica **incoerente**: uma célula diz que dá para passar, a outra
diz que não. Na figura, as células aparecem afastadas só para mostrar a anotação de cada uma; na
grade, as duas linhas dentro do tracejado colorido são **uma parede só**:

![À esquerda, 13 e 7 concordam que a parede do meio está aberta; à direita, 13 e 15 discordam](/img/maze/coerencia.svg)

O `maze_analyzer.py`, o programa que vem com o enunciado para conferir o arquivo de saída, acusa
um labirinto assim. Por isso abrir e fechar mexem **sempre nas duas células ao mesmo tempo**.

## As regras que os dois métodos garantem

| Regra | Como `open_wall` e `close_wall` a garantem |
|---|---|
| **coerência**: o Leste de `x,y` é igual ao Oeste de `x+1,y` | mudam as duas células de uma vez |
| **borda fechada** | recusam uma parede sem vizinha do outro lado |
| **"42" fechado** | recusam uma parede de célula do "42", ou voltada para uma |
| cada célula vale de `0` a `15` | só ligam ou desligam um bit |

## `open_wall`

```python
    def open_wall(self, cell: Cell, side: Direction) -> None:
        other = self._other_side(cell, side)
        self._walls[cell.y][cell.x] &= ~side
        self._walls[other.y][other.x] &= ~side.opposite
```

1. `_other_side` encontra a célula do outro lado da parede, ou levanta (lança) um erro se aquela
   parede não pode mudar (explicado abaixo).
2. Desliga o bit `side` na célula.
3. Desliga o bit do lado **oposto** (`side.opposite`) na vizinha: o Oeste, se `side` é o Leste.

`x &= y` é a forma curta de `x = x & y`. E `~side` liga todos os bits **menos** o de `side`
([parte 4](../04-value-objects/02-direction-bits.md) mostra a conta bit a bit). Juntos, `&= ~side`
apagam só aquele bit e mantêm os outros como estavam. O resultado é um `int` comum.

Abrir o Leste de `0,0` muda as duas células: a `0,0` desliga o bit do Leste (2) e passa de 15
para 13; a `1,0` desliga o bit do Oeste (8) e passa de 15 para 7. As duas células da parede
aparecem em amarelo, e a parede aberta vira uma linha fina tracejada:

![A grade 3 por 2 depois de abrir a parede entre 0,0 e 1,0](/img/maze/abrir-depois.svg)

Os números batem com uma subtração (15 − 2 = 13) só porque o bit estava ligado. O `& ~` não
subtrai, ele **desliga** o bit: com o bit já desligado, não muda nada. Subtrair erraria: abrir de
novo o Leste da `0,0`, que vale 13, daria 13 − 2 = 11 (`1011`), com o Leste fechado e o Sul
aberto.

## `close_wall`

```python
    def close_wall(self, cell: Cell, side: Direction) -> None:
        other = self._other_side(cell, side)
        self._walls[cell.y][cell.x] |= side
        self._walls[other.y][other.x] |= side.opposite
```

O espelho de `open_wall`: liga os dois bits com `|=` (a forma curta de `x = x | side`). Só o
`Braider` ([parte 8](../08-braider/04-a-regra-do-3x3.md)) o usa, para desfazer uma abertura que
deixou um bloco 3x3 sem nenhuma parede por dentro, o que o enunciado proíbe.

## `_other_side`: a guarda

```python
    def _other_side(self, cell: Cell, side: Direction) -> Cell:
        other = self.neighbour(cell, side)
        if other is None or cell in self.pattern:
            raise MazeError('internal: cannot change a border or "42" wall')
        return other
```

As duas operações começam pela mesma verificação, então ela mora num método auxiliar. O `_` no
começo do nome diz que ele é interno: só o próprio `Maze` o chama.

A parede só pode mudar quando:

- existe vizinha do outro lado: `neighbour` ([página anterior](./03-vizinhos.md)) não devolveu
  `None`, então o outro lado não é a borda nem uma célula do "42";
- a própria célula não é do "42". O `neighbour` só olha a célula de **destino**, por isso esta
  segunda condição.

O erro vem **antes** de qualquer escrita: se a parede não pode mudar, a grade fica intacta.

### Por que levantar erro, e não ignorar

Um algoritmo correto nunca pede para abrir a borda: ele só abre paredes que `neighbour` aprovou.
Se o pedido chega, há um defeito no algoritmo. Ignorar o pedido em silêncio esconderia o defeito
e produziria um labirinto diferente do esperado. Levantar `MazeError` faz o defeito aparecer na
hora, no ponto exato. A mensagem começa com `internal:`, a convenção do projeto para "defeito do
programa, não erro de quem usa".

## Experimente

Com os três métodos e o import no `maze.py`, na raiz do projeto:

```bash
.venv/bin/python - <<'EOF'
from mazegen.entities.maze import Maze
from mazegen.errors import MazeError
from mazegen.value_objects.cell import Cell
from mazegen.value_objects.direction import Direction
from mazegen.value_objects.pattern42 import Pattern42

maze = Maze(3, 2, Pattern42.for_size(3, 2))
maze.open_wall(Cell(0, 0), Direction.EAST)
print(maze.walls(Cell(0, 0)), maze.walls(Cell(1, 0)),
      maze.is_open(Cell(0, 0), Direction.EAST))
maze.close_wall(Cell(1, 0), Direction.WEST)
print(maze.walls(Cell(0, 0)), maze.walls(Cell(1, 0)),
      maze.is_open(Cell(0, 0), Direction.EAST))
try:
    maze.open_wall(Cell(0, 0), Direction.NORTH)
except MazeError as error:
    print(error)
print(maze.walls(Cell(0, 0)))
EOF
```

```text
13 7 True
15 15 False
internal: cannot change a border or "42" wall
15
```

- Depois de abrir, a `0,0` vale `13` e a `1,0` vale `7`: as duas células da parede mudaram, e o
  Leste de `0,0` virou passagem.
- Fechar o Oeste de `1,0` desfaz a abertura feita a partir de `0,0`: é a mesma parede, vista do
  outro lado.
- O Norte de `0,0` é a borda: o pedido é recusado com o erro, e a célula continua valendo `15`.
