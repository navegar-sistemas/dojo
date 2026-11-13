---
sidebar_position: 4
title: O resultado final
---

# O resultado final

A saída de cada programa pronto, igual, letra por letra, à que o enunciado mostra.

## Exercício 0

```bash
python3 ex0/ft_garden_intro.py
```

```text
=== Welcome to My Garden ===
Plant: Rose
Height: 25cm
Age: 30 days

=== End of Program ===
```

## Exercício 1

```bash
python3 ex1/ft_garden_data.py
```

```text
=== Garden Plant Registry ===
Rose: 25cm, 30 days old
Sunflower: 80cm, 45 days old
Cactus: 15cm, 120 days old
```

## Exercício 2

```bash
python3 ex2/ft_plant_growth.py
```

```text
=== Garden Plant Growth ===
Rose: 25.0cm, 30 days old
=== Day 1 ===
Rose: 25.8cm, 31 days old
=== Day 2 ===
Rose: 26.6cm, 32 days old
=== Day 3 ===
Rose: 27.4cm, 33 days old
=== Day 4 ===
Rose: 28.2cm, 34 days old
=== Day 5 ===
Rose: 29.0cm, 35 days old
=== Day 6 ===
Rose: 29.8cm, 36 days old
=== Day 7 ===
Rose: 30.6cm, 37 days old
Growth this week: 5.6cm
```

## Exercício 3

```bash
python3 ex3/ft_plant_factory.py
```

```text
=== Plant Factory Output ===
Created: Rose: 25.0cm, 30 days old
Created: Oak: 200.0cm, 365 days old
Created: Cactus: 5.0cm, 90 days old
Created: Sunflower: 80.0cm, 45 days old
Created: Fern: 15.0cm, 120 days old
```

## Exercício 4

```bash
python3 ex4/ft_garden_security.py
```

```text
=== Garden Security System ===
Plant created: Rose: 15.0cm, 10 days old

Height updated: 25cm
Age updated: 30 days

Rose: Error, height can't be negative
Height update rejected
Rose: Error, age can't be negative
Age update rejected

Current state: Rose: 25.0cm, 30 days old
```

## Exercício 5

```bash
python3 ex5/ft_plant_types.py
```

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

## Exercício 6

```bash
python3 ex6/ft_garden_analytics.py
```

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

Algumas linhas começam com um espaço (` Color: red`): o espaço faz parte da saída e marca uma
informação extra da planta impressa logo acima.
