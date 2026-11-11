class Plant:
    def __init__(self, name: str, height: int, age: int) -> None:
        self.name = name
        self.height = height
        self.age = age

    def show(self) -> None:
        plural: str = "s" if self.age != 1 else ""
        print(f"{self.name}: {self.height}cm, {self.age} day{plural} old")


if __name__ == "__main__":
    print("=== Garden Plant Registry ===")
    plants: list[Plant] = [
        Plant("Rose", 25, 30),
        Plant("Sunflower", 80, 45),
        Plant("Cactus", 15, 120),
    ]
    for plant in plants:
        plant.show()
