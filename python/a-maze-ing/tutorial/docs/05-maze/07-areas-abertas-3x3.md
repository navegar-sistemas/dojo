---
sidebar_position: 8
title: Áreas abertas 3x3
---

# Áreas abertas 3x3

Um labirinto é feito de corredores, não de salões. O enunciado transforma isso numa regra
concreta: nenhum bloco de 3x3 células pode ficar totalmente aberto. O modo Pac-Man abre paredes
extras e corre o risco de criar um bloco assim, então precisa perguntar à grade, a cada parede
aberta, se isso aconteceu. Esta página escreve o método que responde, `has_open_3x3`, e o seu
auxiliar, `_window_open`. Os dois entram na classe `Maze`, depois do `loop_count` da
[página anterior](./06-contar-ciclos.md), sem import novo.

## A regra

Nenhum bloco de 3x3 células pode ter **todas** as paredes de dentro abertas. O enunciado diz que
os corredores não podem ter mais de 2 células de largura, e dá o exemplo: uma área aberta 2x3 ou
3x2 pode, uma 3x3 nunca. Blocos abertos de 2x2 também são permitidos.

Um bloco 3x3 tem 12 paredes internas (as que ficam entre duas células do próprio bloco):

- entre as 3 colunas há 2 fileiras verticais de paredes, com 3 paredes cada: 6;
- entre as 3 linhas há 2 fileiras horizontais de paredes, com 3 paredes cada: 6.

Na figura, o bloco está em amarelo, as paredes fechadas são linhas grossas, e as abertas, linhas
finas tracejadas:

![Um bloco 3 por 3 com as 12 paredes internas abertas](/img/maze/janela-3x3-aberta.svg)

Basta **uma** parede interna fechada para o bloco deixar de ser uma área aberta. Aqui, a parede
entre as duas células verdes:

![O mesmo bloco com a parede entre 1,1 e 2,1 fechada](/img/maze/janela-3x3-fechada.svg)

O modo perfeito nunca forma um 3x3 aberto: abrir as 12 paredes entre 9 células criaria ciclos, e
um labirinto perfeito não tem ciclo nenhum. No modo Pac-Man, o `Braider`
([parte 8](../08-braider/04-a-regra-do-3x3.md)) abre paredes extras e, depois de cada uma,
pergunta ao `Maze` se algum 3x3 ficou aberto. Se ficou, ele fecha a parede de volta.

## `has_open_3x3`: todas as janelas

```python
    def has_open_3x3(self) -> bool:
        for y0 in range(self.height - 2):
            for x0 in range(self.width - 2):
                if self._window_open(x0, y0):
                    return True
        return False
```

Uma **janela** é um bloco 3x3 da grade, identificado pela célula do canto de cima à esquerda,
`x0,y0`. O método testa todas as janelas possíveis e responde `True` na primeira que estiver
aberta.

O canto `x0` vai de 0 até `width - 3`, para a janela caber na grade (as colunas `x0`, `x0 + 1` e
`x0 + 2` precisam existir). `range(self.width - 2)` dá exatamente os números de 0 a
`width - 3`, porque o `range` para logo **antes** do valor final. O mesmo vale para `y0`.

Numa grade 5x4 há 3 posições para `x0` e 2 para `y0`, ou seja, 3 x 2 = 6 janelas. A figura
marca em amarelo a que começa em `1,0`:

![Uma das seis janelas 3 por 3 de uma grade 5 por 4](/img/maze/janelas-5x4.svg)

Numa grade com menos de 3 colunas ou 3 linhas, o `range` fica vazio, nenhuma janela é testada, e
a resposta é `False`.

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

Percorre as 9 células da janela e procura uma parede interna fechada. Cada parede interna é
conferida **uma vez só**, pela célula da esquerda ou pela de cima:

- as 6 paredes verticais são o **Leste** das células das duas primeiras colunas
  (`x < x0 + 2`);
- as 6 horizontais são o **Sul** das células das duas primeiras linhas (`y < y0 + 2`).

![Quem confere cada parede interna: E nas duas primeiras colunas, S nas duas primeiras linhas](/img/maze/janela-paredes-conferidas.svg)

Pela coerência (duas vizinhas sempre concordam sobre a parede que dividem), olhar o Leste de
`x,y` é o mesmo que olhar o Oeste de `x+1,y`, então não é preciso conferir os dois lados. A
coluna da direita e a linha de baixo não têm parede interna a conferir: o Leste e o Sul delas
dão para fora da janela.

Uma janela com célula do "42" nunca está aberta. Toda célula da janela divide pelo menos uma
parede interna com outra célula da janela, e a célula do "42" tem as quatro paredes fechadas:
essa parede interna está fechada. O laço a encontra lendo a própria célula do "42", quando ela
está nas duas primeiras colunas ou linhas, ou lendo a vizinha da esquerda ou de cima, que, pela
coerência, anota a mesma parede como fechada.

### Parar na primeira parede fechada

O `return False` sai na **primeira** parede fechada encontrada. Num labirinto, quase toda janela
tem uma parede fechada logo no começo, então a maioria custa uma ou duas leituras, em vez de 12.

Isso importa porque o `Braider` chama `has_open_3x3` depois de **cada** parede que abre, e cada
chamada percorre todas as janelas. Numa grade 100x100 são 98 x 98 = 9 604 janelas por chamada;
com a saída antecipada, uma chamada leva poucos milissegundos.

### Por que olhar a grade inteira

Uma parede aberta só pode criar um 3x3 aberto nas janelas que a contêm, e bastaria olhar essas.
Seria mais rápido, mas exige calcular quais janelas tocam a parede, inclusive perto das bordas.
É uma escolha do projeto percorrer todas: o código fica mais simples de ler e de conferir, e com
a saída antecipada já é rápido o bastante.

## Experimente

Com os dois métodos no `maze.py`, na raiz do projeto:

```bash
.venv/bin/python - <<'EOF'
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
print([maze.walls(cell) for cell in maze.cells()])
print(maze.has_open_3x3(), maze.loop_count())
maze.close_wall(Cell(1, 1), Direction.EAST)
print(maze.has_open_3x3())
EOF
```

```text
[9, 1, 3, 8, 0, 2, 12, 4, 6]
True 4
False
```

- O laço abre as 12 paredes internas de uma grade 3x3, com a mesma regra de "Leste das duas
  primeiras colunas, Sul das duas primeiras linhas".
- Na primeira linha impressa, as células vêm na ordem de `cells()`, linha por linha. A do meio,
  `1,1`, vale `0`: as quatro paredes abertas. Os cantos guardam só as duas paredes da borda
  (`9` = Norte + Oeste no canto de cima à esquerda).
- `loop_count` dá 4: os quatro quadrados 2x2 dentro do bloco.
- Fechar uma única parede, o Leste de `1,1`, já basta para o bloco deixar de ser aberto.
