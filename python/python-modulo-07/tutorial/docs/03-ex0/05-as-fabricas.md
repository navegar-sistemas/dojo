---
sidebar_position: 5
title: As fábricas
---

# As fábricas

As fábricas ficam num arquivo próprio, `ex0/factory.py`. Elas precisam das criaturas, que estão
em `ex0/creature.py`, no mesmo pacote. Crie o arquivo:

```python
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

## O import

`from .creature import ...` é um import relativo: o módulo `creature` deste mesmo pacote
([Módulos e pacotes](../02-conceitos/01-modulos-e-pacotes.md#o-experimento)). Os nomes vêm em
ordem alfabética, um costume que facilita achar um nome numa lista longa. A linha em branco
separa os imports da biblioteca do Python (`abc`) dos imports do próprio projeto, outro costume
de estilo.

## A fábrica abstrata

`CreatureFactory` herda de `ABC` e tem os dois métodos abstratos que o enunciado pede. Ela não
tem `__init__`: uma fábrica não guarda nada, só cria.

O tipo de retorno dos dois métodos é `Creature`, a classe abstrata. É a promessa que toda fábrica
faz: "devolvo uma criatura", sem dizer qual.

## As fábricas concretas

Cada fábrica concreta escreve os dois métodos com as criaturas da sua família. `Flameling()` cria
uma criatura nova a cada chamada: duas chamadas a `create_base` devolvem dois objetos
diferentes, cada um com os seus atributos.

As fábricas concretas também declaram `-> Creature`, e não `-> Flameling`. Assim, quem usa a
fábrica continua vendo só o tipo abstrato, e o nome da classe concreta não aparece nem nos type
hints que o mypy mostra a quem usa o pacote.
