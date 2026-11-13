---
sidebar_position: 8
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 tournament.py) - <<'FIM'
Tournament 0 (basic)
 [ (Flameling+Normal), (Healing+Defensive) ]
*** Tournament ***
2 opponents involved

* Battle *
Flameling is a Fire type Creature
 vs.
Sproutling is a Grass type Creature
 now fight!
Flameling uses Ember!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount

Tournament 1 (error)
 [ (Flameling+Aggressive), (Healing+Defensive) ]
*** Tournament ***
2 opponents involved

* Battle *
Flameling is a Fire type Creature
 vs.
Sproutling is a Grass type Creature
 now fight!
Battle error, aborting tournament: Invalid Creature 'Flameling' for this aggressive strategy

Tournament 2 (multiple)
 [ (Aquabub+Normal), (Healing+Defensive), (Transform+Aggressive) ]
*** Tournament ***
3 opponents involved

* Battle *
Aquabub is a Water type Creature
 vs.
Sproutling is a Grass type Creature
 now fight!
Aquabub uses Water Gun!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount

* Battle *
Aquabub is a Water type Creature
 vs.
Shiftling is a Normal type Creature
 now fight!
Aquabub uses Water Gun!
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.

* Battle *
Sproutling is a Grass type Creature
 vs.
Shiftling is a Normal type Creature
 now fight!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.
FIM
```

Sem nenhuma linha impressa, a saída é a esperada.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 tournament.py ex2
.venv/bin/mypy --disallow-untyped-defs tournament.py ex2
```

```text
Success: no issues found in 3 source files
```

## is_valid com cada combinação

O torneio não usa `is_valid`, mas ele faz parte da estratégia. Este teste pergunta a cada
estratégia se ela serve para a criatura base de três famílias:

```bash
python3 -B -c 'from ex0 import FlameFactory
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex2 import AggressiveStrategy, DefensiveStrategy, NormalStrategy
strategies = [NormalStrategy(), AggressiveStrategy(), DefensiveStrategy()]
for factory in [FlameFactory(), HealingCreatureFactory(), TransformCreatureFactory()]:
    creature = factory.create_base()
    for strategy in strategies:
        print(creature.name, type(strategy).__name__, strategy.is_valid(creature))'
```

```text
Flameling NormalStrategy True
Flameling AggressiveStrategy False
Flameling DefensiveStrategy False
Sproutling NormalStrategy True
Sproutling AggressiveStrategy False
Sproutling DefensiveStrategy True
Shiftling NormalStrategy True
Shiftling AggressiveStrategy True
Shiftling DefensiveStrategy False
```

`type(strategy).__name__` é o nome da classe do objeto. A normal serve para todas; a agressiva,
só para quem se transforma; a defensiva, só para quem cura.

## A exceção dedicada

```bash
python3 -B -c 'from ex0 import FlameFactory
from ex2 import DefensiveStrategy
DefensiveStrategy().act(FlameFactory().create_base())'
```

A última linha da saída é:

```text
ex2.strategy.InvalidStrategyError: Invalid Creature 'Flameling' for this defensive strategy
```

Sem o `try` do torneio, a exceção chega ao fim do programa e aparece no traceback com o nome
completo da classe, `ex2.strategy.InvalidStrategyError` (o módulo onde ela foi definida e o nome
dela), e a mensagem clara que o enunciado pede.

## Quando o inválido é o segundo oponente

```bash
python3 -B -c 'from ex0 import FlameFactory
from ex1 import HealingCreatureFactory
from ex2 import AggressiveStrategy, DefensiveStrategy
from tournament import battle
battle([(HealingCreatureFactory(), DefensiveStrategy()), (FlameFactory(), AggressiveStrategy())])'
```

```text
*** Tournament ***
2 opponents involved

* Battle *
Sproutling is a Grass type Creature
 vs.
Flameling is a Fire type Creature
 now fight!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount
Battle error, aborting tournament: Invalid Creature 'Flameling' for this aggressive strategy
```

`from tournament import battle` importa a função sem rodar o `main`, graças ao
`if __name__ == "__main__":`. O primeiro oponente age normalmente; o erro aparece quando chega a
vez do segundo, e o torneio é abortado nesse ponto.
