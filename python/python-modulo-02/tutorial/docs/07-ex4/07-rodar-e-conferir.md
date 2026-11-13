---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 ex4/ft_finally_block.py) - <<'FIM'
=== Garden Watering System ===

Testing valid plants...
Opening watering system
Watering Tomato: [OK]
Watering Lettuce: [OK]
Watering Carrots: [OK]
Closing watering system

Testing invalid plants...
Opening watering system
Watering Tomato: [OK]
Caught PlantError: Invalid plant name to water: 'lettuce'
.. ending tests and returning to main
Closing watering system

Cleanup always happens, even with errors!
FIM
```

Sem nenhuma linha impressa, a saída é idêntica à do enunciado.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex4
.venv/bin/mypy --disallow-untyped-defs ex4
```

```text
Success: no issues found in 1 source file
```
