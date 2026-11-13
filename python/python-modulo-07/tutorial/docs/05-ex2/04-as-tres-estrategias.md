---
sidebar_position: 4
title: As três estratégias
---

# As três estratégias

Acrescente ao fim de `ex2/strategy.py`, depois da exceção, a classe abstrata e as três
estratégias, com duas linhas em branco antes de cada `class`.

## A estratégia abstrata

```python
class BattleStrategy(ABC):
    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> list[str]:
        pass
```

Os dois métodos abstratos do enunciado. Os dois recebem uma `Creature`; `is_valid` devolve
`bool`, e `act` devolve a lista com o texto de cada ação
([O que `act` devolve](./02-o-padrao-estrategia.md#o-que-act-devolve)).

## A estratégia normal

```python
class NormalStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        return [creature.attack()]
```

Serve para qualquer criatura: `is_valid` devolve sempre `True`, e `act` só ataca. Toda
`Creature` tem `attack`, então não há o que conferir. O parâmetro `creature` de `is_valid` não é
usado, mas fica: a assinatura (nome, parâmetros e retorno) precisa ser a mesma da
classe abstrata.

## A estratégia agressiva

```python
class AggressiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, TransformCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, TransformCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this aggressive strategy")
        return [creature.transform(), creature.attack(), creature.revert()]
```

- `is_valid`: a criatura serve se tem a capacidade de se transformar;
- `act` confere de novo e, se a criatura não serve, lança a exceção dedicada com a mensagem do
  enunciado. A mensagem foi dividida em dois textos seguidos, para caber nos 79 caracteres: o
  Python junta textos escritos lado a lado num só (`"ab" "cd"` é `"abcd"`), e só o primeiro
  precisa do `f`, porque só ele tem um valor entre chaves;
- depois do `if`, o mypy sabe que a criatura é também uma `TransformCapability`
  ([isinstance e o mypy](../02-conceitos/04-isinstance-e-o-mypy.md#isinstance-direto-no-if)), e
  aceita `transform` e `revert`. A lista tem as três ações na ordem do enunciado: transformar,
  atacar (já com o golpe reforçado) e voltar ao normal.

## Por que `act` não chama `is_valid`

Escrever `if not self.is_valid(creature): raise ...` daria o mesmo resultado ao rodar, mas o mypy
recusaria o `creature.transform()` logo abaixo: para ele, `is_valid` devolve um `bool` qualquer,
e a criatura continua sendo só uma `Creature`
([Uma função que confere não basta](../02-conceitos/04-isinstance-e-o-mypy.md#uma-função-que-confere-não-basta)).
Por isso `act` repete o `isinstance`. As duas conferências dizem a mesma coisa: `is_valid` é a
pergunta, para quem quer saber antes; o `if` de `act` é a proteção, para quem não perguntou.

## A estratégia defensiva

```python
class DefensiveStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> list[str]:
        if not isinstance(creature, HealCapability):
            raise InvalidStrategyError(
                f"Invalid Creature '{creature.name}' "
                "for this defensive strategy")
        return [creature.attack(), creature.heal()]
```

O mesmo desenho da agressiva, com a capacidade de curar: ataca e depois cura. A mensagem de erro
é escolha do tutorial, por analogia com a da agressiva (o enunciado só mostra esta), com
`defensive`.

## O `__init__.py`

O pacote `ex2` não tem restrição sobre o que expõe, e o `tournament.py` precisa das estratégias e
da exceção. Crie `ex2/__init__.py`:

```python
from .strategy import (
    AggressiveStrategy,
    BattleStrategy,
    DefensiveStrategy,
    InvalidStrategyError,
    NormalStrategy,
)

__all__ = [
    "BattleStrategy",
    "NormalStrategy",
    "AggressiveStrategy",
    "DefensiveStrategy",
    "InvalidStrategyError",
]
```

Com cinco nomes, o import não cabe numa linha de 79 caracteres. Entre parênteses, o Python
aceita um nome por linha, e a vírgula depois do último é permitida. A lista `__all__` usa a mesma
quebra.
