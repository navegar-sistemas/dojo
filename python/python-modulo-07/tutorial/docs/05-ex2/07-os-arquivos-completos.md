---
sidebar_position: 7
title: Os arquivos completos
---

# Os arquivos completos

O pacote `ex2` tem dois arquivos, e o programa de teste fica na raiz. Os pacotes `ex0` e `ex1`
não mudam.

## `ex2/strategy.py`

```python title="ex2/strategy.py"
from abc import ABC, abstractmethod

from ex0.creature import Creature
from ex1.capability import HealCapability, TransformCapability


class InvalidStrategyError(Exception):
    pass


class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        pass


class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        return [creature.attack()]


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, TransformCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this aggressive strategy")
        return [creature.transform(), creature.attack(), creature.revert()]


class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, HealCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this defensive strategy")
        return [creature.attack(), creature.heal()]
```

## `ex2/__init__.py`

```python title="ex2/__init__.py"
from .strategy import (
    AggressiveStrategy,
    BattleStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
    NormalStrategy,
)

__all__ = [
    "BattleStrategy",
    "NormalStrategy",
    "AggressiveStrategy",
    "DefensiveStrategy",
    "InvalidStrategyError",
]
```

## `tournament.py`

```python title="tournament.py"
from ex0 import AquaFactory, CreatureFactory, FlameFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import (
    AggressiveStrategy,
    BattleStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
    NormalStrategy,
)


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]]) -> None:
    print("*** Tournament ***")
    print(f"{len(opponents)} opponents involved")
    fighters = []
    for factory, strategy in opponents:
        fighters.append((factory.create_base(), strategy))
    try:
        for i in range(len(fighters)):
            for j in range(i + 1, len(fighters)):
                one, one_strategy = fighters[i]
                two, two_strategy = fighters[j]
                print()
                print("* Battle *")
                print(one.describe())
                print(" vs.")
                print(two.describe())
                print(" now fight!")
                for line in one_strategy.act(one):
                    print(line)
                for line in two_strategy.act(two):
                    print(line)
    except InvalidStrategyError as error:
        print(f"Battle error, aborting tournament: {error}")


def main() -> None:
    flame = FlameFactory()
    aqua = AquaFactory()
    healing = HealingCreatureFactory()
    transform = TransformCreatureFactory()
    normal = NormalStrategy()
    aggressive = AggressiveStrategy()
    defensive = DefensiveStrategy()

    print("Tournament 0 (basic)")
    print(" [ (Flameling+Normal), (Healing+Defensive) ]")
    battle([(flame, normal), (healing, defensive)])

    print()
    print("Tournament 1 (error)")
    print(" [ (Flameling+Aggressive), (Healing+Defensive) ]")
    battle([(flame, aggressive), (healing, defensive)])

    print()
    print("Tournament 2 (multiple)")
    print(" [ (Aquabub+Normal), (Healing+Defensive), "
          "(Transform+Aggressive) ]")
    battle([(aqua, normal), (healing, defensive), (transform, aggressive)])


if __name__ == "__main__":
    main()
```

O que os arquivos usam, todos autorizados: `abc` (`ABC` e `abstractmethod`), a classe embutida
`Exception`, as funções embutidas `isinstance`, `len`, `range` e `print`, o método de lista
`append`, e os imports do próprio projeto (`ex0`, `ex0.creature`, `ex1`, `ex1.capability`,
`ex2` e o relativo `.strategy`).
