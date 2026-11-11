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
    print("=== Garden Plant Growth ===")
    rose: Plant = Plant("Rose", 25.0, 30, 0.8)
    initial_height: float = rose.height
    rose.show()
    for i in range(1, 8):
        print(f"=== Day {i} ===")
        rose.add_day()
    diff: float = round(rose.height - initial_height, 1)
    print(f"Growth this week: {diff}cm")
