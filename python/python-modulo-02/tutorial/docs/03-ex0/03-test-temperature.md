---
sidebar_position: 3
title: test_temperature
---

# test_temperature

A função de teste chama `input_temperature` com cada entrada e imprime o resultado ou o erro.
Ela não recebe nada e não devolve nada, por isso o type hint é só `-> None`.

```python
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
```

Bloco por bloco:

1. **O título.** `print("=== Garden Temperature ===")`.
2. **Um laço sobre as entradas.** `("25", "abc")` é uma tupla com as duas entradas que o
   enunciado manda testar. O `for` roda o corpo uma vez para cada uma.
3. **A entrada.** `f"\nInput data is '{temp_str}'"`: o `\n` imprime a linha vazia que separa os
   testes, e as aspas simples em volta de `{temp_str}` aparecem na saída (`Input data is '25'`).
4. **O `try`.** Se `input_temperature` devolver um número, a linha seguinte imprime
   `Temperature is now 25°C`.
5. **O `except`.** Se `input_temperature` lançar `ValueError`, a linha do `Temperature is now` é
   pulada e o `except` imprime a mensagem do erro depois de `Caught input_temperature error: `.
6. **O fim.** Depois do laço, a última mensagem. Ela só aparece porque nenhum erro escapou: é a
   prova de que o programa não travou.

O `try` fica **dentro** do `for`. Assim, um erro numa entrada é capturado e o laço segue para a
próxima. Com o `try` em volta do `for` inteiro, o primeiro erro pularia todas as entradas
restantes.

## As duas voltas do laço

| Volta | `temp_str` | O que acontece | O que imprime |
|---|---|---|---|
| 1 | `"25"` | `input_temperature` devolve `25` | `Temperature is now 25°C` |
| 2 | `"abc"` | `int("abc")` lança `ValueError`; o `except` captura | `Caught input_temperature error: invalid literal for int() with base 10: 'abc'` |
