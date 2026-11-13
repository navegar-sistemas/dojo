---
sidebar_position: 8
title: O arquivo completo
---

# O arquivo completo

```python title="ex1/higher_magic.py"
from collections.abc import Callable


def fireball(target: str, power: int) -> str:
    return f"Fireball hits {target}"


def heal(target: str, power: int) -> str:
    return f"Heals {target}"


def power_echo(target: str, power: int) -> str:
    return str(power)


def is_strong(target: str, power: int) -> bool:
    return power >= 15


def spell_combiner(spell1: Callable, spell2: Callable) -> Callable:
    if not callable(spell1) or not callable(spell2):
        raise TypeError("spell_combiner needs two callable spells")

    def combined(target: str, power: int) -> tuple[str, str]:
        return spell1(target, power), spell2(target, power)

    return combined


def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    if not callable(base_spell):
        raise TypeError("power_amplifier needs a callable spell")

    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplified


def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    if not callable(condition) or not callable(spell):
        raise TypeError("conditional_caster needs a callable condition "
                        "and a callable spell")

    def caster(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return caster


def spell_sequence(spells: list[Callable]) -> Callable:
    if not all(callable(spell) for spell in spells):
        raise TypeError("spell_sequence needs a list of callable spells")

    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]

    return sequence


def main() -> None:
    print("\nTesting spell combiner...")
    combined = spell_combiner(fireball, heal)
    print(f"Combined spell result: {', '.join(combined('Dragon', 10))}")

    print("\nTesting power amplifier...")
    mega_echo = power_amplifier(power_echo, 3)
    print(f"Original: {power_echo('Dragon', 10)}, "
          f"Amplified: {mega_echo('Dragon', 10)}")

    print("\nTesting conditional caster...")
    careful_fireball = conditional_caster(is_strong, fireball)
    print(f"Power 20: {careful_fireball('Goblin', 20)}")
    print(f"Power 5: {careful_fireball('Goblin', 5)}")

    print("\nTesting spell sequence...")
    combo = spell_sequence([fireball, heal, mega_echo])
    print(f"Sequence result: {combo('Wizard', 12)}")


if __name__ == "__main__":
    main()
```

O que o arquivo usa, todos autorizados: `Callable` de `collections.abc`, as funções embutidas
`callable`, `all`, `str` e `print`, o método `join` de `str`, e compreensões de lista. Cada função
de dentro (`combined`, `amplified`, `caster`, `sequence`) tem type hints nos parâmetros e no
retorno.
