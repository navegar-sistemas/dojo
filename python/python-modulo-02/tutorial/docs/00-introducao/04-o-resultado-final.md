---
sidebar_position: 4
title: O resultado final
---

# O resultado final

Esta é a saída de cada programa pronto, igual, letra por letra, à que o enunciado mostra. Cada
exercício do tutorial termina conferindo que o programa imprime exatamente isto. Os comandos só
funcionam depois que os arquivos existirem: a página "Rodar e conferir" de cada exercício os
roda.

## Exercício 0

```bash
python3 ex0/ft_first_exception.py
```

```text
=== Garden Temperature ===

Input data is '25'
Temperature is now 25°C

Input data is 'abc'
Caught input_temperature error: invalid literal for int() with base 10: 'abc'

All tests completed - program didn't crash!
```

## Exercício 1

```bash
python3 ex1/ft_raise_exception.py
```

```text
=== Garden Temperature Checker ===

Input data is '25'
Temperature is now 25°C

Input data is 'abc'
Caught input_temperature error: invalid literal for int() with base 10: 'abc'

Input data is '100'
Caught input_temperature error: 100°C is too hot for plants (max 40°C)

Input data is '-50'
Caught input_temperature error: -50°C is too cold for plants (min 0°C)

All tests completed - program didn't crash!
```

## Exercício 2

```bash
python3 ex2/ft_different_errors.py
```

```text
=== Garden Error Types Demo ===
Testing operation 0...
Caught ValueError: invalid literal for int() with base 10: 'abc'
Testing operation 1...
Caught ZeroDivisionError: division by zero
Testing operation 2...
Caught FileNotFoundError: [Errno 2] No such file or directory: '/non/existent/file'
Testing operation 3...
Caught TypeError: can only concatenate str (not "int") to str
Testing operation 4...
Operation completed successfully

All error types tested successfully!
```

## Exercício 3

```bash
python3 ex3/ft_custom_errors.py
```

```text
=== Custom Garden Errors Demo ===

Testing PlantError...
Caught PlantError: The tomato plant is wilting!

Testing WaterError...
Caught WaterError: Not enough water in the tank!

Testing catching all garden errors...
Caught GardenError: The tomato plant is wilting!
Caught GardenError: Not enough water in the tank!

All custom error types work correctly!
```

## Exercício 4

```bash
python3 ex4/ft_finally_block.py
```

```text
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
```
