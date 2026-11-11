class Plant:
    def __init__(
        self, name: str, height: float, age_days: int, growth_rate: float
    ) -> None:
        self._name = name
        self._growth_rate = growth_rate
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
        plural: str = "s" if self._age_days != 1 else ""
        print(
            f"{self._name}: {round(self._height, 1)}cm, "
            f"{self._age_days} day{plural} old"
        )

    def grow(self) -> None:
        self.set_height(self._height + self._growth_rate)

    def age(self) -> None:
        self.set_age(self._age_days + 1)

    def add_day(self) -> None:
        self.grow()
        self.age()
        self.show()


class Flower(Plant):
    def __init__(
        self,
        name: str,
        height: float,
        age_days: int,
        growth_rate: float,
        color: str,
    ) -> None:
        super().__init__(name, height, age_days, growth_rate)
        self._color = color
        self._bloomed = False

    def bloom(self) -> None:
        self._bloomed = True

    def show(self) -> None:
        super().show()
        print(f" Color: {self._color}")
        if self._bloomed:
            print(f" {self._name} is blooming beautifully!")
        else:
            print(f" {self._name} has not bloomed yet")


class Tree(Plant):
    def __init__(
        self,
        name: str,
        height: float,
        age_days: int,
        growth_rate: float,
        trunk_diameter: float,
    ) -> None:
        super().__init__(name, height, age_days, growth_rate)
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
        self,
        name: str,
        height: float,
        age_days: int,
        growth_rate: float,
        harvest_season: str,
    ) -> None:
        super().__init__(name, height, age_days, growth_rate)
        self._harvest_season = harvest_season
        self._nutritional_value = 0.0

    def grow(self) -> None:
        super().grow()
        self._nutritional_value += 0.5

    def age(self) -> None:
        super().age()
        self._nutritional_value += 0.5

    def show(self) -> None:
        super().show()
        print(f" Harvest season: {self._harvest_season}")
        print(f" Nutritional value: {self._nutritional_value:g}")


if __name__ == "__main__":
    print("=== Garden Plant Types ===")

    print("=== Flower")
    rose: Flower = Flower("Rose", 15.0, 10, 0.8, "red")
    rose.show()
    print("[asking the rose to bloom]")
    rose.bloom()
    rose.show()
    print()

    print("=== Tree")
    oak: Tree = Tree("Oak", 200.0, 365, 1.5, 5.0)
    oak.show()
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    print()

    print("=== Vegetable")
    tomato: Vegetable = Vegetable("Tomato", 5.0, 10, 2.1, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for _ in range(20):
        tomato.grow()
        tomato.age()
    tomato.show()
