---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

As páginas anteriores mostraram o arquivo em pedaços, para ler. Agora crie
`ex0/ft_first_exception.py` com o conteúdo completo: as três partes juntas, com duas linhas em
branco entre as funções e antes do main, como o flake8 exige:

```python title="ex0/ft_first_exception.py"
def input_temperature(temp_str: str) -> int:
    return int(temp_str)


def test_temperature() -> None:
    print("=== Garden Temperature ===")
    for temp_str in ("25", "abc"):
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

O arquivo só chama `int()` e `print()`, as duas funções autorizadas, além das próprias funções.
