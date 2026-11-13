---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

Crie `ex1/ft_raise_exception.py` com o conteúdo completo: as constantes, a nova
`input_temperature`, a nova `test_temperature` e o main.

```python title="ex1/ft_raise_exception.py"
MIN_TEMPERATURE = 0
MAX_TEMPERATURE = 40


def input_temperature(temp_str: str) -> int:
    temperature = int(temp_str)
    if temperature > MAX_TEMPERATURE:
        raise ValueError(
            f"{temperature}°C is too hot for plants (max {MAX_TEMPERATURE}°C)"
        )
    if temperature < MIN_TEMPERATURE:
        raise ValueError(
            f"{temperature}°C is too cold for plants (min {MIN_TEMPERATURE}°C)"
        )
    return temperature


def test_temperature() -> None:
    print("=== Garden Temperature Checker ===")
    for temp_str in ("25", "abc", "100", "-50"):
        print(f"\nInput data is '{temp_str}'")
        try:
            temperature = input_temperature(temp_str)
            print(f"Temperature is now {temperature}°C")
        except ValueError as error:
            print(f"Caught input_temperature error: {error}")
    print("\nAll tests completed - program didn't crash!")


if __name__ == "__main__":
    test_temperature()
```

O arquivo continua chamando só `int()` e `print()`. `raise` e `ValueError(...)` não contam como
funções chamadas: `raise` é palavra da linguagem, liberada pelo enunciado, e `ValueError` é um
tipo de exceção embutido, que o enunciado manda usar.
