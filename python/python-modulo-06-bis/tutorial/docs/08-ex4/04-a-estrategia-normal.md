---
sidebar_position: 4
title: A estratégia normal
---

# A estratégia normal

A estratégia simples serve para qualquer criatura e só faz a criatura atacar.

Crie o arquivo `ex4/normal.py`:

```python title="ex4/normal.py"
from ex3.creature import Creature

from .strategy import BattleStrategy, StrategyError


class NormalStrategy(BattleStrategy):
    name = "Normal"

    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise StrategyError(f"Invalid Creature '{creature.name}' "
                                "for this normal strategy")
        print(creature.attack())
```

- `from .strategy import ...` é um import relativo, do módulo `strategy` deste pacote;
- `name = "Normal"` dá o valor do atributo anotado em `BattleStrategy`;
- `is_valid` devolve `True` para qualquer criatura: toda criatura sabe atacar, porque `attack` é
  um método de `Creature`. O parâmetro `creature` não é usado, mas precisa existir: a assinatura é
  a da mãe;
- `act` confere a criatura com `is_valid` antes de agir, e só então imprime o ataque.

Com o `is_valid` desta classe, o `raise` nunca acontece. Ele está ali para que `act` siga a mesma
regra em toda estratégia ("confere antes de agir; se não serve, `StrategyError`"), como o
enunciado pede para o `act`. Se um dia esta estratégia passar a recusar alguma criatura, basta
mudar `is_valid`.

A mensagem do erro foi dividida em dois textos seguidos para caber nos 79 caracteres; o Python os
junta num só ([Processar o fluxo](../04-ex1/03-registrar-e-rotear.md#processar-o-fluxo)).
