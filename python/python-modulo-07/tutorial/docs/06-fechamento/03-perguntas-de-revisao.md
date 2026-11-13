---
sidebar_position: 3
title: Perguntas de revisão
---

# Perguntas de revisão

O enunciado recomenda entender os **padrões de projeto** do DataDeck, e não só o código que os
implementa. As perguntas abaixo revisam cada padrão: o problema, a solução e onde ela aparece no
projeto. Duas delas tratam de avisos dos exercícios: no 0, que outras criaturas podem ser
usadas, desde que os conceitos (famílias e fábricas abstratas) fiquem; no 1, que o exercício
precisa usar o conteúdo do pacote `ex0` e ser construído sobre ele.

## O que o padrão fábrica abstrata resolve?

**O problema:** o código que usa as criaturas não deveria depender das classes concretas delas,
e as criaturas de uma família deveriam vir sempre juntas.

**A solução:** uma classe abstrata de fábrica, `CreatureFactory`, declara o que toda fábrica sabe
criar (`create_base` e `create_evolved`). Cada família tem uma fábrica concreta
(`FlameFactory`, `AquaFactory`, `HealingCreatureFactory`, `TransformCreatureFactory`). Quem usa
recebe uma `CreatureFactory` e trabalha com `Creature`, as duas abstratas.

**No projeto:** o `test_factory` do `battle.py` é uma única função para todas as famílias, e o
`battle` do `tournament.py` recebe fábricas sem saber de que família. Os pacotes `ex0` e `ex1` só
expõem as fábricas, e as classes concretas ficam por trás delas
([O padrão fábrica abstrata](../03-ex0/02-o-padrao-fabrica-abstrata.md)).

## O que as capacidades resolvem?

**O problema:** algumas criaturas sabem fazer coisas a mais, e essas habilidades podem um dia
servir para outras coisas que não são criaturas.

**A solução:** cada habilidade é uma classe abstrata própria, que não herda de `Creature`
(`HealCapability`, `TransformCapability`). A criatura que tem a habilidade herda das duas classes:
de `Creature`, o que ela é; da capacidade, o que ela sabe fazer a mais. Uma classe assim, feita
para ser misturada a outra por herança múltipla, é chamada de mixin. A capacidade pode guardar
estado, como o `transformed`, que muda o `attack` da criatura.

**No projeto:** `isinstance(creature, HealCapability)` pergunta se uma criatura sabe curar, sem
conhecer a classe dela ([As capacidades](../04-ex1/02-as-capacidades.md)).

## O que o padrão estratégia resolve?

**O problema:** cada criatura luta de um jeito, e o código do torneio não deveria conhecer cada
capacidade nem a ordem das ações de cada uma.

**A solução:** o jeito de lutar fica num objeto, a estratégia. A classe abstrata `BattleStrategy`
declara `act` (agir) e `is_valid` (a criatura serve?); cada jeito de lutar é uma classe concreta.
O torneio só chama `strategy.act(creature)`. A estratégia que não serve para a criatura lança uma
exceção dedicada, e o torneio a trata.

**No projeto:** a mesma criatura pode lutar com estratégias diferentes, e uma estratégia nova não
muda o torneio ([O padrão estratégia](../05-ex2/02-o-padrao-estrategia.md)).

## O que os três padrões têm em comum?

