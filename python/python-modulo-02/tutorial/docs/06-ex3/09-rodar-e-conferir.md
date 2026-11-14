---
sidebar_position: 9
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 ex3/ft_custom_errors.py) - <<'FIM'
=== Custom Garden Errors Demo ===

Testing PlantError...
Caught PlantError: The tomato plant is wilting!

Testing WaterError...
Caught WaterError: Not enough water in the tank!

Testing catching all garden errors...
Caught GardenError: The tomato plant is wilting!
Caught GardenError: Not enough water in the tank!

All custom error types work correctly!
FIM
```

Sem nenhuma linha impressa, a saída é idêntica à do enunciado.

## Conferir as mensagens padrão

A demonstração sempre passa uma mensagem, então ela não mostra as mensagens padrão. Para vê-las,
crie cada erro sem mensagem, do mesmo jeito que na conferência dos limites do
[exercício 1](../04-ex1/06-rodar-e-conferir.md#conferir-os-limites):

```bash
cd ex3
python3 -B -c 'from ft_custom_errors import GardenError, PlantError, WaterError; print(GardenError()); print(PlantError()); print(WaterError())'
cd ..
```

```text
Unknown garden error
Unknown plant error
Unknown water error
```

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex3
.venv/bin/mypy --disallow-untyped-defs ex3
```

```text
Success: no issues found in 1 source file
```
