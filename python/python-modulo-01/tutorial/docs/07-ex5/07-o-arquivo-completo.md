---
sidebar_position: 7
title: O arquivo completo
---

# O arquivo completo

A classe `Plant` do exercício 4, sem mudança, as três filhas, e o bloco main com um bloco de
saída por tipo:

```python title="ex5/ft_plant_types.py"
class Plant:
    def __init__(self, name: str, height: float, age_days: int) -> None:
        self._name = name
        self._height = 0.0
        self._age_days = 0
        self.set_height(height)
        self.set_age(age_days)

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age_days

    def set_height(self, height: float) -> bool:
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            return False
        self._height = height
        return True

    def set_age(self, age_days: int) -> bool:
        if age_days < 0:
            print(f"{self._name}: Error, age can't be negative")
            return False
        self._age_days = age_days
        return True

    def show(self) -> None:
        print(
            f"{self._name}: {round(self._height, 1)}cm, "
            f"{self._age_days} days old"
        )

    def grow(self, centimeters: float) -> None:
        self.set_height(self._height + centimeters)

    def age(self, days: int) -> None:
        self.set_age(self._age_days + days)


class Flower(Plant):
    def __init__(
        self, name: str, height: float, age_days: int, color: str
    ) -> None:
        super().__init__(name, height, age_days)
        self._color = color
        self._blooming = False

    def bloom(self) -> None:
        self._blooming = True

    def show(self) -> None:
        super().show()
        print(f" Color: {self._color}")
        if self._blooming:
            print(f" {self._name} is blooming beautifully!")
        else:
            print(f" {self._name} has not bloomed yet")


class Tree(Plant):
    def __init__(
        self, name: str, height: float, age_days: int,
        trunk_diameter: float
    ) -> None:
        super().__init__(name, height, age_days)
        self._trunk_diameter = trunk_diameter

    def produce_shade(self) -> None:
        print(
            f"Tree {self._name} now produces a shade of "
            f"{round(self._height, 1)}cm long and "
            f"{round(self._trunk_diameter, 1)}cm wide."
        )

    def show(self) -> None:
        super().show()
        print(f" Trunk diameter: {round(self._trunk_diameter, 1)}cm")


class Vegetable(Plant):
    def __init__(
        self, name: str, height: float, age_days: int,
        harvest_season: str
    ) -> None:
        super().__init__(name, height, age_days)
        self._harvest_season = harvest_season
        self._nutritional_value = 0.0

    def grow(self, centimeters: float) -> None:
        super().grow(centimeters)
        self._nutritional_value += 0.5

    def age(self, days: int) -> None:
        super().age(days)
        self._nutritional_value += 0.5

    def show(self) -> None:
        super().show()
        print(f" Harvest season: {self._harvest_season}")
        print(f" Nutritional value: {round(self._nutritional_value)}")


if __name__ == "__main__":
    print("=== Garden Plant Types ===")

    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()
    print()

    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print()

    print("=== Vegetable")
    tomato = Vegetable("Tomato", 5.0, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for _ in range(20):
        tomato.grow(2.1)
        tomato.age(1)
    tomato.show()
```

Como no [exercício 0](../02-ex0/04-o-arquivo-completo.md), o arquivo termina com uma única quebra
de linha depois da última linha, que o botão de copiar não leva.

As funções de atualização do exercício 4 (`update_height` e `update_age`) ficaram de fora: eram
da demonstração daquele exercício, e esta não as usa. O arquivo chama `super()`, `print()`,
`range()` e `round()`, as quatro autorizadas.
