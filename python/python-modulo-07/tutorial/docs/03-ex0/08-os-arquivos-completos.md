---
sidebar_position: 8
title: Os arquivos completos
---

# Os arquivos completos

O pacote `ex0` tem três arquivos, e o programa de teste fica na raiz.

## `ex0/creature.py`

```python title="ex0/creature.py"
from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        self.name = name
        self.creature_type = creature_type

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return f"{self.name} is a {self.creature_type} type Creature"


class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return f"{self.name} uses Ember!"


class Pyrodon(Creature):
    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self) -> str:
        return f"{self.name} uses Flamethrower!"


class Aquabub(Creature):
    def __init__(self) -> None:
        super().__init__("Aquabub", "Water")

    def attack(self) -> str:
        return f"{self.name} uses Water Gun!"


class Torragon(Creature):
    def __init__(self) -> None:
        super().__init__("Torragon", "Water")

    def attack(self) -> str:
        return f"{self.name} uses Hydro Pump!"
```

## `ex0/factory.py`

```python title="ex0/factory.py"
from abc import ABC, abstractmethod

from .creature import Aquabub, Creature, Flameling, Pyrodon, Torragon


class CreatureFactory(ABC):
    @abstractmethod
    def create_base(self) -> Creature:
        pass

    @abstractmethod
    def create_evolved(self) -> Creature:
        pass


class FlameFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Flameling()

    def create_evolved(self) -> Creature:
        return Pyrodon()


class AquaFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Aquabub()

    def create_evolved(self) -> Creature:
        return Torragon()
```

## `ex0/__init__.py`

```python title="ex0/__init__.py"
from .factory import AquaFactory, CreatureFactory, FlameFactory

__all__ = ["CreatureFactory", "FlameFactory", "AquaFactory"]
```

## `battle.py`

```python title="battle.py"
from ex0 import AquaFactory, CreatureFactory, FlameFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    base = factory.create_base()
    evolved = factory.create_evolved()
    for creature in [base, evolved]:
        print(creature.describe())
        print(creature.attack())


def test_battle(first: CreatureFactory, second: CreatureFactory) -> None:
    print("Testing battle")
    one = first.create_base()
    two = second.create_base()
    print(one.describe())
    print(" vs.")
    print(two.describe())
    print(" fight!")
    print(one.attack())
    print(two.attack())


def main() -> None:
    flame = FlameFactory()
    aqua = AquaFactory()
    test_factory(flame)
    print()
    test_factory(aqua)
    print()
    test_battle(flame, aqua)


if __name__ == "__main__":
    main()
```

O que os arquivos usam, todos autorizados: `abc` (`ABC` e `abstractmethod`), a função embutida
`print`, e os imports do próprio pacote (`.creature`, `.factory` e `ex0`). Nenhum `import` de
`typing` é necessário: os type hints usam só classes (`str`, `Creature`, `CreatureFactory`) e o
`None`.
