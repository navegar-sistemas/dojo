---
sidebar_position: 8
title: Rodar e conferir
---

# Rodar e conferir

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

## Comparar com o enunciado

```bash
diff <(python3 ex5/ft_plant_types.py) - <<'FIM'
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
FIM
```

O `diff` não imprime nada.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex5
.venv/bin/mypy --strict ex5
```

```text
Success: no issues found in 1 source file
```

O exercício 5 está pronto.
