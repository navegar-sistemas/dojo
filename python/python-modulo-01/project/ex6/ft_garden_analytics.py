class Plant:
    class Stats:
        def __init__(self) -> None:
            self._grow_calls = 0
            self._age_calls = 0
            self._show_calls = 0

        def record_grow(self) -> None:
            self._grow_calls += 1

        def record_age(self) -> None:
            self._age_calls += 1

        def record_show(self) -> None:
            self._show_calls += 1

        def display(self) -> None:
            print(
                f"Stats: {self._grow_calls} grow, "
                f"{self._age_calls} age, {self._show_calls} show"
            )

    def __init__(
        self, name: str, height: float, age_days: int, growth_rate: float
    ) -> None:
        self._name = name
        self._growth_rate = growth_rate
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
        return Plant("Unknown plant", 0.0, 0, 0.0)

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
        self._stats.record_show()
        plural: str = "s" if self._age_days != 1 else ""
        print(
            f"{self._name}: {round(self._height, 1)}cm, "
            f"{self._age_days} day{plural} old"
        )

    def grow(self) -> None:
        self._stats.record_grow()
        self.set_height(self._height + self._growth_rate)

    def age(self, days: int = 1) -> None:
        self._stats.record_age()
        if days < 0:
            print(f"{self._name}: Error, days can't be negative")
            return
        self.set_age(self._age_days + days)

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


class Seed(Flower):
    def __init__(
        self,
        name: str,
        height: float,
        age_days: int,
        growth_rate: float,
        color: str,
        seeds_per_bloom: int,
    ) -> None:
        super().__init__(name, height, age_days, growth_rate, color)
        self._seeds_per_bloom = seeds_per_bloom
        self._seeds = 0

    def bloom(self) -> None:
        super().bloom()
        self._seeds = self._seeds_per_bloom

    def show(self) -> None:
        super().show()
        print(f" Seeds: {self._seeds}")


class Tree(Plant):
    class Stats(Plant.Stats):
        def __init__(self) -> None:
            super().__init__()
            self._shade_calls = 0

        def record_shade(self) -> None:
            self._shade_calls += 1

        def display(self) -> None:
            super().display()
            print(f" {self._shade_calls} shade")

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
        self._tree_stats = Tree.Stats()
        self._stats = self._tree_stats

    def produce_shade(self) -> None:
        self._tree_stats.record_shade()
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

    def age(self, days: int = 1) -> None:
        previous_age: int = self._age_days
        super().age(days)
        self._nutritional_value += 0.5 * (self._age_days - previous_age)

    def show(self) -> None:
        super().show()
        print(f" Harvest season: {self._harvest_season}")
        print(f" Nutritional value: {self._nutritional_value:g}")


def display_stats(plant: Plant) -> None:
    print(f"[statistics for {plant.get_name()}]")
    plant.get_stats().display()


if __name__ == "__main__":
    print("=== Garden statistics ===")

    print("=== Check year-old")
    for days in (30, 400):
        print(
            f"Is {days} days more than a year? -> "
            f"{Plant.is_older_than_a_year(days)}"
        )
    print()

    print("=== Flower")
    rose: Flower = Flower("Rose", 15.0, 10, 8.0, "red")
    rose.show()
    display_stats(rose)
    print("[asking the rose to grow and bloom]")
    rose.grow()
    rose.bloom()
    rose.show()
    display_stats(rose)
    print()

    print("=== Tree")
    oak: Tree = Tree("Oak", 200.0, 365, 1.5, 5.0)
    oak.show()
    display_stats(oak)
    print("[asking the oak to produce shade]")
    oak.produce_shade()
    display_stats(oak)
    print()

    print("=== Seed")
    sunflower: Seed = Seed("Sunflower", 80.0, 45, 30.0, "yellow", 42)
    sunflower.show()
    print("[make sunflower grow, age and bloom]")
    sunflower.grow()
    sunflower.age(20)
    sunflower.bloom()
    sunflower.show()
    display_stats(sunflower)
    print()

    print("=== Anonymous")
    unknown: Plant = Plant.anonymous()
    unknown.show()
    display_stats(unknown)
