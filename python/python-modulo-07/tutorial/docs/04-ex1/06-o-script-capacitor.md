---
sidebar_position: 6
title: O script capacitor
---

# O script capacitor

O `capacitor.py`, na raiz, testa as duas famílias novas. As fábricas devolvem `Creature`, e
`Creature` não tem `heal` nem `transform`: antes de usar uma capacidade, o script confere com
`isinstance` que a criatura a tem
([isinstance e o mypy](../02-conceitos/04-isinstance-e-o-mypy.md)).

Crie `capacitor.py` na pasta `datadeck`, com os imports:

```python
from ex0.creature import Creature
from ex1 import HealingCreatureFactory, TransformCreatureFactory
from ex1.capability import HealCapability, TransformCapability
```

- `Creature`, para o type hint das funções de teste;
- as duas fábricas, do pacote `ex1`;
- as duas capacidades, do módulo `ex1.capability`, para o `isinstance`.

## Os testes de cada capacidade

Acrescente abaixo dos imports, com duas linhas em branco antes de cada `def`:

```python
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
```

- `test_healing` segue os três passos do enunciado: descrever, atacar e curar;
- `test_transform` segue os cinco: descrever, atacar, transformar, atacar de novo e voltar. O
  segundo `attack` sai diferente do primeiro porque o `transform` mudou o estado do objeto;
- dentro de cada `if isinstance(...)`, o mypy sabe que a criatura também é uma
  `HealCapability` (ou uma `TransformCapability`) e aceita a chamada a `heal` (ou a `transform` e
  `revert`). Sem o `if`, ele acusaria `"Creature" has no attribute "heal"`.

As duas funções recebem a criatura, e não a fábrica, porque o enunciado testa a base e a evoluída
separadamente, com as linhas ` base:` e ` evolved:` entre elas.

## O main

Por fim, no fim do arquivo, com duas linhas em branco antes de cada `def` e antes do `if`:

```python
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

A ordem segue o cenário do enunciado: a fábrica que cura, a base, a evoluída; uma linha vazia;
a fábrica que transforma, a base, a evoluída. Cada criatura é criada na hora em que é testada.
