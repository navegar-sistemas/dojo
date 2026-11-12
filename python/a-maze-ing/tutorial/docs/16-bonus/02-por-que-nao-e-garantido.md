---
sidebar_position: 2
title: Por que não é garantido
---

# Por que não é garantido

O passo (a) do braiding tenta abrir uma parede em cada beco, mas toda abertura passa pela regra
do 3x3: se a parede aberta completar um bloco 3x3 totalmente aberto, ela é fechada de novo.

```python
            sides = maze.closed_sides(cell)
            rng.shuffle(sides)
            for side in sides:
                if self._open_without_3x3(maze, cell, side):
                    break
```

O laço tenta os lados fechados do beco em ordem aleatória e para no primeiro que fica aberto.
Se **todos** completariam um 3x3, nenhum fica, e o beco continua beco. As duas regras do subject
se chocam: "nenhum 3x3 aberto" é obrigatório, "nenhum beco" é bônus, e a obrigatória vence.

## Um beco que não pode ser aberto

Montado com a entidade `Maze` real: uma grade 5x3 com todas as paredes internas abertas, menos
o Leste e o Oeste da célula `(2, 2)`. Nenhuma janela 3x3 está aberta, porque cada uma das três
janelas possíveis contém uma dessas duas paredes. A célula `(2, 2)` tem uma única passagem, para
o Norte: é um beco real, com dois lados fechados voltados para células livres.

![Grade 5 por 3 onde a célula (2, 2) é um beco com passagem só para o Norte](/img/bonus/beco-preso.svg)

Abrir o Oeste completa a janela das colunas 0 a 2:

![Abrir o Oeste da célula (2, 2) deixa o 3x3 das colunas 0 a 2 todo aberto](/img/bonus/beco-preso-oeste.svg)

Abrir o Leste completa a janela das colunas 2 a 4:

![Abrir o Leste da célula (2, 2) deixa o 3x3 das colunas 2 a 4 todo aberto](/img/bonus/beco-preso-leste.svg)

O Sul é borda. O braiding tenta os dois lados, desfaz os dois, e o beco fica.

Essa situação exige muitas paredes abertas em volta do beco, e paredes assim só aparecem
depois de várias aberturas do próprio braiding. Ela é rara, mas possível, e por isso o código
não pode **prometer** zero becos.

## A garantia que o gerador dá

O `MazeGenerator` confere o resultado do braiding com a regra **obrigatória**, não com a do
bônus:

```python
            Braider().braid(maze, self._rng)
            if (len(maze.dead_ends()) <= MAX_DEAD_ENDS
                    and maze.loop_count() >= MIN_LOOPS):
                break
```

Até 2 becos reais e pelo menos 2 ciclos: o tabuleiro é aceito. Fora disso, ele descarta a grade
e tenta de novo, até 20 vezes, com o mesmo gerador aleatório (parte 9). Exigir 0 becos aqui
transformaria um bônus em causa de erro: um config válido poderia terminar em `MazeError` por
causa de um beco que o subject tolera.

## O que acontece na prática

A garantia é "no máximo 2"; o resultado observado é 0. Gerando com `PERFECT=False`, entrada
`(0, 0)` e seeds 1 a 100:

| Tamanho | Becos reais | Becos cercados pelo "42" |
|---|---|---|
| 9x7 | 0 em todas | 2 |
| 20x15 | 0 em todas | 2 |
| 40x30 | 0 em todas | 2 |

O motivo é o backtracker (parte 6): os corredores longos dele deixam becos espalhados, cada um
cercado por paredes da árvore. Ao redor de um beco quase nunca existem as 11 paredes abertas que
transformariam a última abertura num 3x3, então o primeiro lado tentado já fica aberto.

O bônus, portanto, é um resultado medido, não uma propriedade do código. A forma de prová-lo
para um labirinto concreto é passar o arquivo de saída pelo analisador do subject.
