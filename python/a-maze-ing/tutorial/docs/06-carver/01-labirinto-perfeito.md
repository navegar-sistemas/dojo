---
sidebar_position: 1
title: O labirinto perfeito é uma árvore
---

# O labirinto perfeito é uma árvore

O `Carver` recebe um `Maze` recém-criado, com todas as paredes fechadas, e abre paredes até
formar um **labirinto perfeito**. Ele é o primeiro passo de toda geração, nos dois modos: o
tabuleiro Pac-Man também nasce de um labirinto perfeito, que depois é trançado (parte 8).

## O labirinto visto como grafo

Troque cada célula por um ponto e cada passagem (parede aberta) por uma linha entre dois pontos.
O labirinto vira um **grafo**: pontos ligados por linhas.

![Labirinto perfeito 6 por 4 com um ponto em cada célula e uma linha laranja em cada passagem](/img/carver/arvore-6x4.svg)

As linhas laranja formam uma **árvore**: dá para ir de qualquer ponto a qualquer outro, e não
existe nenhum ciclo (nenhum caminho que sai de um ponto e volta a ele sem repetir linha). Uma
árvore que passa por **todos** os pontos se chama **árvore geradora**.

| Propriedade da árvore | O que significa no labirinto |
|---|---|
| liga todos os pontos | toda célula é alcançável a partir da entrada |
| não tem ciclo | existe um único caminho entre duas células quaisquer |
| `C` pontos, `C − 1` linhas | `C` células, `C − 1` passagens |

Escavar um labirinto perfeito é, portanto, construir uma árvore geradora das células.

## Por que `C − 1` passagens

Comece com uma célula só. Cada passagem aberta pelo `Carver` liga a parte já escavada a uma
célula **nova**. Para alcançar as outras `C − 1` células são precisas `C − 1` passagens, nem uma
a mais: uma passagem a mais ligaria duas células que já estão ligadas, e isso fecha um ciclo.

O `Maze` da parte 5 mede isso em `loop_count()`, que calcula
`passagens − células + 1`. Numa árvore, o resultado é sempre 0.

## O "42" fica fora da árvore

As 18 células do "42" não fazem parte do grafo: elas mantêm as quatro paredes fechadas. A árvore
cobre só as **células livres**.

O `Carver` não precisa saber disso. Ele pergunta ao `Maze` quais são as vizinhas de uma célula
com `maze.neighbour(cell, side)`, que devolve `None` para fora da grade e para as células do
"42". Uma célula que nunca aparece como vizinha nunca é escavada. A borda também fica fechada
pelo mesmo motivo.

O "42" é centrado com pelo menos uma célula de corredor até cada borda, então as células livres
continuam todas ligadas entre si: nenhuma fica isolada atrás do desenho.

## Consequências que vêm de graça

- **Entrada e saída com um único caminho**: é o que o subject exige com `PERFECT=True`.
- **Becos sem saída**: todo ramo que sai do caminho principal termina num beco. Essas pontas
  são as folhas da árvore.
- **Nenhum bloco 3x3 aberto**: um 3x3 aberto tem 9 células e 12 passagens internas, mais que
  as `9 − 1 = 8` que uma árvore permite. Logo, contém ciclos, e uma árvore nunca tem um. O modo
  perfeito cumpre a regra do 3x3 sem checagem nenhuma.

Falta escolher **como** construir a árvore. A próxima página mostra o algoritmo.
