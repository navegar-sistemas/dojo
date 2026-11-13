---
sidebar_position: 6
title: A demonstração
---

# A demonstração

O `main` entra no fim do arquivo, depois de `spell_dispatcher`, e imprime a saída do enunciado:

```python
def main() -> None:
    print("\nTesting spell reducer...")
    powers = [10, 20, 30, 40]
    print(f"Sum: {spell_reducer(powers, 'add')}")
    print(f"Product: {spell_reducer(powers, 'multiply')}")
    print(f"Max: {spell_reducer(powers, 'max')}")

    print("\nTesting memoized fibonacci...")
    for n in [0, 1, 10, 15]:
        print(f"Fib({n}): {memoized_fibonacci(n)}")

    print("\nTesting spell dispatcher...")
    dispatcher = spell_dispatcher()
    print(dispatcher(42))
    print(dispatcher("fireball"))
    print(dispatcher(["fireball", "heal", "shield"]))
    print(dispatcher(3.14))


if __name__ == "__main__":
    main()
```

- **reducer:** os poderes 10, 20, 30 e 40 dão a soma 100, o produto 240000 e o maior 40, os três
  números do enunciado. Dentro da f-string com aspas duplas, o nome da operação vai entre aspas
  simples;
- **fibonacci:** o `for` percorre os quatro valores de `n` do exemplo. As chamadas aproveitam o
  cache umas das outras: `Fib(15)` reaproveita tudo o que `Fib(10)` calculou;
- **dispatcher:** um argumento de cada tipo registrado, e um `float` (`3.14`), que não tem versão
  registrada e cai na função base. A lista tem três feitiços, por isso `Multi-cast: 3 spells`.

O `\n` no começo do primeiro `print` produz a linha vazia do começo da saída, como no exemplo.
`partial_enchanter` não aparece na saída do enunciado, e a demonstração segue o exemplo; ele é
testado em [Rodar e conferir](./08-rodar-e-conferir.md#partial_enchanter).
