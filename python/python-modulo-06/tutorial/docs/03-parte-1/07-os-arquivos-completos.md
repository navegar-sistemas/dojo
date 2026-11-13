---
sidebar_position: 7
title: Os arquivos completos
---

# Os arquivos completos

Os nove arquivos da Parte I, como ficam ao fim dela. O `alchemy/__init__.py` muda de novo nas
Partes II e III; esta é a versão com `__all__`.

## Os componentes

```python title="elements.py"
def create_fire() -> str:
    return "Fire element created"


def create_water() -> str:
    return "Water element created"
```

```python title="alchemy/elements.py"
def create_earth() -> str:
    return "Earth element created"


def create_air() -> str:
    return "Air element created"
```

```python title="alchemy/__init__.py"
from alchemy.elements import create_air

__all__ = ["create_air"]
```

## Os scripts

```python title="ft_alembic_0.py"
import elements


if __name__ == "__main__":
    print("=== Alembic 0 ===")
    print("Using: 'import ...' structure to access elements.py")
    print(f"Testing create_fire: {elements.create_fire()}")
```

```python title="ft_alembic_1.py"
from elements import create_water


if __name__ == "__main__":
    print("=== Alembic 1 ===")
    print("Using: 'from ... import ...' structure to access elements.py")
    print(f"Testing create_water: {create_water()}")
```

```python title="ft_alembic_2.py"
import alchemy.elements


if __name__ == "__main__":
    print("=== Alembic 2 ===")
    print("Accessing alchemy/elements.py using 'import ...' structure")
    print(f"Testing create_earth: {alchemy.elements.create_earth()}")
```

```python title="ft_alembic_3.py"
from alchemy.elements import create_air


if __name__ == "__main__":
    print("=== Alembic 3 ===")
    print("Accessing alchemy/elements.py using "
          "'from ... import ...' structure")
    print(f"Testing create_air: {create_air()}")
```

```python title="ft_alembic_4.py"
import alchemy


if __name__ == "__main__":
    print("=== Alembic 4 ===")
    print("Accessing the alchemy module using 'import alchemy'")
    print(f"Testing create_air: {alchemy.create_air()}")
    print("Now show that not all functions can be reached")
    print("This will raise an exception!")
    print("Testing the hidden create_earth: ", end="")
    # alchemy/__init__.py does not expose create_earth: AttributeError here.
    print(f"{alchemy.create_earth()}")
```

```python title="ft_alembic_5.py"
from alchemy import create_air


if __name__ == "__main__":
    print("=== Alembic 5 ===")
    print("Accessing the alchemy module using 'from alchemy import ...'")
    print(f"Testing create_air: {create_air()}")
```

O que os arquivos importam: só módulos do próprio projeto (`elements`, `alchemy` e
`alchemy.elements`). A única função embutida usada é `print`, e nada mexe em `sys.path`.
