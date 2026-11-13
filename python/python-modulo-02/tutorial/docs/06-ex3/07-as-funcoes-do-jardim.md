---
sidebar_position: 7
title: As funções do jardim
---

# As funções do jardim

Faltam as funções que lançam os erros e as que os capturam.

## As situações

Duas funções simulam os problemas, cada uma lançando o seu erro com a mensagem da saída
esperada:

```python
def wilt_tomato() -> None:
    raise PlantError("The tomato plant is wilting!")


def empty_tank() -> None:
    raise WaterError("Not enough water in the tank!")
```

`wilt_tomato` ("murchar o tomateiro") é o problema de planta; `empty_tank` ("tanque vazio"), o
de água. Num sistema de verdade, cada uma conferiria um sensor antes de lançar; aqui elas lançam
sempre, porque o objetivo é ver os erros.

## Capturar cada tipo

Um teste para cada tipo, com o `except` do tipo exato:

```python
def test_plant_error() -> None:
    print("\nTesting PlantError...")
    try:
        wilt_tomato()
    except PlantError as error:
        print(f"Caught PlantError: {error}")


def test_water_error() -> None:
    print("\nTesting WaterError...")
    try:
        empty_tank()
    except WaterError as error:
        print(f"Caught WaterError: {error}")
```

## Capturar todos pela base

Os mesmos dois problemas, agora capturados por `except GardenError`:

```python
def test_all_garden_errors() -> None:
    print("\nTesting catching all garden errors...")
    try:
        wilt_tomato()
    except GardenError as error:
        print(f"Caught GardenError: {error}")
    try:
        empty_tank()
    except GardenError as error:
        print(f"Caught GardenError: {error}")
```

São dois `try` separados porque cada chamada lança um erro: com as duas chamadas num `try` só, o
erro de `wilt_tomato` pularia o resto do bloco e `empty_tank` nunca rodaria.

## O main

O main imprime o título, roda os três testes e imprime a mensagem final:

```python
if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===")
    test_plant_error()
    test_water_error()
    test_all_garden_errors()
    print("\nAll custom error types work correctly!")
```

Cada teste começa com `\n`, o que produz a linha vazia antes de cada `Testing` na saída.
