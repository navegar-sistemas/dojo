---
sidebar_position: 6
title: Os arquivos completos
---

# Os arquivos completos

A Parte IV acrescenta os cinco arquivos do grimório e os dois últimos scripts. Os outros arquivos
estão nas páginas "Os arquivos completos" das Partes
[I](../03-parte-1/07-os-arquivos-completos.md), [II](../04-parte-2/05-os-arquivos-completos.md) e
[III](../05-parte-3/06-os-arquivos-completos.md).

## O grimório

```python title="alchemy/grimoire/__init__.py"
from .light_spellbook import light_spell_record

__all__ = ["light_spell_record"]
```

```python title="alchemy/grimoire/light_spellbook.py"
from .light_validator import validate_ingredients


def light_spell_allowed_ingredients() -> list[str]:
    return ["earth", "air", "fire", "water"]


def light_spell_record(spell_name: str, ingredients: str) -> str:
    validation = validate_ingredients(ingredients)
    if validation.endswith(" - VALID"):
        return f"Spell recorded: {spell_name} ({validation})"
    return f"Spell rejected: {spell_name} ({validation})"
```

```python title="alchemy/grimoire/light_validator.py"
def validate_ingredients(ingredients: str) -> str:
    # Imported at call time: light_spellbook.py imports this module while it
    # loads, so importing it back at the top of this file would be circular.
    from .light_spellbook import light_spell_allowed_ingredients

    text = ingredients.lower()
    for allowed in light_spell_allowed_ingredients():
        if allowed in text:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
```

```python title="alchemy/grimoire/dark_spellbook.py"
# Circular on purpose: dark_validator.py imports this module back.
from .dark_validator import validate_ingredients


def dark_spell_allowed_ingredients() -> list[str]:
    return ["bats", "frogs", "arsenic", "eyeball"]


def dark_spell_record(spell_name: str, ingredients: str) -> str:
    validation = validate_ingredients(ingredients)
    if validation.endswith(" - VALID"):
        return f"Spell recorded: {spell_name} ({validation})"
    return f"Spell rejected: {spell_name} ({validation})"
```

```python title="alchemy/grimoire/dark_validator.py"
# Circular on purpose: dark_spellbook.py imports this module too.
from .dark_spellbook import dark_spell_allowed_ingredients


def validate_ingredients(ingredients: str) -> str:
    text = ingredients.lower()
    for allowed in dark_spell_allowed_ingredients():
        if allowed in text:
            return f"{ingredients} - VALID"
    return f"{ingredients} - INVALID"
```

## Os scripts

```python title="ft_kaboom_0.py"
import alchemy.grimoire


if __name__ == "__main__":
    print("=== Kaboom 0 ===")
    print("Using grimoire module directly")
    record = alchemy.grimoire.light_spell_record("Fantasy",
                                                 "Earth, wind and fire")
    print(f"Testing record light spell: {record}")
```

```python title="ft_kaboom_1.py"
if __name__ == "__main__":
    print("=== Kaboom 1 ===")
    print("Access to alchemy/grimoire/dark_spellbook.py directly")
    print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    # Imported only here, after the prints: the circular import inside
    # dark_spellbook.py raises ImportError before anything below runs.
    from alchemy.grimoire.dark_spellbook import dark_spell_record
    print("Testing record dark spell: "
          f"{dark_spell_record('Curse', 'Bats and frogs')}")
```

O que os arquivos importam: só módulos do próprio projeto, todos com import relativo dentro do
grimório. A única função embutida usada é `print`; dos métodos de texto, `lower` e `endswith`.
