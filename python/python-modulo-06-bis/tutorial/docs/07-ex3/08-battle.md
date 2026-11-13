---
sidebar_position: 8
title: battle.py
---

# battle.py

O primeiro script de teste usa só as fábricas: pede criaturas, descreve, ataca e põe duas para
lutar. Ele não importa nenhuma criatura concreta, e mesmo assim imprime as frases de cada uma.

Crie o arquivo `battle.py`, na raiz do projeto, ao lado da pasta `ex3`:

```python title="battle.py"
from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    print("Testing factory")
    for creature in (factory.create_base(), factory.create_evolved()):
        print(creature.describe())
        print(creature.attack())


def test_battle(first: CreatureFactory, second: CreatureFactory) -> None:
    print("Testing battle")
    left = first.create_base()
    right = second.create_base()
    print(left.describe())
    print(" vs.")
    print(right.describe())
    print(" fight!")
    print(left.attack())
    print(right.attack())


def main() -> None:
    flame = FlameFactory()
    transform = TransformCreatureFactory()
    test_factory(flame)
    print()
    test_factory(transform)
    print()
    test_battle(flame, transform)


if __name__ == "__main__":
    main()
```

## test_factory

É a **única** função que o enunciado pede para testar uma fábrica: recebe uma fábrica qualquer,
cria a criatura base e depois a evoluída e, com cada uma, descreve e ataca.

- `(factory.create_base(), factory.create_evolved())` é uma tupla com as duas criaturas, criadas
  nessa ordem; o `for` percorre a tupla, primeiro a base, depois a evoluída;
- `creature.describe()` e `creature.attack()` devolvem textos, e o `print` os imprime. O
  `describe` é o de `Creature`; o `attack` é o da classe de cada criatura;
- o parâmetro é um `CreatureFactory`: a função funciona igual com `FlameFactory()` e com
  `TransformCreatureFactory()`, sem nenhum `if` sobre a família.

## test_battle

A segunda função recebe duas fábricas, cria a criatura base de cada uma e as põe frente a frente:
descreve a primeira, imprime ` vs.`, descreve a segunda, imprime ` fight!` e faz as duas
atacarem, nessa ordem. ` vs.` e ` fight!` começam com um espaço, como no enunciado.

## O main

O `main` cria as duas fábricas uma vez e as usa nos três testes. Os `print()` sem argumento
imprimem as linhas vazias entre os blocos.

Nesse cenário, o `Shiftling` ataca sem se transformar (`Shiftling attacks normally.`): aqui
ninguém chama `transform`. Quem testa a transformação é o
[capacitor.py](./09-capacitor.md).
