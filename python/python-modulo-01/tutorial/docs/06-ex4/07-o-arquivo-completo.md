---
sidebar_position: 7
title: O arquivo completo
---

# O arquivo completo

A classe com os atributos protegidos, os getters, os setters, o construtor que usa os setters, e
`show()`, `grow()` e `age()` lendo e mudando os atributos protegidos. Depois, as duas funções de
atualização e o bloco main com as quatro etapas da saída:

```python title="ex4/ft_garden_security.py"
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


def update_height(plant: Plant, height: float) -> None:
    if plant.set_height(height):
        print(f"Height updated: {round(plant.get_height())}cm")
    else:
        print("Height update rejected")


def update_age(plant: Plant, age_days: int) -> None:
    if plant.set_age(age_days):
        print(f"Age updated: {plant.get_age()} days")
    else:
        print("Age update rejected")


if __name__ == "__main__":
    print("=== Garden Security System ===")
    rose = Plant("Rose", 15.0, 10)
    print("Plant created: ", end="")
    rose.show()
    print()
    update_height(rose, 25.0)
    update_age(rose, 30)
    print()
    update_height(rose, -5.0)
    update_age(rose, -1)
    print()
    print("Current state: ", end="")
    rose.show()
```

- os valores negativos de teste, `-5.0` e `-1`, são escolhas do projeto; qualquer negativo serve;
- `Plant created: ` e `Current state: ` usam o `end=""` do
  [exercício 3](../05-ex3/04-o-prefixo-created.md), com o `show()` completando a linha;
- os `print()` vazios fazem as linhas vazias entre as etapas.

O arquivo chama `print()` e `round()`.
