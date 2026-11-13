---
sidebar_position: 6
title: Os arquivos completos
---

# Os arquivos completos

A Parte III acrescenta cinco arquivos e muda pela última vez o `alchemy/__init__.py` e o
`alchemy/potions.py`. Os outros arquivos estão em
[Os arquivos completos da Parte I](../03-parte-1/07-os-arquivos-completos.md) e
[da Parte II](../04-parte-2/05-os-arquivos-completos.md).

```python title="alchemy/transmutation/recipes.py"
from elements import create_fire
from ..elements import create_air
from ..potions import strength_potion


def lead_to_gold() -> str:
    return ("Recipe transmuting Lead to Gold: "
            f"brew '{create_air()}' and '{strength_potion()}' "
            f"mixed with '{create_fire()}'")
```

```python title="alchemy/transmutation/__init__.py"
from .recipes import lead_to_gold

__all__ = ["lead_to_gold"]
```

```python title="alchemy/__init__.py"
from .elements import create_air
from .potions import healing_potion as heal, strength_potion
from .transmutation import lead_to_gold

__all__ = ["create_air", "heal", "strength_potion", "lead_to_gold"]
```

```python title="alchemy/potions.py"
from elements import create_fire, create_water
from .elements import create_air, create_earth


def healing_potion() -> str:
    return (f"Healing potion brewed with '{create_earth()}' "
            f"and '{create_air()}'")


def strength_potion() -> str:
    return (f"Strength potion brewed with '{create_fire()}' "
            f"and '{create_water()}'")
```

```python title="ft_transmutation_0.py"
import alchemy.transmutation.recipes


if __name__ == "__main__":
    print("=== Transmutation 0 ===")
    print("Using file alchemy/transmutation/recipes.py directly")
    print("Testing lead to gold: "
          f"{alchemy.transmutation.recipes.lead_to_gold()}")
```

```python title="ft_transmutation_1.py"
import alchemy.transmutation


if __name__ == "__main__":
    print("=== Transmutation 1 ===")
    print("Import transmutation module directly")
    print(f"Testing lead to gold: {alchemy.transmutation.lead_to_gold()}")
```

```python title="ft_transmutation_2.py"
import alchemy


if __name__ == "__main__":
    print("=== Transmutation 2 ===")
    print("Import alchemy module only")
    print(f"Testing lead to gold: {alchemy.lead_to_gold()}")
```

O que os arquivos importam: só módulos do próprio projeto. Dentro do pacote `alchemy`, os imports
são relativos; o `elements` da raiz e os imports dos scripts são absolutos. A única função
embutida usada é `print`.
