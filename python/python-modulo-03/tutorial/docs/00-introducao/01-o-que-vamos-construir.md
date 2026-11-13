---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

Quase todo programa guarda **vários** valores de uma vez: as pontuações de uma partida, os itens
de uma mochila, os jogadores conectados. Uma variável comum guarda um valor só. Para guardar
muitos, o Python tem as **coleções**: objetos que agrupam outros valores. São quatro: lista,
tupla, set e dicionário. Ao lado delas, os *generators* e as *comprehensions* produzem valores em
série.

O projeto se chama **Data Quest** ("missão dos dados"). O tema é uma plataforma que analisa dados
de jogos: pontuações, posições no mapa, conquistas, inventário. O tema só dá nome às coisas; o
assunto de verdade é escolher e usar a coleção certa para cada tarefa.

## Sete programas pequenos

O projeto tem sete **exercícios**. Cada um é um programa de um arquivo só, numa pasta própria, e
cada um apresenta uma coleção ou recurso novo:

| Exercício | Arquivo | O que ensina |
|---|---|---|
| 0 | `ex0/ft_command_quest.py` | **listas**, lendo a lista de argumentos que o programa recebe ao ser rodado |
| 1 | `ex1/ft_score_analytics.py` | criar uma lista nova e tirar estatísticas dela (total, média, maior, menor) |
| 2 | `ex2/ft_coordinate_system.py` | **tuplas**, para guardar uma posição `(x, y, z)` que não muda |
| 3 | `ex3/ft_achievement_tracker.py` | **sets**, para comparar as conquistas de vários jogadores |
| 4 | `ex4/ft_inventory_system.py` | **dicionários**, para guardar a quantidade de cada item de um inventário |
| 5 | `ex5/ft_data_stream.py` | **generators**, que produzem um valor por vez, sob demanda |
| 6 | `ex6/ft_data_alchemist.py` | **comprehensions**, que constroem uma lista ou um dicionário numa linha |

Um exemplo, o exercício 4 rodando com uma lista de itens digitada no terminal:

```text
=== Inventory System Analysis ===
Got inventory: {'sword': 1, 'potion': 5}
Item list: ['sword', 'potion']
Total quantity of the 2 items: 6
Item sword represents 16.7%
Item potion represents 83.3%
Item most abundant: potion with quantity 5
Item least abundant: sword with quantity 1
Updated inventory: {'sword': 1, 'potion': 5, 'magic_item': 1}
```

As mensagens são em inglês porque o enunciado do projeto mostra a saída exata de cada programa, e
essa saída é em inglês.

## O enunciado

O projeto vem com um documento oficial que diz o que precisa ser entregue: o **enunciado** (em
inglês, *subject*). O resumo dele está em
[O enunciado em linguagem simples](./02-o-enunciado-em-linguagem-simples.md).

Os termos novos estão no [glossário](./05-glossario.md).
