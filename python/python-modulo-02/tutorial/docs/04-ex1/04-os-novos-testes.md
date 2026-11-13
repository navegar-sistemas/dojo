---
sidebar_position: 4
title: Os novos testes
---

# Os novos testes

A função de teste é a mesma do exercício 0, com duas diferenças: o título e as duas entradas
novas na tupla.

```python
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
```

O bloco `except` não mudou: os erros lançados pelo `raise` também são `ValueError`, e o
`{error}` imprime a mensagem que a `input_temperature` escreveu.

| `temp_str` | Quem lança | O que imprime depois de `Caught input_temperature error: ` |
|---|---|---|
| `"25"` | ninguém | (nada: imprime `Temperature is now 25°C`) |
| `"abc"` | o `int()` | `invalid literal for int() with base 10: 'abc'` |
| `"100"` | o primeiro `raise` | `100°C is too hot for plants (max 40°C)` |
| `"-50"` | o segundo `raise` | `-50°C is too cold for plants (min 0°C)` |

O main é o mesmo do exercício 0:

```python
if __name__ == "__main__":
    test_temperature()
```
