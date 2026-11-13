---
sidebar_position: 3
title: A estratégia abstrata
---

# A estratégia abstrata

Toda estratégia responde a duas perguntas do torneio: "esta criatura serve para você?" e "faça a
criatura agir". `BattleStrategy` declara as duas, e o mesmo módulo define o erro que uma
estratégia lança quando recebe uma criatura que não serve.

Crie o arquivo `ex4/strategy.py`:

```python title="ex4/strategy.py"
from abc import ABC, abstractmethod

from ex3.creature import Creature


class StrategyError(Exception):
    pass


class BattleStrategy(ABC):
    name: str

    @abstractmethod
    def is_valid(self, creature: Creature) -> bool:
        pass

    @abstractmethod
    def act(self, creature: Creature) -> None:
        pass
```

## O import de outro pacote

`from ex3.creature import Creature` não tem ponto: o módulo vem de **outro** pacote, o `ex3`, e
não deste. É o import entre os dois exercícios de que o enunciado fala. `Creature` vem do módulo
`ex3.creature`, e não da porta do pacote, porque o `ex3` só expõe as fábricas
([E as classes abstratas?](../07-ex3/07-a-porta-do-pacote.md#e-as-classes-abstratas)).

## Uma exceção do projeto

O enunciado pede uma **exceção dedicada**: um tipo de erro só para "criatura inválida para esta
estratégia". Um tipo novo de exceção é uma classe filha de `Exception`, a classe mãe das exceções
comuns do Python, como `ValueError` e `TypeError`:

- `class StrategyError(Exception): pass` cria o tipo. O corpo vazio (`pass`) basta: a mensagem e
  todo o resto vêm de `Exception`;
- `raise StrategyError("mensagem")` lança a exceção com a mensagem
  ([Exceções, em resumo](../00-introducao/03-pre-requisitos.md#exceções-em-resumo));
- `except StrategyError` captura **só** esse tipo. O torneio usa isso para abortar diante de uma
  criatura inválida sem esconder outros erros: um `TypeError` vindo de um defeito no código
  continua aparecendo como traceback.

O nome `StrategyError` é escolha do tutorial; o enunciado só pede que a exceção seja dedicada e
tenha uma mensagem clara.

## A classe abstrata

- `is_valid(self, creature: Creature) -> bool` responde se a criatura serve para a estratégia;
- `act(self, creature: Creature) -> None` faz a criatura agir. Cada estratégia imprime as frases
  da criatura (escolha do tutorial: a estratégia sabe quantas ações há e em que ordem, e o torneio
  só manda agir). Por isso o retorno é `None`;
- os dois recebem um `Creature`, a classe abstrata: a estratégia trabalha com qualquer criatura,
  de qualquer família.

## O nome da estratégia

`name: str`, no corpo da classe e sem valor, é uma **anotação de atributo de classe**: diz ao mypy
que toda estratégia tem um atributo `name` do tipo `str`, e deixa o valor para cada filha. O
torneio o usa para imprimir a lista de oponentes, como em `(Flameling+Normal)`. O enunciado não
pede esse atributo; ele é escolha do tutorial, no mesmo papel do `name` dos processadores do
exercício 1 ([Nome e contadores](../04-ex1/02-nome-e-contadores.md)).
