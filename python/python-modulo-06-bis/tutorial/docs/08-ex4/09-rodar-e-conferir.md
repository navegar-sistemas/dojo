---
sidebar_position: 9
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 tournament.py) - <<'FIM'
Tournament 0 (basic)
 [ (Flameling+Normal), (Shiftling+Aggressive) ]
*** Tournament ***
2 opponents involved

* Battle *
Flameling is a Fire type Creature
 vs.
Shiftling is a Normal type Creature
 now fight!
Flameling uses Ember!
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.

Tournament 1 (error)
 [ (Shiftling+Aggressive), (Flameling+Aggressive) ]
*** Tournament ***
2 opponents involved

* Battle *
Shiftling is a Normal type Creature
 vs.
Flameling is a Fire type Creature
 now fight!
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.
Battle error, aborting tournament: Invalid Creature 'Flameling' for this aggressive strategy
FIM
```

Sem nenhuma linha impressa, a saída é a esperada. Rodar o torneio cria as pastas de cache
`ex3/__pycache__` e `ex4/__pycache__`, que não são entregues.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex4 tournament.py
.venv/bin/mypy --disallow-untyped-defs ex4 tournament.py
```

```text
Success: no issues found in 5 source files
```

O mypy confere os cinco arquivos do exercício e segue os imports até o `ex3`.

## Quem serve para cada estratégia

```bash
python3 -B -c 'from ex3 import FlameFactory, TransformCreatureFactory
from ex4 import AggressiveStrategy, NormalStrategy
flameling = FlameFactory().create_base()
shiftling = TransformCreatureFactory().create_base()
for strategy in (NormalStrategy(), AggressiveStrategy()):
    print(strategy.name, strategy.is_valid(flameling), strategy.is_valid(shiftling))'
```

```text
Normal True True
Aggressive False True
```

A estratégia normal aceita as duas criaturas; a agressiva, só a que tem a capacidade.

## A exceção dedicada

Chamado direto, sem o `try` do torneio, o `act` da estratégia agressiva com um `Flameling` para o
programa:

```bash
python3 -B -c 'from ex3 import FlameFactory
from ex4 import AggressiveStrategy
AggressiveStrategy().act(FlameFactory().create_base())'
```

A última linha da saída é:

```text
ex4.strategy.StrategyError: Invalid Creature 'Flameling' for this aggressive strategy
```

O traceback mostra o tipo da exceção com o módulo onde ela foi definida, `ex4.strategy`, e a
mensagem.

## A estratégia abstrata não é instanciada

```bash
python3 -B -c 'from ex4 import BattleStrategy; BattleStrategy()'
```

A última linha da saída é:

```text
TypeError: Can't instantiate abstract class BattleStrategy without an implementation for abstract methods 'act', 'is_valid'
```

No Python 3.10 e no 3.11, a mensagem é
`Can't instantiate abstract class BattleStrategy with abstract methods act, is_valid`.

## Três oponentes

Com três oponentes, cada um enfrenta os outros dois. O terceiro dá a estratégia agressiva a um
`Flameling`:

```bash
python3 -B -c 'from ex3 import FlameFactory, TransformCreatureFactory
from ex4 import AggressiveStrategy, NormalStrategy
from tournament import battle
battle([(FlameFactory(), NormalStrategy()),
        (TransformCreatureFactory(), AggressiveStrategy()),
        (FlameFactory(), AggressiveStrategy())])'
```

```text
*** Tournament ***
3 opponents involved

* Battle *
Flameling is a Fire type Creature
 vs.
Shiftling is a Normal type Creature
 now fight!
Flameling uses Ember!
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.

* Battle *
Flameling is a Fire type Creature
 vs.
Flameling is a Fire type Creature
 now fight!
Flameling uses Ember!
Battle error, aborting tournament: Invalid Creature 'Flameling' for this aggressive strategy
```

- a primeira batalha (oponente 0 contra 1) termina normalmente;
- na segunda (0 contra 2), o primeiro `Flameling` ataca, e o segundo, com a estratégia agressiva,
  levanta a `StrategyError`;
- a terceira batalha (1 contra 2) não acontece: o torneio abortou.
