---
sidebar_position: 9
title: Rodar e conferir
---

# Rodar e conferir

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

## Comparar com o enunciado

```bash
diff <(python3 ex6/ft_garden_analytics.py) - <<'FIM'
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
FIM
```

O `diff` não imprime nada.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex6
.venv/bin/mypy --strict ex6
```

```text
Success: no issues found in 1 source file
```

O exercício 6 está pronto, e com ele os sete programas.
