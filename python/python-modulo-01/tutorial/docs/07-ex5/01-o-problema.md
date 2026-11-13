---
sidebar_position: 1
title: O problema
---

# O problema

O jardim tem tipos diferentes de planta: flores, árvores, hortaliças. Todas têm nome, altura e
idade, crescem e envelhecem; cada tipo tem também coisas só suas. Uma flor tem cor e floresce;
uma árvore tem um tronco e faz sombra; uma hortaliça tem época de colheita e valor nutricional.

Copiar a classe `Plant` três vezes e acrescentar o que falta a cada cópia funcionaria, mas
triplicaria o código comum: uma correção na validação da altura teria de ser feita em três
lugares. O que o exercício pede é escrever o comum uma vez e **herdá-lo**.

## O que o enunciado pede

Um arquivo `ex5/ft_plant_types.py`, que só pode chamar `super()`, `print()`, `range()` e
`round()`, com:

- a classe `Plant` do exercício 4, com o que é comum a todas as plantas (nome, altura, idade);
- três tipos especializados que **herdam** de `Plant`:
  - **`Flower`** (flor): um atributo `color` (cor) e a ação de florescer, `bloom()`;
  - **`Tree`** (árvore): um atributo `trunk_diameter` (diâmetro do tronco) e a ação de fazer
    sombra, `produce_shade()`;
  - **`Vegetable`** (hortaliça): os atributos `harvest_season` (época de colheita) e
    `nutritional_value` (valor nutricional);
- os tipos especializados chamam os métodos de `Plant` por meio de `super()`, inclusive o
  construtor;
- `show()` de um tipo especializado imprime a linha de `Plant` e, embaixo, os dados extras do
  tipo, reaproveitando o `show()` de `Plant`;
- pelo menos uma planta de cada tipo; a flor floresce; o valor nutricional da hortaliça começa
  em 0 e aumenta quando ela cresce e envelhece;
- nada de código comum duplicado entre os três tipos.

Os atributos novos não precisam de validação.

## A saída esperada

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

=== Tree
Oak: 200.0cm, 365 days old
 Trunk diameter: 5.0cm
[asking the oak to produce shade]
Tree Oak now produces a shade of 200.0cm long and 5.0cm wide.

=== Vegetable
Tomato: 5.0cm, 10 days old
 Harvest season: April
 Nutritional value: 0
[make tomato grow and age for 20 days]
Tomato: 47.0cm, 30 days old
 Harvest season: April
 Nutritional value: 20
```

Três blocos, um por tipo. As linhas entre colchetes narram o que o programa faz em seguida; as
linhas que começam com um espaço são os dados extras do tipo. O tomate, em 20 dias, cresce de 5
para 47 cm (2,1 cm por dia) e o valor nutricional vai de 0 a 20.
