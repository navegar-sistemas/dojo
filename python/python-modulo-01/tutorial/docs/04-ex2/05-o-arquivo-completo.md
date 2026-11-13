---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

A classe do exercício 1 com `height` agora `float`, o `show()` arredondando, e os dois métodos
novos. No bloco main, a rosa é criada como antes, com a altura `25.0`, e passa pela semana:

```python title="ex2/ft_plant_growth.py"
class Plant:
    name: str
    height: float
    age_days: int

    def show(self) -> None:
        print(
            f"{self.name}: {round(self.height, 1)}cm, "
            f"{self.age_days} days old"
        )

    def grow(self, centimeters: float) -> None:
        self.height += centimeters

    def age(self, days: int) -> None:
        self.age_days += days


if __name__ == "__main__":
    rose = Plant()
    rose.name = "Rose"
    rose.height = 25.0
    rose.age_days = 30

    print("=== Garden Plant Growth ===")
    rose.show()
    start_height = rose.height
    for day in range(1, 8):
        print(f"=== Day {day} ===")
        rose.grow(0.8)
        rose.age(1)
        rose.show()
    growth = rose.height - start_height
    print(f"Growth this week: {round(growth, 1)}cm")
```

Como no [exercício 0](../02-ex0/04-o-arquivo-completo.md), o arquivo termina com uma única quebra
de linha depois da última linha, que o botão de copiar não leva.

O arquivo chama `print()`, `range()` e `round()`, as três autorizadas, além dos próprios métodos.
