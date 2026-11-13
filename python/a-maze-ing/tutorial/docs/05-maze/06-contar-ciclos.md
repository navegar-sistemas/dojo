---
sidebar_position: 7
title: Contar ciclos
---

# Contar ciclos

No modo Pac-Man, o enunciado exige pelo menos **duas rotas independentes**, para o jogador
perseguido sempre ter outro caminho para fugir. Depois de abrir paredes extras, o gerador precisa
conferir se isso aconteceu. Esta página escreve o método que conta essas rotas, `loop_count`.
Ele entra na classe `Maze`, depois dos métodos da [página anterior](./05-passagens-e-becos.md),
sem import novo.

## Relembrando: ciclo

Um **ciclo** é um caminho que dá a volta e termina na célula onde começou, sem passar duas vezes
pelo mesmo trecho ([parte 1](../01-o-problema/05-perfeito-e-pac-man.md)). Ele existe quando há
duas rotas diferentes entre duas células: dá para ir por uma e voltar pela outra.

Um exemplo deixa claro o que são rotas **independentes**. Na grade 3x2 com todas as paredes
internas abertas há dois quadrados de 2x2 células, marcados em laranja e azul. Cada quadrado é
um ciclo:

![A grade 3 por 2 com todas as paredes internas abertas: 2 ciclos](/img/maze/ciclos-dois.svg)

Dar a volta na grade inteira também é um ciclo, mas não é uma rota nova: é só juntar os dois
quadrados e deixar de fora o trecho do meio, que eles dividem. Quem foge por ela não ganha
nenhuma alternativa que os dois quadrados já não dessem. Por isso essa grade tem **duas** rotas
independentes: o número de ciclos que não dá para montar juntando os outros.

## A conta

Pense no labirinto como um **grafo**: um desenho de pontos ligados por traços. Cada célula é um
ponto, e cada passagem entre duas células é um traço.

- Um labirinto **perfeito** (sem nenhum ciclo) é o que se chama de **árvore** em teoria dos
  grafos: ele liga `n` células com exatamente `n - 1` passagens. É o mínimo para ligar tudo: com
  uma a menos, alguma célula ficaria isolada.
- Cada passagem **a mais**, aberta entre duas células que já estavam ligadas, cria uma rota nova:
  um ciclo independente.

Então, num labirinto em que toda célula é alcançável:

```text
ciclos = passagens - células + 1
```

Na serpentina 3x2, há 6 células e 5 passagens: `5 - 6 + 1 = 0`. Nenhum ciclo, como se espera de
um corredor único.

![A serpentina 3 por 2: 5 passagens e nenhum ciclo](/img/maze/ciclos-serpentina.svg)

Abrindo as duas paredes Sul que faltam, são 7 passagens: `7 - 6 + 1 = 2`. É a grade do exemplo
acima: os dois ciclos são os dois quadrados 2x2 (as células `0,0`, `1,0`, `0,1`, `1,1`, em
laranja, e as células `1,0`, `2,0`, `1,1`, `2,1`, em azul).

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

Uma única volta pelas células soma duas coisas:

- `ends`: as **pontas** de passagem. Uma passagem liga duas células, então aparece duas vezes: na
  lista `passages` de cada uma. Somando o tamanho dessas listas, cada passagem é contada duas
  vezes, e o número de passagens é `ends // 2` (`//` é a divisão inteira).
- `count`: o número de células do labirinto. O `cells()` já pula o "42", que não faz parte do
  grafo.

### A condição: tudo conectado

A fórmula só vale quando todas as células são alcançáveis, porque o "`n - 1` passagens" é o que
liga **um** pedaço só. Num labirinto partido em dois pedaços separados, cada pedaço tem uma
passagem a menos que as suas células, e a conta erra. Numa grade 4x1 com a parede entre `0,0` e
`1,0` aberta e a parede entre `2,0` e `3,0` aberta, há dois corredores de duas células, sem ciclo
nenhum, mas a conta dá `2 - 4 + 1 = -1`.

O gerador nunca chega a esse caso. O `Carver` (o algoritmo que cava,
[parte 6](../06-carver/02-recursive-backtracker.md)) visita toda célula fora do "42", e o
braiding (a transformação em tabuleiro Pac-Man, [parte 8](../08-braider/03-criar-ciclos.md)) só
abre paredes a mais, nunca fecha uma passagem que o `Carver` cavou.

Pelo mesmo motivo, numa grade recém-criada, sem passagem nenhuma, a conta não mede ciclo nenhum:
dá `0 - células + 1`, um número negativo. O método só é chamado depois de cavar.

## Experimente

Com o `loop_count` no `maze.py`, na raiz do projeto:

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
print(maze.loop_count())
maze.open_wall(Cell(0, 0), Direction.SOUTH)
maze.open_wall(Cell(1, 0), Direction.SOUTH)
print(maze.loop_count(), maze.dead_ends())
split = Maze(4, 1, Pattern42.for_size(4, 1))
split.open_wall(Cell(0, 0), Direction.EAST)
split.open_wall(Cell(2, 0), Direction.EAST)
print(split.loop_count())
EOF
```

```text
0
2 []
-1
```

- A serpentina não tem ciclo.
- Com as duas paredes Sul abertas, são 2 ciclos, e os becos da serpentina também somem: toda
  célula passa a ter duas passagens ou mais.
- Os dois corredores separados da grade 4x1 dão `-1`: a conta só faz sentido com tudo conectado.
