---
sidebar_position: 7
title: O arquivo completo
---

# O arquivo completo

```python title="ex4/decorator_mastery.py"
import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def spell_timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result

    return wrapper


def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            power = kwargs["power"] if "power" in kwargs else args[-1]
            if power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print("Spell failed, retrying... "
                              f"(attempt {attempt}/{max_attempts})")
            return f"Spell casting failed after {max_attempts} attempts"

        return wrapper

    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and all(
            char.isalpha() or char == " " for char in name)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


@spell_timer
def fireball() -> str:
    time.sleep(0.1)
    return "Fireball cast!"


@retry_spell(max_attempts=3)
def unstable_spell() -> str:
    raise RuntimeError("The spell backfired")


@retry_spell(max_attempts=3)
def stable_spell() -> str:
    return "Waaaaaaagh spelled !"


def main() -> None:
    print("Testing spell timer...")
    result = fireball()
    print(f"Result: {result}")

    print("\nTesting retrying spell...")
    print(unstable_spell())
    print(stable_spell())

    print("\nTesting MageGuild...")
    print(MageGuild.validate_mage_name("Alex"))
    print(MageGuild.validate_mage_name("Jo"))
    guild = MageGuild()
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Fireball", 5))


if __name__ == "__main__":
    main()
```

O que o arquivo usa, todos autorizados: `functools.wraps` e `staticmethod` (os dois do
enunciado), o módulo `time` da biblioteca padrão (`perf_counter` e `sleep`), `Callable` de
`collections.abc`, `Any` de `typing`, as funções embutidas `len`, `all`, `range` e `print`, e o
método `isalpha` de `str`.
