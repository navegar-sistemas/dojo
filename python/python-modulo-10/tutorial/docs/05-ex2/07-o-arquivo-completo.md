---
sidebar_position: 7
title: O arquivo completo
---

# O arquivo completo

```python title="ex2/scope_mysteries.py"
from collections.abc import Callable
from typing import Any


def mage_counter() -> Callable:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable:
    total = initial_power

    def accumulate(amount: int) -> int:
        nonlocal total
        total += amount
        return total

    return accumulate


def enchantment_factory(enchantment_type: str) -> Callable:
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return enchant


def memory_vault() -> dict[str, Callable]:
    memories: dict[str, Any] = {}

    def store(key: str, value: Any) -> None:
        memories[key] = value

    def recall(key: str) -> Any:
        return memories.get(key, "Memory not found")

    return {"store": store, "recall": recall}


def main() -> None:
    print("Testing mage counter...")
    counter_a = mage_counter()
    counter_b = mage_counter()
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    base = 100
    accumulate = spell_accumulator(base)
    for amount in [20, 30]:
        print(f"Base {base}, add {amount}: {accumulate(amount)}")

    print("\nTesting enchantment factory...")
    flaming = enchantment_factory("Flaming")
    frozen = enchantment_factory("Frozen")
    print(flaming("Sword"))
    print(frozen("Shield"))

    print("\nTesting memory vault...")
    vault = memory_vault()
    store, recall = vault["store"], vault["recall"]
    key, value = "secret", 42
    store(key, value)
    print(f"Store '{key}' = {value}")
    print(f"Recall '{key}': {recall(key)}")
    print(f"Recall 'unknown': {recall('unknown')}")


if __name__ == "__main__":
    main()
```

O que o arquivo usa, todos autorizados: `Callable` de `collections.abc`, `Any` de `typing`, a
instrução `nonlocal` (duas vezes, nas duas funções que atribuem a uma variável envolvente), o
método `get` de `dict` e `print`. Nenhuma linha usa `global`, e nenhuma variável fica fora de uma
função.
