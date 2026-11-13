---
sidebar_position: 6
title: O arquivo completo
---

# O arquivo completo

Crie `ex4/ft_finally_block.py` com o conteúdo completo: as duas classes copiadas,
`water_plant`, `test_watering_system` e o main.

```python title="ex4/ft_finally_block.py"
class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        self.message = message


def water_plant(plant_name: str) -> None:
    if plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")


def test_watering_system() -> None:
    tests = (
        ("valid", ("Tomato", "Lettuce", "Carrots")),
        ("invalid", ("Tomato", "lettuce", "Carrots")),
    )
    for label, plants in tests:
        print(f"\nTesting {label} plants...")
        print("Opening watering system")
        try:
            for plant_name in plants:
                water_plant(plant_name)
        except PlantError as error:
            print(f"Caught PlantError: {error}")
            print(".. ending tests and returning to main")
            return
        finally:
            print("Closing watering system")


if __name__ == "__main__":
    print("=== Garden Watering System ===")
    test_watering_system()
    print("\nCleanup always happens, even with errors!")
```

As funções prontas chamadas são `print()` e `capitalize()`, as duas autorizadas.
