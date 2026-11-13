---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

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

## Comparar com o enunciado

```bash
diff <(python3 ex2/ft_plant_growth.py) - <<'FIM'
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
FIM
```

O `diff` não imprime nada.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex2
.venv/bin/mypy --strict ex2
```

```text
Success: no issues found in 1 source file
```

O exercício 2 está pronto.
