---
sidebar_position: 1
title: O tabuleiro sem becos
---

# O tabuleiro sem becos

O primeiro bônus sugerido pelo subject é um labirinto padrão (não perfeito) **sem nenhum beco
sem saída**: um tabuleiro "perfeitamente trançado" (*perfectly braided*), onde um jogador
perseguido nunca fica preso. O modo Pac-Man construído nas partes 8 e 9 já entrega isso. Não há
código novo nesta parte: ela explica por que o resultado sai assim e como provar.

Os bônus só contam com a parte obrigatória inteira aprovada.

## O que é um beco real

Um **beco** é uma célula com uma única passagem: quem entra só sai por onde veio. Num tabuleiro
de Pac-Man, é uma armadilha: o fantasma que vem atrás fecha a única saída.

Nem todo beco pode ser desfeito. Uma célula encostada no "42" pode ter todas as paredes
fechadas voltadas para células do "42" ou para a borda; abrir qualquer uma delas abriria uma
célula que precisa ficar fechada, ou o lado de fora da grade. Esses são os becos **cercados pelo
"42"**. O subject tolera os becos do "42", e o `maze_analyzer.py` os conta separado.

Um beco **real** tem pelo menos uma parede fechada voltada para uma célula livre: uma parede que
poderia ser aberta. É esse que o bônus proíbe.

## Perfeito e Pac-Man, lado a lado

O labirinto perfeito do `config.txt` padrão com `SEED=42`, com os becos reais em laranja e os
cercados pelo "42" em azul:

![Labirinto perfeito 20 por 15 com 32 becos reais em laranja e 2 cercados pelo 42 em azul](/img/bonus/perfeito-20x15.svg)

Um labirinto perfeito é uma árvore: todo galho que sai do caminho principal termina num beco.
São 32 becos reais.

O mesmo config com `PERFECT=False`, o padrão:

![Tabuleiro Pac-Man 20 por 15 sem becos reais e com 2 cercados pelo 42](/img/bonus/pacman-20x15.svg)

Nenhum laranja. Os dois becos azuis continuam: são as células dentro das "barrigas" do 4 e do 2,
cercadas por células do "42" e com uma única passagem para fora. Não há parede que possa ser
aberta nelas.

## Por que o Pac-Man sai assim

O braiding (parte 8) tem dois passos: (a) abrir uma parede em cada beco; (b) abrir paredes extras
até haver 2 ciclos. O passo (a) é o que remove os becos:

- `maze.dead_ends()` lista só os becos reais: os cercados pelo "42" têm `closed_sides` vazio e
  não entram na lista.
- Cada beco da lista tem uma parede fechada aberta para uma vizinha livre, em ordem aleatória.
- Abrir uma parede só **aumenta** o número de passagens das duas células. Nenhuma abertura cria
  um beco novo, então uma única passada pela lista basta.

A regra do subject para o modo Pac-Man tolera até 2 becos reais. O braiding vai além do mínimo
porque abrir **todos** é tão simples quanto abrir alguns: o mesmo laço, sem critério de parada.

## Não há chave para ligar

O bônus é o comportamento do modo padrão. Não existe opção no config para ligá-lo ou desligá-lo:
`PERFECT=False` gera o tabuleiro sem becos, `PERFECT=True` gera o labirinto perfeito, com todos
os seus becos. O README descreve o bônus na seção **Bonus** (parte 15).
