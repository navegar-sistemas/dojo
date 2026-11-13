---
sidebar_position: 2
title: Por que não é garantido
---

# Por que não é garantido

O tabuleiro Pac-Man sai sem becos em todos os casos medidos, mas o código não **promete** isso.
O motivo é uma regra obrigatória do enunciado que às vezes impede abrir um beco: a de que nenhum
bloco de 3x3 células pode ficar totalmente aberto, sem nenhuma parede por dentro. Esta página
mostra quando as duas regras se chocam e por que a obrigatória vence.

## Toda abertura passa pela regra do 3x3

No passo (a) do *braiding*, o laço que abre os becos tenta as paredes fechadas de cada beco
([parte 8](../08-braider/02-abrir-os-becos.md)):

```python
            sides = maze.closed_sides(cell)
            rng.shuffle(sides)
            for side in sides:
                if self._open_without_3x3(maze, cell, side):
                    break
```

- `maze.closed_sides(cell)` é a lista das paredes fechadas do beco que dão para uma célula livre:
  as que poderiam ser abertas.
- `rng.shuffle(sides)` embaralha essa lista com o sorteador do gerador (`rng`), para a parede
  aberta não ser sempre a do mesmo lado.
- `_open_without_3x3` abre a parede e confere se algum bloco 3x3 ficou todo aberto. Se ficou,
  fecha a parede de novo e devolve `False`; senão, deixa aberta e devolve `True`
  ([parte 8](../08-braider/04-a-regra-do-3x3.md)).
- O `break` para no primeiro lado que fica aberto.

Se **todos** os lados completariam um 3x3, nenhum fica aberto, e o beco continua beco. As duas
regras do enunciado se chocam: "nenhuma área 3x3 aberta" é obrigatória, "nenhum beco" é bônus,
e a obrigatória vence.

## Um beco que não pode ser aberto

Este caso foi montado com a classe `Maze` real, a grade de paredes do gerador
([parte 5](../05-maze/01-a-grade-de-paredes.md)): uma grade de 5 colunas por 3 linhas com todas
as paredes de dentro abertas, menos duas, a Leste e a Oeste da célula `2,2`.

- Nenhum bloco 3x3 está todo aberto. Numa grade 5x3 cabem três blocos 3x3 (colunas 0 a 2, 1 a 3
  e 2 a 4), e cada um contém pelo menos uma das duas paredes fechadas.
- A célula `2,2` tem uma única passagem, para o Norte: é um beco **real**, com dois lados
  fechados voltados para células livres. O Sul dela é a borda.

![Grade 5 por 3 onde a célula 2,2 é um beco com passagem só para o Norte](/img/bonus/beco-preso.svg)

Nas três figuras desta seção, as linhas cheias são paredes fechadas e as tracejadas, paredes
abertas. O laranja marca o beco real, como na [parte 8](../08-braider/01-becos-sem-saida.md), e
o amarelo, nas duas seguintes, marca o bloco 3x3 que ficaria todo aberto, como na
[parte 5](../05-maze/07-areas-abertas-3x3.md).

Abrir o Oeste deixa sem nenhuma parede o bloco das colunas 0 a 2:

![Abrir o Oeste da célula 2,2 deixa o 3x3 das colunas 0 a 2 todo aberto](/img/bonus/beco-preso-oeste.svg)

Abrir o Leste deixa sem nenhuma parede o bloco das colunas 2 a 4:

![Abrir o Leste da célula 2,2 deixa o 3x3 das colunas 2 a 4 todo aberto](/img/bonus/beco-preso-leste.svg)

O *braiding* tenta os dois lados, desfaz os dois, e o beco fica.

Essa situação exige muitas paredes abertas em volta do beco, e paredes assim só aparecem depois
de várias aberturas do próprio *braiding*. Ela é rara, mas possível, e por isso o código não pode
prometer zero becos.

## A garantia que o gerador dá

Depois do *braiding*, o `MazeGenerator` confere o resultado com a regra **obrigatória**, não com
a do bônus ([parte 9](../09-gerador/03-generate.md)):

```python
            Braider().braid(maze, self._rng)
            if (len(maze.dead_ends()) <= MAX_DEAD_ENDS
                    and maze.loop_count() >= MIN_LOOPS):
                break
```

- `MAX_DEAD_ENDS` vale 2: o máximo de becos reais, a leitura do projeto para o "um ou dois são
  tolerados" do enunciado.
- `MIN_LOOPS` vale 2: o mínimo de ciclos, as "duas rotas independentes" do enunciado.
  `maze.loop_count()` conta os ciclos do labirinto ([parte 5](../05-maze/06-contar-ciclos.md)).

Com até 2 becos reais e pelo menos 2 ciclos, o tabuleiro é aceito e o `break` sai do laço de
tentativas. Fora disso, o gerador descarta a grade e começa de novo, até 20 vezes, sempre com o
mesmo sorteador.

Exigir 0 becos aqui transformaria um bônus em causa de erro: um arquivo de configuração válido
poderia terminar em `MazeError` por causa de um beco que o enunciado tolera.

## O que acontece na prática

A garantia é "no máximo 2"; o resultado observado é 0. Gerando com `PERFECT=False`, entrada
`0,0`, saída no canto de baixo à direita e as sementes de 1 a 100:

| Tamanho | Becos reais | Becos cercados pelo "42" |
|---|---|---|
| 9x7 | 0 em todas | 2 |
| 20x15 | 0 em todas | 2 |
| 40x30 | 0 em todas | 2 |

O motivo está no *recursive backtracker*, o algoritmo que cava o labirinto perfeito
([parte 6](../06-carver/02-recursive-backtracker.md)). Os corredores longos dele deixam os becos
espalhados, cada um cercado pelas paredes da árvore. Para a última abertura completar um 3x3,
as outras 11 paredes de dentro daquele bloco já teriam de estar abertas, e isso quase nunca
acontece em volta de um beco; o primeiro lado tentado já fica aberto.

O bônus, portanto, é um resultado medido, e não uma propriedade garantida pelo código. O jeito
de prová-lo para um labirinto concreto é passar o arquivo de saída pelo analisador do
enunciado, na [próxima página](./03-conferir-com-o-analyzer.md).
