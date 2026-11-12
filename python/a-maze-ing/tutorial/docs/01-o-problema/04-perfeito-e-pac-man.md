---
sidebar_position: 4
title: Labirinto perfeito e tabuleiro Pac-Man
---

# Labirinto perfeito e tabuleiro Pac-Man

A chave `PERFECT` escolhe entre dois tipos de labirinto.

## Perfeito (`PERFECT=True`)

Existe **exatamente um caminho** entre quaisquer duas células. Não há ciclos: andando por um
corredor, nunca se volta a um lugar por outro lado.

Um labirinto perfeito 6x4 gerado pelo programa (`seed=7`), com a entrada em magenta e a saída em
vermelho:

![Labirinto perfeito 6 por 4](/img/problema/perfeito-6x4.svg)

A célula de cima à esquerda e a de baixo à esquerda são becos: cada uma tem uma só saída.

Consequências:

- todo corredor que sai do caminho principal termina num **beco sem saída**;
- com `C` células, o labirinto tem exatamente `C − 1` passagens. Em teoria de grafos, isso é uma
  **árvore geradora**: todas as células ligadas, sem nenhum ciclo.

## Pac-Man (`PERFECT=False`, o padrão)

Um tabuleiro onde dá para fugir dos fantasmas: há **ciclos** (rotas alternativas) e quase não há
becos.

| Regra | Valor |
|---|---|
| rotas independentes (ciclos) | pelo menos 2 |
| becos sem saída reais | no máximo 2 |
| cantos e centro | sempre corredores alcançáveis |
| áreas abertas | nenhum bloco 3x3 totalmente aberto |

A proibição do 3x3 aberto vem do subject: o labirinto não pode ter "salões" largos, só
corredores. Blocos 2x2, 2x3 e 3x2 abertos são permitidos.

O mesmo labirinto 6x4, agora no modo Pac-Man (`seed=7`):

![Tabuleiro Pac-Man 6 por 4](/img/problema/pacman-6x4.svg)

As duas paredes que fechavam os becos da esquerda foram abertas, e os corredores de cima e de
baixo viraram rotas alternativas.

## Como o Pac-Man é gerado

Não existe um algoritmo separado para ele. O gerador:

1. cria um labirinto **perfeito**;
2. abre uma parede em cada beco sem saída, ligando-o a uma vizinha;
3. abre mais paredes aleatórias até haver pelo menos 2 ciclos;
4. desfaz qualquer abertura que formaria um 3x3 aberto.

Esse processo se chama **braiding** ("trançar"), e é o assunto da parte 8.

## Tamanhos impossíveis

O Pac-Man precisa de 2 ciclos independentes. Uma grade `W x H` com todas as paredes internas
abertas tem `(W − 1) × (H − 1)` ciclos, então grades 1xN, Nx1 e 2x2 nunca chegam a 2. O config
recusa:

```text
Error: config.txt: PERFECT=False needs (WIDTH - 1) x (HEIGHT - 1) >= 2 for a Pac-Man board, got 1x10
```

## Sempre conectado

Nos dois modos, toda célula (exceto as do "42") é alcançável a partir da entrada. Não existe
região isolada.
