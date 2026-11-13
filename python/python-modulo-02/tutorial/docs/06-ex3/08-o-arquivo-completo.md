---
sidebar_position: 8
title: O arquivo completo
---

# O arquivo completo

Crie `ex3/ft_custom_errors.py` com o conteúdo completo. As classes vêm primeiro, porque as
funções as usam; depois as funções que lançam, as que capturam e o main:

```python title="ex3/ft_custom_errors.py"
class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        self.message = message


class WaterError(GardenError):
    def __init__(self, message: str = "Unknown water error") -> None:
        self.message = message


def wilt_tomato() -> None:
    raise PlantError("The tomato plant is wilting!")


def empty_tank() -> None:
    raise WaterError("Not enough water in the tank!")


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


if __name__ == "__main__":
    print("=== Custom Garden Errors Demo ===")
    test_plant_error()
    test_water_error()
    test_all_garden_errors()
    print("\nAll custom error types work correctly!")
```

Como no [exercício 0](../03-ex0/05-o-arquivo-completo.md), o arquivo termina com uma única quebra
de linha depois da última linha, que o botão de copiar não leva. Os avisos do flake8 sobre o fim
do arquivo estão em [O fim do arquivo](../03-ex0/06-rodar-e-conferir.md#o-fim-do-arquivo).

A única função pronta chamada é `print()`. `PlantError(...)` e `WaterError(...)` criam objetos das
classes do próprio arquivo, que podem ser usadas à vontade.
