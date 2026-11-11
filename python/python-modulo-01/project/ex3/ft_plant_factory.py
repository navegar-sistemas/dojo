class Plant:
    def __init__(
        self, name: str, height: float, age_days: int, growth_rate: float
    ) -> None:
        self.name = name
        self.height = height
        self.age_days = age_days
        self.growth_rate = growth_rate

    def show(self) -> None:
        plural: str = "s" if self.age_days != 1 else ""
        print(
            f"{self.name}: {round(self.height, 1)}cm, "
            f"{self.age_days} day{plural} old"
        )

    def grow(self) -> None:
        self.height += self.growth_rate

    def age(self) -> None:
        self.age_days += 1

    def add_day(self) -> None:
        self.grow()
        self.age()
        self.show()


if __name__ == "__main__":
    print("=== Plant Factory Output ===")
    plants: list[Plant] = [
        Plant("Rose", 25.0, 30, 0.8),
        Plant("Oak", 200.0, 365, 1.5),
        Plant("Cactus", 5.0, 90, 0.1),
        Plant("Sunflower", 80.0, 45, 3.0),
        Plant("Fern", 15.0, 120, 0.5),
    ]
    for plant in plants:
        print("Created:", end=" ")
        plant.show()
