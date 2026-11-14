---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

A classe do exercício 2 com o construtor no lugar das declarações; `show()`, `grow()` e `age()`
iguais. No bloco main, as cinco plantas e o laço:

```python title="ex3/ft_plant_factory.py"
class Plant:
    def __init__(
        self, name: str, height: float, age_days: int, growth_rate: float
    ) -> None:
        self.name = name
        self.height = height
        self.age_days = age_days
        self.growth_rate = growth_rate

    def show(self) -> None:
        print(
            f"{self.name}: {round(self.height, 1)}cm, "
            f"{self.age_days} days old"
        )

    def grow(self) -> None:
        self.height += self.growth_rate

    def age(self) -> None:
        self.age_days += 1


if __name__ == "__main__":
    plants = [
        Plant("Rose", 25.0, 30, 0.8),
        Plant("Oak", 200.0, 365, 1.5),
        Plant("Cactus", 5.0, 90, 0.1),
        Plant("Sunflower", 80.0, 45, 3.0),
        Plant("Fern", 15.0, 120, 0.5),
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
