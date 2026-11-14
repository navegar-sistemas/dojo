---
sidebar_position: 1
title: O problema
---

# O problema

O último exercício junta tudo e acrescenta as peças que faltam para analisar o jardim: perguntas
que não dependem de uma planta específica, um jeito especial de criar plantas, um tipo de planta
herdando de outro tipo, e estatísticas de uso de cada planta.

## O que o enunciado pede

Um arquivo `ex6/ft_garden_analytics.py`, que só pode chamar `super()`, `print()`, `range()`,
`round()`, `staticmethod()` e `classmethod()`, com as classes do exercício 5 melhoradas:

- um **método estático** em `Plant` que responde se uma idade, recebida como parâmetro, passa de
  um ano;
- um **método de classe** que cria uma planta "anônima" na hora, quando ainda não se sabem os
  dados dela;
- uma classe **`Seed`** (semente) que herda de `Flower` e guarda o número de sementes que a flor
  dá depois de florescer; o `show()` dela mostra as sementes;
- dentro de toda `Plant`, um sistema interno de **estatísticas**, escrito como uma **classe
  aninhada** (uma classe dentro de outra), que conta as chamadas a `grow()`, a `age()` e a
  `show()`. Esse sistema precisa de encapsulamento e de um método que exibe os números;
- nas árvores, uma estatística a mais: as chamadas a `produce_shade()`;
- uma **única função**, fora de qualquer classe, que exibe as estatísticas de qualquer tipo de
  planta.

O enunciado aceita, para os métodos estático e de classe, a sintaxe de **decorador**, explicada
em [O método estático](./02-o-metodo-estatico.md). Ele avisa também que este exercício reúne todos
os conceitos do projeto: o ponto principal é entender como as peças interagem e se organizam.

## A saída esperada

```text
=== Garden statistics ===
=== Check year-old
Is 30 days more than a year? -> False
Is 400 days more than a year? -> True

=== Flower
Rose: 15.0cm, 10 days old
 Color: red
 Rose has not bloomed yet
[statistics for Rose]
Stats: 0 grow, 0 age, 1 show
[asking the rose to grow and bloom]
Rose: 23.0cm, 10 days old
 Color: red
 Rose is blooming beautifully!
[statistics for Rose]
Stats: 1 grow, 0 age, 2 show

=== Tree
Oak: 200.0cm, 365 days old
 Trunk diameter: 5.0cm
[statistics for Oak]
Stats: 0 grow, 0 age, 1 show
 0 shade
[asking the oak to produce shade]
Tree Oak now produces a shade of 200.0cm long and 5.0cm wide.
[statistics for Oak]
Stats: 0 grow, 0 age, 1 show
 1 shade

=== Seed
Sunflower: 80.0cm, 45 days old
 Color: yellow
 Sunflower has not bloomed yet
 Seeds: 0
[make sunflower grow, age and bloom]
Sunflower: 110.0cm, 65 days old
 Color: yellow
 Sunflower is blooming beautifully!
 Seeds: 42
[statistics for Sunflower]
Stats: 1 grow, 1 age, 2 show

=== Anonymous
Unknown plant: 0.0cm, 0 days old
[statistics for Unknown plant]
Stats: 0 grow, 0 age, 1 show
```

O que a saída diz sobre o funcionamento:

- a rosa cresce de 15 para 23 cm com **uma** chamada a `grow()` (`1 grow`): 8 cm de uma vez, a
  taxa de crescimento dela;
- o girassol cresce de 80 para 110 cm com **uma** chamada a `grow()`: a taxa dele é de 30 cm;
- o girassol envelhece de 45 para 65 dias com **uma** chamada a `age()` (`1 age`): 20 dias de uma
  vez. O `age()` do exercício 5 soma sempre um dia, e por isso passa a receber quantos dias
  envelhecer ([A classe aninhada](./04-a-classe-aninhada.md#contar-as-chamadas));
- as estatísticas da árvore têm a linha a mais, `0 shade` e depois `1 shade`;
- o girassol tem `0` sementes antes de florescer e `42` depois;
- a planta anônima se chama `Unknown plant` e tem 0 cm e 0 dias.
