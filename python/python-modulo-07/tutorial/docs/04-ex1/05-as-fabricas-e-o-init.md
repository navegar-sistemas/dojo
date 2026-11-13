---
sidebar_position: 5
title: As fábricas e o __init__.py
---

# As fábricas e o `__init__.py`

As duas famílias novas precisam de fábricas, no mesmo formato da `FlameFactory` e da
`AquaFactory` ([As fábricas](../03-ex0/05-as-fabricas.md)). Crie `ex1/factory.py`:

```python
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

- `CreatureFactory` vem do pacote `ex0`, que a expõe; `Creature`, do módulo `ex0.creature`, para
  o type hint de retorno;
- as quatro criaturas vêm do módulo vizinho, com import relativo;
- cada fábrica cria a base e a evoluída da sua família, como pede o enunciado.

As fábricas novas são filhas da **mesma** `CreatureFactory` do exercício 0. Por isso, toda função
escrita para uma `CreatureFactory`, como o `test_factory` do `battle.py`, já funciona com elas.

## O `__init__.py`

Como o `ex0`, o pacote `ex1` expõe só as fábricas. Crie `ex1/__init__.py`:

```python
from .factory import HealingCreatureFactory, TransformCreatureFactory

__all__ = ["HealingCreatureFactory", "TransformCreatureFactory"]
```

As capacidades também ficam de fora: o enunciado manda o pacote expor somente fábricas. Quem
precisa delas, como o `capacitor.py` da [próxima página](./06-o-script-capacitor.md), as importa
do módulo `ex1.capability`.
