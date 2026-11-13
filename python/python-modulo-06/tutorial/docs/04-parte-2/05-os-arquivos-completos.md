---
sidebar_position: 5
title: Os arquivos completos
---

# Os arquivos completos

A Parte II acrescenta três arquivos e muda o `alchemy/__init__.py`. Os arquivos da Parte I que
não mudaram estão em [Os arquivos completos da Parte I](../03-parte-1/07-os-arquivos-completos.md).

```python title="alchemy/potions.py"
from alchemy.elements import create_air, create_earth
from elements import create_fire, create_water


def healing_potion() -> str:
    return (f"Healing potion brewed with '{create_earth()}' "
            f"and '{create_air()}'")


def strength_potion() -> str:
    return (f"Strength potion brewed with '{create_fire()}' "
            f"and '{create_water()}'")
```

```python title="alchemy/__init__.py"
from alchemy.elements import create_air
from alchemy.potions import healing_potion as heal, strength_potion

__all__ = ["create_air", "heal", "strength_potion"]
```

```python title="ft_distillation_0.py"
from alchemy.potions import healing_potion, strength_potion


if __name__ == "__main__":
    print("=== Distillation 0 ===")
    print("Direct access to alchemy/potions.py")
    print(f"Testing strength_potion: {strength_potion()}")
    print(f"Testing healing_potion: {healing_potion()}")
```

```python title="ft_distillation_1.py"
import alchemy


if __name__ == "__main__":
    print("=== Distillation 1 ===")
    print("Using: 'import alchemy' structure to access potions")
    print(f"Testing strength_potion: {alchemy.strength_potion()}")
    print(f"Testing heal alias: {alchemy.heal()}")
```

O que os arquivos importam: só módulos do próprio projeto (`elements`, `alchemy`,
`alchemy.elements` e `alchemy.potions`). A única função embutida usada é `print`.
