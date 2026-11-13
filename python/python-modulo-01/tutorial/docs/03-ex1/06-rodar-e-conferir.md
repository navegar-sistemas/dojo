---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

```bash
python3 ex1/ft_garden_data.py
```

```text
=== Garden Plant Registry ===
Rose: 25cm, 30 days old
Sunflower: 80cm, 45 days old
Cactus: 15cm, 120 days old
```

## Comparar com o enunciado

O mesmo `diff` do [exercício 0](../02-ex0/05-rodar-e-conferir.md), com a saída deste
exercício:

```bash
diff <(python3 ex1/ft_garden_data.py) - <<'FIM'
=== Garden Plant Registry ===
Rose: 25cm, 30 days old
Sunflower: 80cm, 45 days old
Cactus: 15cm, 120 days old
FIM
```

O `diff` não imprime nada: as saídas são iguais.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex1
.venv/bin/mypy --strict ex1
```

```text
Success: no issues found in 1 source file
```

O exercício 1 está pronto.
