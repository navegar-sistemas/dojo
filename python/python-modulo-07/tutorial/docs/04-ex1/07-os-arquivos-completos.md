---
sidebar_position: 7
title: Os arquivos completos
---

# Os arquivos completos

O pacote `ex1` tem quatro arquivos, e o programa de teste fica na raiz. O pacote `ex0` não muda.

## `ex1/capability.py`

```python title="ex1/capability.py"
from abc import ABC, abstractmethod


class HealCapability(ABC):
    @abstractmethod
    def heal(self) -> str:
        pass


class TransformCapability(ABC):
    def __init__(self) -> None:
        self.transformed = False

    @abstractmethod
    def transform(self) -> str:
        pass

    @abstractmethod
    def revert(self) -> str:
        pass
```

## `ex1/creature.py`

```python title="ex1/creature.py"
from ex0.creature import Creature

from .capability import HealCapability, TransformCapability


class Sproutling(Creature, HealCapability):
    def __init__(self) -> None:
        super().__init__("Sproutling", "Grass")

    def attack(self) -> str:
        return f"{self.name} uses Vine Whip!"

    def heal(self) -> str:
        return f"{self.name} heals itself for a small amount"


class Bloomelle(Creature, HealCapability):
    def __init__(self) -> None:
        super().__init__("Bloomelle", "Grass/Fairy")

    def attack(self) -> str:
        return f"{self.name} uses Petal Dance!"

    def heal(self) -> str:
        return f"{self.name} heals itself and others for a large amount"


class Shiftling(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Shiftling", "Normal")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self.transformed:
            return f"{self.name} performs a boosted strike!"
        return f"{self.name} attacks normally."

    def transform(self) -> str:
        self.transformed = True
        return f"{self.name} shifts into a sharper form!"

    def revert(self) -> str:
        self.transformed = False
        return f"{self.name} returns to normal."


class Morphagon(Creature, TransformCapability):
    def __init__(self) -> None:
        Creature.__init__(self, "Morphagon", "Normal/Dragon")
        TransformCapability.__init__(self)

    def attack(self) -> str:
        if self.transformed:
            return f"{self.name} unleashes a devastating morph strike!"
        return f"{self.name} attacks normally."

    def transform(self) -> str:
        self.transformed = True
        return f"{self.name} morphs into a dragonic battle form!"

    def revert(self) -> str:
        self.transformed = False
        return f"{self.name} stabilizes its form."
```

## `ex1/factory.py`

```python title="ex1/factory.py"
from ex0 import CreatureFactory
from ex0.creature import Creature

from .creature import Bloomelle, Morphagon, Shiftling, Sproutling


class HealingCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Sproutling()

    def create_evolved(self) -> Creature:
        return Bloomelle()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Shiftling()

    def create_evolved(self) -> Creature:
        return Morphagon()
```

## `ex1/__init__.py`

```python title="ex1/__init__.py"
from .factory import HealingCreatureFactory, TransformCreatureFactory

__all__ = ["HealingCreatureFactory", "TransformCreatureFactory"]
```

## `capacitor.py`

```python title="capacitor.py"
from ex0.creature import Creature
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1.capability import HealCapability, TransformCapability


def test_healing(creature: Creature) -> None:
    print(creature.describe())
    print(creature.attack())
    if isinstance(creature, HealCapability):
        print(creature.heal())


def test_transform(creature: Creature) -> None:
    print(creature.describe())
    print(creature.attack())
    if isinstance(creature, TransformCapability):
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())


def main() -> None:
    print("Testing Creature with healing capability")
    healing = HealingCreatureFactory()
    print(" base:")
    test_healing(healing.create_base())
    print(" evolved:")
    test_healing(healing.create_evolved())
    print()
    print("Testing Creature with transform capability")
    transform = TransformCreatureFactory()
    print(" base:")
    test_transform(transform.create_base())
    print(" evolved:")
    test_transform(transform.create_evolved())


if __name__ == "__main__":
    main()
```

O que os arquivos usam, todos autorizados: `abc` (`ABC` e `abstractmethod`), as funções
embutidas `isinstance` e `print`, e os imports do próprio projeto (`ex0`, `ex0.creature`,
`ex1`, `ex1.capability` e os relativos `.capability`, `.creature` e `.factory`).
