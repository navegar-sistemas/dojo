---
sidebar_position: 4
title: O arquivo completo
---

# O arquivo completo

```python title="ex6/ft_data_alchemist.py"
import random

PLAYERS = ["Alice", "bob", "Charlie", "dylan", "Emma", "Gregory", "john",
           "kevin", "Liam"]


def main() -> None:
    """Transform and filter player data with comprehensions."""
    print("=== Game Data Alchemist ===")
    print(f"\nInitial list of players: {PLAYERS}")
    capitalized = [name.capitalize() for name in PLAYERS]
    print(f"New list with all names capitalized: {capitalized}")
    already = [name for name in PLAYERS if name == name.capitalize()]
    print(f"New list of capitalized names only: {already}")

    scores = {name: random.randint(0, 1000) for name in capitalized}
    print(f"\nScore dict: {scores}")
    average = sum(scores.values()) / len(scores)
    print(f"Score average is {round(average, 2)}")
    high = {name: scores[name] for name in scores if scores[name] > average}
    print(f"High scores: {high}")


if __name__ == "__main__":
    main()
```

- a lista inicial são os nove nomes do exemplo do enunciado, numa constante;
- os `\n` antes de `Initial list` e de `Score dict` imprimem as linhas vazias da saída;
- cada comprehension cabe numa linha de até 79 caracteres, como o enunciado pede.

O arquivo usa `random.randint`, `print()`, `len()`, `sum()` e `round()`, o método `capitalize`,
liberado pela regra dos tipos, e o método `values` do dicionário, do exercício 4.
