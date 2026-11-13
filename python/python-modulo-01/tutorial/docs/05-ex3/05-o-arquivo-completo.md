---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

A classe do exercício 2 com o construtor no lugar das declarações; `show()`, `grow()` e `age()`
iguais. No bloco main, as cinco plantas e o laço:

```python title="ex3/ft_plant_factory.py"
class Plant:
    def __init__(self, name: str, height: float, age_days: int) -> None:
        self.name = name
        self.height = height
        self.age_days = age_days

    def show(self) -> None:
        print(
            f"{self.name}: {round(self.height, 1)}cm, "
            f"{self.age_days} days old"
        )

    def grow(self, centimeters: float) -> None:
        self.height += centimeters

    def age(self, days: int) -> None:
        self.age_days += days


if __name__ == "__main__":
    plants = [
        Plant("Rose", 25.0, 30),
        Plant("Oak", 200.0, 365),
        Plant("Cactus", 5.0, 90),
        Plant("Sunflower", 80.0, 45),
        Plant("Fern", 15.0, 120),
    ]
    print("=== Plant Factory Output ===")
    for plant in plants:
        print("Created: ", end="")
        plant.show()
```

Como no [exercício 0](../02-ex0/04-o-arquivo-completo.md), o arquivo termina com uma única quebra
de linha depois da última linha, que o botão de copiar não leva.

`grow()` e `age()` não são chamados neste programa, mas continuam na classe: o enunciado pede
plantas prontas para crescer logo depois de criadas, e a classe é a mesma que evolui de exercício
em exercício. O arquivo chama `print()` e `round()`.
