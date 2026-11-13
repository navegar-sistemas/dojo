---
sidebar_position: 3
title: As perguntas do enunciado
---

# As perguntas do enunciado

O enunciado deixa uma pergunta no fim dos exercícios 1, 2, 3 e 4, respondidas abaixo. Também avisa
que, na avaliação, pode ser pedido que você explique o polimorfismo, mostre a sobrescrita de
métodos, acrescente ao sistema um tipo de dado novo, uma família de criaturas nova ou uma
estratégia nova, ou mude o jeito de processar um dado; e pede que você saiba explicar como a
herança reaproveita código e, ao mesmo tempo, deixa cada classe especializar o comportamento, e
por que cada padrão de projeto existe.

## Exercício 1: como o polimorfismo deixa o DataStream tratar tipos diferentes sem conhecê-los?

A pergunta completa: "Como o polimorfismo permite que o `DataStream` trate diferentes tipos de
dados no fluxo sem conhecer as suas implementações específicas? Quais são os benefícios dessa
abordagem de design?".

`DataStream` guarda uma `list[DataProcessor]` e só chama os métodos que a classe abstrata
garante: `validate`, `ingest`, `total`, `remaining` e `output`. Em `processor.validate(element)`,
o Python roda o `validate` da classe do objeto guardado ali, seja ela `NumericProcessor`,
`TextProcessor` ou `LogProcessor`. O fluxo pergunta "você aceita?" e "guarde", e cada processador
responde do seu jeito ([Registrar e rotear](../04-ex1/03-registrar-e-rotear.md)).

Os benefícios desse desenho:

