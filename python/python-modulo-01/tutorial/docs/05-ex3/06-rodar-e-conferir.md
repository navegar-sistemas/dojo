---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

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

## Comparar com o enunciado

```bash
diff <(python3 ex3/ft_plant_factory.py) - <<'FIM'
=== Plant Factory Output ===
Created: Rose: 25.0cm, 30 days old
Created: Oak: 200.0cm, 365 days old
Created: Cactus: 5.0cm, 90 days old
Created: Sunflower: 80.0cm, 45 days old
Created: Fern: 15.0cm, 120 days old
FIM
```

O `diff` não imprime nada.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex3
.venv/bin/mypy --strict ex3
```

```text
Success: no issues found in 1 source file
```

O exercício 3 está pronto.