Os três padrões separam **o que** se faz (a classe abstrata) de **como** se faz (as classes
concretas), e o resto do programa só conversa com a parte abstrata. É o polimorfismo
([Polimorfismo](../02-conceitos/02-classe-abstrata-e-super.md#polimorfismo)) aplicado em três
lugares: na criação das criaturas, nas habilidades delas e no jeito de lutar.

## Como acrescentar uma família nova?

O aviso do exercício 0 permite outras criaturas, mantendo famílias e fábricas abstratas. O
experimento abaixo cria uma família nova, a da pedra, e uma estratégia nova, a cautelosa, sem
mexer em nenhum arquivo dos exercícios. Crie `experimentos/extensao.py`:

```python title="experimentos/extensao.py"
from battle import test_factory
from ex0 import CreatureFactory, FlameFactory
from ex0.creature import Creature
from ex1 import HealingCreatureFactory
from ex2 import BattleStrategy, DefensiveStrategy, NormalStrategy
from tournament import battle


class Pebbling(Creature):
    def __init__(self) -> None:
        super().__init__("Pebbling", "Rock")

    def attack(self) -> str:
        return f"{self.name} uses Rock Throw!"


class Bouldron(Creature):
    def __init__(self) -> None:
        super().__init__("Bouldron", "Rock/Ground")

    def attack(self) -> str:
        return f"{self.name} uses Rock Slide!"


class RockFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Pebbling()

    def create_evolved(self) -> Creature:
        return Bouldron()


class CautiousStrategy(BattleStrategy):
    def is_valid(self, creature: Creature) -> bool:
        return True

    def act(self, creature: Creature) -> list[str]:
        return [f"{creature.name} waits and watches."]


test_factory(RockFactory())
print()
battle([
    (RockFactory(), NormalStrategy()),
    (FlameFactory(), CautiousStrategy()),
    (HealingCreatureFactory(), DefensiveStrategy()),
])
```

- `test_factory` vem do `battle.py`, e `battle`, do `tournament.py`: os dois programas podem ser
  importados sem rodar o `main`, graças ao `if __name__ == "__main__":`;
- a família da pedra são duas criaturas filhas de `Creature` e uma fábrica filha de
  `CreatureFactory`;
- a estratégia cautelosa serve para qualquer criatura e só observa.

O programa está em `experimentos/`, mas importa os pacotes da raiz. `PYTHONPATH=.` põe a pasta
atual (o `.`), a raiz, na lista de busca
([Onde o Python procura](../02-conceitos/01-modulos-e-pacotes.md#onde-o-python-procura)):

```bash
PYTHONPATH=. python3 -B experimentos/extensao.py
```

```text
Testing factory
Pebbling is a Rock type Creature
Pebbling uses Rock Throw!
Bouldron is a Rock/Ground type Creature
Bouldron uses Rock Slide!

*** Tournament ***
3 opponents involved

* Battle *
Pebbling is a Rock type Creature
 vs.
Flameling is a Fire type Creature
 now fight!
Pebbling uses Rock Throw!
Flameling waits and watches.

* Battle *
Pebbling is a Rock type Creature
 vs.
Sproutling is a Grass type Creature
 now fight!
Pebbling uses Rock Throw!
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount

* Battle *
Flameling is a Fire type Creature
 vs.
Sproutling is a Grass type Creature
 now fight!
Flameling waits and watches.
Sproutling uses Vine Whip!
Sproutling heals itself for a small amount
```

A função `test_factory` e a função `battle` trataram a família e a estratégia novas sem nenhuma
mudança. O mypy confere o experimento junto com os outros; rodado da raiz, ele acha os pacotes
na pasta atual:

```bash
.venv/bin/flake8 experimentos
.venv/bin/mypy --disallow-untyped-defs experimentos
```

```text
Success: no issues found in 8 source files
```

## Como o exercício 1 constrói sobre o 0?

O `ex1` não copia nada do `ex0`: importa a mesma classe `Creature` (as criaturas novas são filhas
dela) e a mesma `CreatureFactory` (as fábricas novas são filhas dela). Por isso o torneio do
exercício 2 mistura, na mesma lista, fábricas do `ex0` e do `ex1`: todas são `CreatureFactory`,
e todas as criaturas são `Creature`
([As criaturas que curam](../04-ex1/03-as-criaturas-que-curam.md#os-dois-imports)).

## Como mudar o jeito de lutar?

Para que o `Sproutling` lute sem curar, nenhuma classe muda: basta inscrevê-lo com outra
estratégia, `(healing, normal)` no lugar de `(healing, defensive)`. Para que a estratégia
defensiva cure **antes** de atacar, só a lista devolvida pelo `act` dela muda:

```python
        return [creature.heal(), creature.attack()]
```

O torneio e as criaturas continuam iguais. A saída do programa muda nas linhas de cura, e o
`diff` com o enunciado passa a mostrar diferenças: depois de experimentar, desfaça a mudança,
para que a saída volte a ser a do enunciado.