- **Extensão sem alteração:** um tipo de dado novo é uma classe nova; `DataStream` não muda
  ([Acrescentar um tipo de dado novo](#acrescentar-um-tipo-de-dado-novo));
- **Cada regra num lugar só:** o que é um número válido está só no `NumericProcessor`; a fila e o
  rank estão só no `DataProcessor`;
- **Erros cedo:** a classe abstrata impede criar um processador que esqueceu um método
  (`TypeError` ao instanciar), e o mypy confere assinaturas e plugins antes de rodar;
- **Testes separados:** cada processador é testado sozinho, como no exercício 0, e o fluxo é
  testado com qualquer processador.

## Exercício 2: ABC ou Protocol, qual é a diferença real? \{#abc-ou-protocol}

A pergunta completa: "`DataProcessor` é uma ABC e `ExportPlugin` é um `Protocol`. Os dois
restringem o que uma classe precisa oferecer. Qual é a diferença real, e por que um sistema de
plugins quer o segundo?".

A diferença está em **como uma classe entra na regra**:

- com a **ABC**, pelo **nome**: uma classe é um `DataProcessor` só se herdar dele, declarando a
  relação no `class NumericProcessor(DataProcessor)`. Isso se chama **tipagem nominal**. O Python
  confere a regra enquanto o programa roda (instanciar uma filha incompleta lança `TypeError`, e
  `isinstance(objeto, DataProcessor)` funciona), e a ABC ainda passa código pronto às filhas, como
  a fila e o `output`;
- com o **Protocol**, pela **forma**: uma classe é um `ExportPlugin` se tiver o método
  `process_output` com a assinatura certa, sem herdar dele e sem nem saber que ele existe. Isso se
  chama **tipagem estrutural**, a versão conferida pelo mypy do duck typing
  ([Protocol e duck typing](../05-ex2/02-protocol-e-duck-typing.md)). Quem confere é só o mypy,
  antes de rodar ([Um plugin que não cumpre a regra](../05-ex2/08-rodar-e-conferir.md#plugin-errado));
  no programa rodando, o `Protocol` não faz nada. Nem `isinstance` funciona com ele:

```bash
python3 -B -c 'from data_pipeline import CSVExportPlugin, ExportPlugin
print(isinstance(CSVExportPlugin(), ExportPlugin))'
```

A última linha da saída é:

```text
TypeError: Instance and class checks can only be used with @runtime_checkable protocols
```

("conferências de instância e de classe só podem ser usadas com protocols marcados com
`@runtime_checkable`", um decorador de `typing` que o projeto não precisa).

Um sistema de plugins quer o `Protocol` porque os plugins vêm **de fora**: são escritos por
outras pessoas, às vezes antes de o `ExportPlugin` existir, às vezes em bibliotecas que não podem
ser mudadas. Exigir herança obrigaria cada plugin a importar a classe do projeto e a se amarrar a
ela. E a herança não daria nada em troca: os plugins não compartilham código, só o nome de um
método. Com o `Protocol`, qualquer classe com o `process_output` certo encaixa, e o mypy ainda
confere a assinatura. Os processadores, ao contrário, compartilham a fila, o rank e o `output`, e
para eles a ABC é a escolha certa.

## Exercício 3: o que se perderia com a capacidade dentro de Creature? \{#capacidade-na-base}

A pergunta completa: "Uma capacidade é uma classe abstrata que, de propósito, não é uma
`Creature`. O que quebraria, ou se tornaria impossível, se você tivesse colocado `transform` e
`revert` na classe base `Creature`?".

Com `transform` e `revert` como métodos abstratos de `Creature`:

- **toda criatura seria obrigada a se transformar.** `Flameling` e `Pyrodon` teriam de escrever
  um `transform` e um `revert` de mentira (que não fazem nada, ou que lançam um erro); sem eles,
  `Flameling()` lançaria `TypeError`, como toda classe com método abstrato faltando
  ([A classe abstrata](../02-conceitos/02-a-classe-abstrata.md)). A classe afirmaria uma
  habilidade que não tem;
- **ficaria impossível perguntar quem se transforma.** Hoje,
  `isinstance(criatura, TransformCapability)` separa as duas famílias. Com tudo em `Creature`,
  toda criatura "tem" `transform`, e a estratégia agressiva não conseguiria recusar um `Flameling`
  antes da luta: o erro apareceria no meio dela, ou a criatura fingiria se transformar;
- **cada habilidade nova mudaria a base de todas as famílias.** Uma capacidade de voar, por
  exemplo, entraria em `Creature` e obrigaria todas as criaturas existentes a escrever `fly`. Com
  capacidades separadas, uma habilidade nova é uma classe nova, e só quem a tem herda dela;
- **as habilidades não se combinariam.** Uma criatura pode herdar de várias capacidades
  (transformar e curar, por exemplo) e escolher quais tem; dentro de `Creature`, seriam todas ou
  nenhuma;
- **o estado de transformação ocuparia todas as criaturas**, inclusive as que nunca se
  transformam.

## Exercício 4: para onde foi a decisão de como lutar?

A pergunta completa: "O código do torneio nunca confere a que família uma criatura pertence, e
mesmo assim cada uma luta de um jeito diferente. Para onde foi essa decisão, e o que isso lhe dá
no dia em que uma nova capacidade for acrescentada?".

A decisão foi para as **estratégias**. O torneio só chama `strategy.act(creature)`
([O torneio](../08-ex4/06-o-torneio.md)); cada estratégia sabe o que fazer (só atacar, ou
transformar, atacar e voltar) e confere, com `isinstance` sobre a capacidade, se a criatura serve
para ela. As próprias criaturas completam a decisão: cada uma tem o seu `attack`.

No dia em que surgir uma capacidade nova, o trabalho é **acrescentar** código, sem mudar o que
existe: a classe da capacidade, as criaturas que a têm com a sua fábrica, e uma estratégia que a
use. A função `battle`, as estratégias antigas e as famílias antigas ficam como estão.

## Uma família, uma capacidade e uma estratégia novas

O experimento abaixo faz exatamente isso, fora dos pacotes, e cobre três pedidos da avaliação de
uma vez: uma **capacidade** nova (curar), uma **família** nova (as criaturas de planta, com a sua
fábrica) e uma **estratégia** nova (a de suporte, que cura e depois ataca). Crie
`experimentos/nova_familia.py`:

```python title="experimentos/nova_familia.py"
from abc import ABC, abstractmethod

from battle import test_factory
from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex3.creature import Creature
from ex4 import (
    AggressiveStrategy,
    BattleStrategy,
    NormalStrategy,
    StrategyError,
)
from tournament import battle


class HealCapability(ABC):
    @abstractmethod
    def heal(self) -> str:
        pass


class Sproutle(Creature, HealCapability):
    def __init__(self) -> None:
        super().__init__("Sproutle", "Grass")

    def attack(self) -> str:
        return f"{self.name} uses Vine Whip!"

    def heal(self) -> str:
        return f"{self.name} soaks up the sun and heals."


class Bloomoth(Creature, HealCapability):
    def __init__(self) -> None:
        super().__init__("Bloomoth", "Grass/Bug")

    def attack(self) -> str:
        return f"{self.name} uses Petal Storm!"

    def heal(self) -> str:
        return f"{self.name} spreads healing pollen."


class GrassFactory(CreatureFactory):
    def create_base(self) -> Creature:
        return Sproutle()

    def create_evolved(self) -> Creature:
        return Bloomoth()


class SupportStrategy(BattleStrategy):
    name = "Support"

    def is_valid(self, creature: Creature) -> bool:
        return isinstance(creature, HealCapability)

    def act(self, creature: Creature) -> None:
        if not isinstance(creature, HealCapability):
            raise StrategyError(f"Invalid Creature '{creature.name}' "
                                "for this support strategy")
        print(creature.heal())
        print(creature.attack())


test_factory(GrassFactory())
print()
battle([
    (GrassFactory(), SupportStrategy()),
    (FlameFactory(), NormalStrategy()),
    (TransformCreatureFactory(), AggressiveStrategy()),
])
```

- `HealCapability` é uma capacidade como `TransformCapability`: abstrata, sem herdar de
  `Creature`. Ela não guarda estado, e por isso não tem `__init__`: o `super().__init__` das
  criaturas chega ao construtor de `Creature`, e não há outro construtor para chamar;
- `GrassFactory` é uma fábrica como as do `ex3`, com as duas criaturas da família nova;
- `SupportStrategy` segue o desenho de `AggressiveStrategy`, com `isinstance` sobre a capacidade
  nova;
- `test_factory` vem de `battle.py` e `battle` vem de `tournament.py`, os dois sem nenhuma
  mudança. O `main` deles não roda, por causa do `if __name__ == "__main__":`.

O arquivo fica em `experimentos/`, e os módulos que ele importa, na pasta do projeto. Para o
Python achá-los, a variável `PYTHONPATH`, escrita antes do comando, acrescenta a pasta atual
(`.`) aos lugares onde ele procura módulos:

```bash
PYTHONPATH=. python3 -B experimentos/nova_familia.py
```

```text
Testing factory
Sproutle is a Grass type Creature
Sproutle uses Vine Whip!
Bloomoth is a Grass/Bug type Creature
Bloomoth uses Petal Storm!

*** Tournament ***
3 opponents involved

* Battle *
Sproutle is a Grass type Creature
 vs.
Flameling is a Fire type Creature
 now fight!
Sproutle soaks up the sun and heals.
Sproutle uses Vine Whip!
Flameling uses Ember!

* Battle *
Sproutle is a Grass type Creature
 vs.
Shiftling is a Normal type Creature
 now fight!
Sproutle soaks up the sun and heals.
Sproutle uses Vine Whip!
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.

* Battle *
Flameling is a Fire type Creature
 vs.
Shiftling is a Normal type Creature
 now fight!
Flameling uses Ember!
Shiftling shifts into a sharper form!
Shiftling performs a boosted strike!
Shiftling returns to normal.
```

```bash
.venv/bin/flake8 experimentos/nova_familia.py
.venv/bin/mypy --disallow-untyped-defs experimentos/nova_familia.py
```

```text
Success: no issues found in 1 source file
```

O `test_factory` do exercício 3 tratou a família nova como as outras, e o torneio com três
oponentes fez as três batalhas, cada criatura com a sua estratégia. Nenhuma linha de `ex3`, `ex4`,
`battle.py` ou `tournament.py` mudou.

## Mostrar a sobrescrita

`NumericProcessor.validate` sobrescreve o `validate` abstrato de `DataProcessor`: mesmo nome,
mesma assinatura, corpo próprio. `ingest` também é sobrescrito, com uma assinatura mais
específica em cada filha. `output` **não** é sobrescrito: as três filhas usam o da mãe. O atributo
`name` também é sobrescrito em cada filha
([Nome e contadores](../04-ex1/02-nome-e-contadores.md)).

Nas criaturas, `attack` é sobrescrito em cada uma, e `describe` não: as quatro usam o de
`Creature`. Em `Shiftling` e `Morphagon`, o `attack` sobrescrito ainda muda conforme o atributo
`transformed` ([A família que se transforma](../07-ex3/05-a-familia-que-se-transforma.md)).

## Acrescentar um tipo de dado novo

Nenhum processador aceita `True` e `False`
([A armadilha do bool](../02-conceitos/03-any-uniao-e-isinstance.md#a-armadilha-do-bool)). Um
processador novo resolve isso sem tocar em `DataStream` nem nos plugins. Crie
`experimentos/bool_processor.py`:

```python title="experimentos/bool_processor.py"
from typing import Any

from data_pipeline import (
    CSVExportPlugin,
    DataProcessor,
    DataStream,
    NumericProcessor,
)


class BoolProcessor(DataProcessor):
    name = "Bool Processor"

    def validate(self, data: Any) -> bool:
        return isinstance(data, bool)

    def ingest(self, data: bool) -> None:
        if not self.validate(data):
            raise TypeError("Improper bool data")
        self._store("yes" if data else "no")


stream = DataStream()
stream.register_processor(NumericProcessor())
stream.register_processor(BoolProcessor())
stream.process_stream([True, 7, False, "?"])
stream.print_processors_stats()
stream.output_pipeline(5, CSVExportPlugin())
```

O `import` em várias linhas, entre parênteses, traz quatro nomes do `data_pipeline`.

```bash
PYTHONPATH=. python3 -B experimentos/bool_processor.py
```

```text
DataStream error - Can't process element in stream: ?
== DataStream statistics ==
Numeric Processor: total 1 items processed, remaining 1 on processor
Bool Processor: total 2 items processed, remaining 2 on processor
CSV Output:
7
CSV Output:
yes,no
```

`BoolProcessor` herdou a fila, o rank, o `output`, o `total` e o `remaining` sem escrever nada
disso; escreveu só o que é dele: o nome, a conferência e a conversão para texto. O fluxo e o
plugin CSV trataram os valores novos sem nenhuma mudança.

## Mudar o jeito de processar

Uma mudança de comportamento de um tipo de dado fica dentro da classe dele. Para guardar os logs
como `[ERROR] Unauthorized access!!` em vez de `ERROR: Unauthorized access!!`, só a linha do
`_store` do `LogProcessor` muda:

```python
            self._store(f"[{item['log_level']}] {item['log_message']}")
```

O fluxo, os plugins e os outros processadores continuam iguais. A saída do programa muda nas
linhas de log, e por isso o `diff` com o enunciado passa a mostrar diferenças: a mudança é só
para a demonstração na avaliação.

Do mesmo jeito, mudar como uma criatura luta é mexer só na estratégia dela: dar a estratégia
normal ao `Shiftling`, no `main` de `tournament.py`, faz ele só atacar, sem que o torneio mude.

## Por que cada padrão existe

| Padrão | Problema que resolve | No projeto |
|---|---|---|
| fábrica abstrata | o código que usa objetos de uma família não deveria depender das classes concretas, nem saber criá-las | `CreatureFactory` e as duas fábricas; os scripts recebem uma fábrica e só conhecem `Creature`. Trocar de família é passar outra fábrica, e o pacote esconde as criaturas concretas |
| capacidade | dar uma habilidade só a algumas classes de uma família, sem impor a habilidade a todas | `TransformCapability`, herdada só por `Shiftling` e `Morphagon`; quem precisa da habilidade pergunta com `isinstance` |
| estratégia abstrata | o jeito de agir muda de objeto para objeto, e o código que organiza a ação não deveria conhecer cada jeito | `BattleStrategy` e as duas estratégias; o torneio só chama `act`, e a mesma criatura pode lutar com outra estratégia sem que nada mais mude |

## Como a herança reaproveita código e deixa cada classe se especializar?

A mãe escreve uma vez o que é igual para todas as filhas, e cada filha escreve só o que muda. Em
`DataProcessor`, a fila, o rank, `output`, `total`, `remaining` e `_store` são comuns, e cada
processador escreve `validate`, `ingest` e `name`. Em `Creature`, o nome, o tipo e `describe` são
comuns, e cada criatura escreve o seu `attack`. Os métodos abstratos são o contrato: garantem que
toda filha escreve a sua parte, e é esse contrato que permite ao `DataStream`, aos scripts de
teste e ao torneio usarem qualquer filha sem conhecê-la.
