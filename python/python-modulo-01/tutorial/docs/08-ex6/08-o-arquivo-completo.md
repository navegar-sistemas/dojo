---
sidebar_position: 8
title: O arquivo completo
---

# O arquivo completo

`Plant` com a classe aninhada `Stats`, o método estático, o método de classe, os getters novos e
a contagem em `show()`, `grow()` e `age()`; `Flower` como no exercício 5; `Seed` herdando de
`Flower`; `Tree` com a sua `Stats`; `Vegetable` como no exercício 5; a função `display_stats`; e o
bloco main com os cinco blocos da saída:

```python title="ex6/ft_garden_analytics.py"
class Plant:
    class Stats:
        def __init__(self) -> None:
            self._grow_calls = 0
            self._age_calls = 0
            self._show_calls = 0

        def count_grow(self) -> None:
            self._grow_calls += 1

        def count_age(self) -> None:
            self._age_calls += 1

        def count_show(self) -> None:
            self._show_calls += 1

        def display(self) -> None:
            print(
                f"Stats: {self._grow_calls} grow, "
                f"{self._age_calls} age, {self._show_calls} show"
            )

    def __init__(self, name: str, height: float, age_days: int) -> None:
        self._name = name
        self._height = 0.0
        self._age_days = 0
        self._stats = Plant.Stats()
        self.set_height(height)
        self.set_age(age_days)

    @staticmethod
    def is_older_than_a_year(age_days: int) -> bool:
        return age_days > 365

    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0)

    def get_name(self) -> str:
        return self._name

    def get_height(self) -> float:
        return self._height

    def get_age(self) -> int:
        return self._age_days

    def get_stats(self) -> "Plant.Stats":
        return self._stats

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
        self._stats.count_show()
        print(
            f"{self._name}: {round(self._height, 1)}cm, "
            f"{self._age_days} days old"
        )

    def grow(self, centimeters: float) -> None:
        self._stats.count_grow()
        self.set_height(self._height + centimeters)

    def age(self, days: int) -> None:
        self._stats.count_age()
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


class Seed(Flower):
    def __init__(
        self, name: str, height: float, age_days: int, color: str,
        seed_yield: int
    ) -> None:
        super().__init__(name, height, age_days, color)
        self._seed_yield = seed_yield
        self._seeds = 0

    def bloom(self) -> None:
        super().bloom()
        self._seeds = self._seed_yield

    def show(self) -> None:
        super().show()
        print(f" Seeds: {self._seeds}")


class Tree(Plant):
    class Stats(Plant.Stats):
        def __init__(self) -> None:
            super().__init__()
            self._shade_calls = 0

        def count_shade(self) -> None:
            self._shade_calls += 1

        def display(self) -> None:
            super().display()
            print(f" {self._shade_calls} shade")

    _stats: "Tree.Stats"

    def __init__(
        self, name: str, height: float, age_days: int,
        trunk_diameter: float
    ) -> None:
        super().__init__(name, height, age_days)
        self._trunk_diameter = trunk_diameter
        self._stats = Tree.Stats()

    def produce_shade(self) -> None:
        self._stats.count_shade()
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


def display_stats(plant: Plant) -> None:
    print(f"[statistics for {plant.get_name()}]")
    plant.get_stats().display()


if __name__ == "__main__":
    print("=== Garden statistics ===")

    print("=== Check year-old")
    for days in (30, 400):
        older = Plant.is_older_than_a_year(days)
        print(f"Is {days} days more than a year? -> {older}")
    print()

    print("=== Flower")
    rose = Flower("Rose", 15.0, 10, "red")
    rose.show()
    display_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow(8.0)
    rose.bloom()
    rose.show()
    display_stats(rose)
    print()

    print("=== Tree")
    oak = Tree("Oak", 200.0, 365, 5.0)
    oak.show()
    display_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_stats(oak)
    print()

    print("=== Seed")
    sunflower = Seed("Sunflower", 80.0, 45, "yellow", 42)
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow(30.0)
    sunflower.age(20)
    sunflower.bloom()
    sunflower.show()
    display_stats(sunflower)
    print()

    print("=== Anonymous")
    unknown = Plant.anonymous()
    unknown.show()
    display_stats(unknown)
```

Como no [exercício 0](../02-ex0/04-o-arquivo-completo.md), o arquivo termina com uma única quebra
de linha depois da última linha, que o botão de copiar não leva.

- `Vegetable` não aparece na saída deste exercício, mas continua no arquivo: o enunciado pede as
  classes do exercício 5 melhoradas, e uma hortaliça também tem estatísticas, herdadas de
  `Plant`;
- as linhas `[statistics for ...]` saem de `display_stats`; as outras linhas entre colchetes são
  `print` do bloco main.

O arquivo chama `super()`, `print()`, `round()`, `staticmethod()` e `classmethod()` (as duas
últimas pelos decoradores), todas autorizadas. O `range()` também é autorizado, mas não faz falta:
o laço das idades percorre uma tupla.
