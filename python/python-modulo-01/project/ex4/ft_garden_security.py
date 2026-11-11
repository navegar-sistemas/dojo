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


if __name__ == "__main__":
    print("=== Garden Security System ===")
    rose: Plant = Plant("Rose", 15.0, 10, 0.8)
    print("Plant created:", end=" ")
    rose.show()
    print()

    if rose.set_height(25.0):
        print(f"Height updated: {rose.get_height():g}cm")
    if rose.set_age(30):
        print(f"Age updated: {rose.get_age()} days")
    print()

    if not rose.set_height(-5.0):
        print("Height update rejected")
    if not rose.set_age(-3):
        print("Age update rejected")
    print()

    print("Current state:", end=" ")
    rose.show()
