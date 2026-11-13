---
slug: /
sidebar_position: 1
title: O que vamos construir
---

# O que vamos construir

Um programa que guarda os dados de uma planta em três variáveis soltas funciona bem para uma
planta. Com trinta plantas, são noventa variáveis; com plantas que crescem, envelhecem, florescem
e precisam de regras ("altura não pode ser negativa"), o código vira uma pilha de variáveis e
funções sem dono. A **programação orientada a objetos** resolve isso juntando, num mesmo lugar,
os dados de uma coisa e as ações que essa coisa sabe fazer.

O projeto se chama **Code Cultivation** ("cultivo de código"). O tema é um jardim comunitário:
plantas com nome, altura e idade, que crescem, envelhecem, florescem e dão sombra. O tema só dá
nome às coisas; o assunto de verdade é a orientação a objetos em Python.

## Sete programas pequenos

O projeto tem sete **exercícios**. Cada um é um programa de um arquivo só, numa pasta própria, e
cada um acrescenta uma ferramenta nova ao anterior:

| Exercício | Arquivo | O que ensina |
|---|---|---|
| 0 | `ex0/ft_garden_intro.py` | a **estrutura** de um programa Python: onde a execução começa |
| 1 | `ex1/ft_garden_data.py` | a primeira **classe**, `Plant`: um molde para todas as plantas |
| 2 | `ex2/ft_plant_growth.py` | **métodos** que mudam a planta: crescer e envelhecer |
| 3 | `ex3/ft_plant_factory.py` | o **construtor**: criar a planta já com os seus dados |
| 4 | `ex4/ft_garden_security.py` | **encapsulamento**: proteger os dados contra valores inválidos |
| 5 | `ex5/ft_plant_types.py` | **herança**: flores, árvores e hortaliças como tipos especiais de planta |
| 6 | `ex6/ft_garden_analytics.py` | métodos **estáticos** e **de classe**, classes **aninhadas** e estatísticas |

Os programas não leem nada do teclado: cada um cria algumas plantas, faz alguma coisa com elas e
imprime o resultado. Um exemplo, o exercício 5 rodando (o começo da saída):

```text
=== Garden Plant Types ===
=== Flower
Rose: 15.0cm, 10 days old
 Color: red
 Rose has not bloomed yet
[asking the rose to bloom]
Rose: 15.0cm, 10 days old
 Color: red
 Rose is blooming beautifully!
```

A rosa é uma planta como as outras (nome, altura, idade), mas também tem cor e sabe florescer. As
mensagens são em inglês porque o enunciado do projeto mostra a saída de cada programa, e essa
saída é em inglês.

## O enunciado

O projeto vem com um documento oficial, o **enunciado** (em inglês, *subject*), que fixa os
arquivos, as regras e a saída de cada programa
([em linguagem simples](./02-o-enunciado-em-linguagem-simples.md)).
