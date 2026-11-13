---
sidebar_position: 11
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

O mesmo `diff` do [exercício 0](../03-ex0/09-rodar-e-conferir.md#comparar-com-o-enunciado), um
para cada script:

```bash
diff <(python3 battle.py) - <<'FIM'
Testing factory
Flameling is a Fire type Creature
Flameling uses Ember!
Pyrodon is a Fire/Flying type Creature
Pyrodon uses Flamethrower!

Testing factory
Shiftling is a Normal type Creature
Shiftling attacks normally.
Morphagon is a Normal/Dragon type Creature
Morphagon attacks normally.

Testing battle
Flameling is a Fire type Creature
 vs.
Shiftling is a Normal type Creature
 fight!
Flameling uses Ember!
Shiftling attacks normally.
FIM
```

```bash
diff <(python3 capacitor.py) - <<'FIM'
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

Sem nenhuma linha impressa, as duas saídas são as esperadas, inclusive o espaço no começo de
` vs.`, ` fight!`, ` base:` e ` evolved:`.

Rodar os scripts cria a pasta `ex3/__pycache__`, o cache dos módulos do pacote que foram
importados. Ela não faz parte da entrega ([Entregar](../09-fechamento/02-entregar.md)).

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex3 battle.py capacitor.py
.venv/bin/mypy --disallow-untyped-defs ex3 battle.py capacitor.py
```

```text
Success: no issues found in 8 source files
```

O flake8 recebe a pasta `ex3` e os dois scripts, e não imprime nada. O mypy confere os oito
arquivos.

## O pacote só expõe as fábricas

Os testes desta página usam `python3 -B -c`, como no
[exercício 0](../03-ex0/09-rodar-e-conferir.md#a-classe-abstrata-não-é-instanciada): o código
entre aspas roda a partir da pasta do projeto, onde o Python acha o pacote `ex3`.

```bash
python3 -B -c 'import ex3; print(ex3.__all__); print(hasattr(ex3, "Flameling"))'
```

```text
['CreatureFactory', 'FlameFactory', 'TransformCreatureFactory']
False
```

O pacote oferece as três fábricas, e o `Flameling` não está entre os nomes dele.

## As classes abstratas não são instanciadas

```bash
python3 -B -c 'from ex3 import CreatureFactory; CreatureFactory()'
```

A última linha da saída é:

```text
TypeError: Can't instantiate abstract class CreatureFactory without an implementation for abstract methods 'create_base', 'create_evolved'
```

No Python 3.10 e no 3.11, a mensagem é
`Can't instantiate abstract class CreatureFactory with abstract methods create_base, create_evolved`.
O mesmo vale para `Creature` e `TransformCapability`.

## A capacidade não é uma criatura

```bash
python3 -B -c 'from ex3.capability import TransformCapability
from ex3.creature import Creature
from ex3 import FlameFactory, TransformCreatureFactory
print(issubclass(TransformCapability, Creature))
print(isinstance(FlameFactory().create_base(), TransformCapability))
print(isinstance(TransformCreatureFactory().create_base(), TransformCapability))'
```

```text
False
False
True
```

- `issubclass(A, B)`, função embutida, responde se a classe `A` descende da classe `B`:
  `TransformCapability` não descende de `Creature`, como o enunciado exige;
- o `Flameling` não tem a capacidade; o `Shiftling` tem.

## Uma criatura comum no capacitor

A função `test_transform` recebe qualquer criatura. Com um `Flameling`, ela descreve, ataca e avisa
que não há transformação:

```bash
python3 -B -c 'from ex3 import FlameFactory
from capacitor import test_transform
test_transform(FlameFactory().create_base())'
```

```text
Flameling is a Fire type Creature
Flameling uses Ember!
Flameling has no transform capability
```

O `import` de `capacitor` não roda o `main` dele: o `if __name__ == "__main__":` só deixa o `main`
rodar quando o arquivo é executado com `python3 capacitor.py`.

## Cada chamada cria uma criatura nova

```bash
python3 -B -c 'from ex3 import TransformCreatureFactory
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

Os dois `Shiftling` são objetos diferentes, cada um com o seu `transformed`: transformar o
primeiro não muda o segundo.

## Um arquivo do pacote não roda sozinho

```bash
python3 ex3/factory.py
```

A última linha da saída é:

```text
ImportError: attempted relative import with no known parent package
```

Os módulos do pacote são importados pelos scripts da raiz; rodados direto, os imports relativos não
têm pacote para onde apontar ([O pacote](../06-pacotes/01-o-pacote.md#um-módulo-do-pacote-não-roda-sozinho)).
