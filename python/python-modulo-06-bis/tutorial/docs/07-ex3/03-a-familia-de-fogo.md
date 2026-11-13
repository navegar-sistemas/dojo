---
sidebar_position: 3
title: A família do fogo
---

# A família do fogo

A primeira família tem duas criaturas comuns, sem habilidade especial: o `Flameling`, forma base,
e o `Pyrodon`, forma evoluída. Cada uma só precisa dizer o próprio nome, o próprio tipo e como
ataca.

Crie o arquivo `ex3/flame.py`:

```python title="ex3/flame.py"
from .creature import Creature


class Flameling(Creature):
    def __init__(self) -> None:
        super().__init__("Flameling", "Fire")

    def attack(self) -> str:
        return f"{self.name} uses Ember!"


class Pyrodon(Creature):
    def __init__(self) -> None:
        super().__init__("Pyrodon", "Fire/Flying")

    def attack(self) -> str:
        return f"{self.name} uses Flamethrower!"
```

- `from .creature import Creature` é um import relativo: o módulo `creature` deste mesmo pacote
  ([O pacote](../06-pacotes/01-o-pacote.md#o-experimento));
- o construtor de cada criatura não recebe nada e passa à mãe o nome e o tipo fixos, com
  `super().__init__` ([super(): o construtor da mãe](../06-pacotes/02-heranca-multipla.md#super-o-construtor-da-mãe)).
  Assim, `Flameling()` já cria a criatura completa;
- `attack` sobrescreve o método abstrato de `Creature` e devolve a frase da saída do enunciado,
  montada com o `name` guardado pela mãe.

As duas classes só têm o que as diferencia: nome, tipo e ataque. A frase de `describe` vem
pronta de `Creature`.
