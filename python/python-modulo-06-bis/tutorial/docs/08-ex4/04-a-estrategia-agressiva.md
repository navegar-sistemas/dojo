---
sidebar_position: 4
title: A estratégia agressiva
---

# A estratégia agressiva

A estratégia que leva em conta uma capacidade só serve para as criaturas que sabem se transformar.
Com elas, faz a sequência completa: transforma, ataca e volta ao normal.

Crie o arquivo `ex4/aggressive.py`:

```python title="ex4/aggressive.py"
from ex3.capability import TransformCapability
from ex3.creature import Creature

from .strategy import BattleStrategy, StrategyError


class AggressiveStrategy(BattleStrategy):
    name = "Aggressive"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> None:
        if not isinstance(creature, TransformCapability):
            raise StrategyError(f"Invalid Creature '{creature.name}' "
                                "for this aggressive strategy")
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())
```

## is_valid confere a capacidade

`isinstance(creature, TransformCapability)` pergunta se a criatura tem a capacidade, e não de que
família ela é. É a regra do enunciado: a estratégia confere capacidades, nunca a família concreta.
Uma família nova que herde de `TransformCapability` serve para esta estratégia sem nenhuma mudança
aqui.

## act

- se a criatura não tem a capacidade, `act` lança `StrategyError` com a mensagem do enunciado:
  `Invalid Creature 'Flameling' for this aggressive strategy`;
- se tem, imprime as três frases, na ordem `transform`, `attack`, `revert`. O `attack` do meio
  já sai com a frase do golpe forte, porque a criatura está transformada
  ([A família que se transforma](../07-ex3/05-a-familia-que-se-transforma.md)), e o `revert`
  devolve a criatura ao estado normal para a próxima luta.

## Por que act repete o isinstance

`act` poderia conferir a criatura chamando `self.is_valid(creature)`, como a estratégia normal.
Aqui, isso não passa no mypy. Com esta versão do `act`:

```python
    def act(self, creature: Creature) -> None:
        if not self.is_valid(creature):
            raise StrategyError(f"Invalid Creature '{creature.name}' "
                                "for this aggressive strategy")
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())
```

o comando `.venv/bin/mypy --disallow-untyped-defs ex4` acusa:

```text
ex4/aggressive.py:17: error: "Creature" has no attribute "transform"  [attr-defined]
ex4/aggressive.py:19: error: "Creature" has no attribute "revert"  [attr-defined]
Found 2 errors in 1 file (checked 4 source files)
```

O mypy estreita o tipo de uma variável só quando vê o `isinstance` escrito na própria função
([isinstance e o mypy](../06-pacotes/02-heranca-multipla.md#isinstance-e-o-mypy)). Para ele,
`self.is_valid(creature)` é uma chamada qualquer que devolve um `bool`, e `creature` continua um
`Creature`, sem `transform` nem `revert`. Com o `isinstance` no próprio `act`, depois do `raise`
o mypy sabe que a criatura também é um `TransformCapability`.

O resultado é a mesma conferência escrita em dois lugares, `is_valid` e `act`; é o preço de passar
no mypy sem forçar o tipo à mão.
