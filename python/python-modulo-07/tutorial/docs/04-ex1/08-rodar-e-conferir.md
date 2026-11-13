---
sidebar_position: 8
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 capacitor.py) - <<'FIM'
Testing Creature with healing capability
 base:
Sproutling is a Grass type Creature
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount
 evolved:
Bloomelle is a Grass/Fairy type Creature
Bloomelle uses Petal Dance!
Bloomelle heals itself and others for a large amount

Testing Creature with transform capability
 base:
Shiftling is a Normal type Creature
Shiftling attacks normally.
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.
 evolved:
Morphagon is a Normal/Dragon type Creature
Morphagon attacks normally.
Morphagon morphs into a dragonic battle form!
Morphagon unleashes a devastating morph strike!
Morphagon stabilizes its form.
FIM
```

Sem nenhuma linha impressa, a saída é a esperada.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 capacitor.py ex1
.venv/bin/mypy --disallow-untyped-defs capacitor.py ex1
```

```text
Success: no issues found in 5 source files
```

O mypy confere `capacitor.py` e os quatro arquivos do `ex1`; os do `ex0`, que eles importam, ele
lê para conhecer os tipos.

## O pacote só expõe fábricas

```bash
python3 -B -c 'import ex1; print(ex1.__all__)'
```

```text
['HealingCreatureFactory', 'TransformCreatureFactory']
```

## A capacidade é uma mãe à parte

```bash
python3 -B -c 'from ex1 import HealingCreatureFactory
creature = HealingCreatureFactory().create_base()
print(type(creature).__mro__)'
```

```text
(<class 'ex1.creature.Sproutling'>, <class 'ex0.creature.Creature'>, <class 'ex1.capability.HealCapability'>, <class 'abc.ABC'>, <class 'object'>)
```

O código entre as aspas simples pode ocupar várias linhas: o terminal só roda o comando quando a
aspa final fecha. `type(creature)` é a classe do objeto, e a `__mro__` dela mostra a ordem de
busca: `Sproutling`, depois `Creature` (do módulo `ex0.creature`) e, à parte, `HealCapability`
(do `ex1.capability`). A capacidade não está entre os ancestrais de `Creature`: ela é uma segunda
mãe, como o enunciado pede.

## O estado é de cada criatura

```bash
python3 -B -c 'from ex1 import TransformCreatureFactory
factory = TransformCreatureFactory()
first = factory.create_base()
second = factory.create_base()
print(first.transform())
print(first.attack())
print(second.attack())'
```

```text
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling attacks normally.
```

Os dois `Shiftling` vêm da mesma fábrica, mas são objetos diferentes: só o primeiro se
transformou, e só ele ataca com o golpe reforçado. Este comando roda só o Python (`python3 -c`), e o Python
não confere tipos; para o mypy, `first.transform()` precisaria do `isinstance` do
`capacitor.py`.

## Um arquivo do pacote não roda sozinho

```bash
python3 ex1/factory.py
```

A última linha da saída é:

```text
ModuleNotFoundError: No module named 'ex0'
```

Rodado direto, o arquivo põe a pasta `ex1/` na lista de busca, e não a raiz: o `ex0` não é
encontrado ([Onde o Python procura](../02-conceitos/01-modulos-e-pacotes.md#onde-o-python-procura)).
Os pacotes são sempre usados a partir dos programas da raiz.
