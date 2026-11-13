---
sidebar_position: 3
title: As criaturas que curam
---

# As criaturas que curam

`Sproutling` e `Bloomelle` formam a família que cura: são criaturas (atacam e se descrevem) e
têm a capacidade de curar. Elas ficam em `ex1/creature.py`, com as criaturas que se transformam
da [próxima página](./04-as-criaturas-que-se-transformam.md).

Crie o arquivo com os imports e as duas classes:

```python
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
```

## Os dois imports

- `from ex0.creature import Creature` usa o nome completo: `Creature` está em **outro** pacote,
  o `ex0`. O import funciona porque os programas rodam da raiz, onde está a pasta `ex0/`
  ([No projeto](../02-conceitos/01-modulos-e-pacotes.md#no-projeto)). `Creature` vem do módulo,
  e não do pacote `ex0`, porque o pacote só expõe fábricas
  ([O que fica de fora](../03-ex0/06-o-init-do-pacote.md#o-que-fica-de-fora));
- `from .capability import ...` é relativo: o módulo `capability` deste pacote, o `ex1`.
  `TransformCapability` já entra no import porque a próxima página a usa;
- a linha em branco separa os imports de outro pacote do import do próprio pacote.

É assim que o exercício 1 "constrói sobre o `ex0`", como o enunciado pede: não copia a classe
`Creature`, importa a mesma.

## Duas mães, um construtor

`class Sproutling(Creature, HealCapability)` herda das duas classes. A ordem de busca
([A ordem de busca](../02-conceitos/03-heranca-multipla.md#a-ordem-de-busca)) é `Sproutling`,
`Creature`, `HealCapability`, `ABC`, `object`. `super().__init__("Sproutling", "Grass")` chega ao
`__init__` de `Creature`, a próxima classe da ordem, que guarda o nome e o tipo. Como
`HealCapability` não tem `__init__` próprio, não falta nada para criar.

## Os três métodos

Cada criatura escreve os métodos abstratos das duas mães: `attack`, de `Creature`, e `heal`, de
`HealCapability`. Os textos são os da saída do enunciado. `describe` vem pronto de `Creature`.
