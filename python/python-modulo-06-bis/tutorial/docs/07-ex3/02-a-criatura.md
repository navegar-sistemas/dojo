---
sidebar_position: 2
title: A criatura
---

# A criatura

Toda criatura tem um nome e um tipo, se descreve com a mesma frase e ataca do seu próprio jeito.
`Creature` escreve uma vez o que é igual para todas e deixa o ataque para cada filha, no mesmo
desenho de `DataProcessor` ([A classe abstrata](../02-conceitos/02-a-classe-abstrata.md)).

Crie o arquivo `ex3/creature.py`:

```python title="ex3/creature.py"
from abc import ABC, abstractmethod


class Creature(ABC):
    def __init__(self, name: str, creature_type: str) -> None:
        self.name = name
        self.creature_type = creature_type

    @abstractmethod
    def attack(self) -> str:
        pass

    def describe(self) -> str:
        return f"{self.name} is a {self.creature_type} type Creature"
```

## O construtor

O construtor recebe o nome e o tipo e os guarda nos atributos `name` e `creature_type`, os
"atributos para o nome e o tipo" que o enunciado pede. Diferentemente do `DataProcessor`, este
construtor tem parâmetros: cada filha passa os seus valores
([A família do fogo](./03-a-familia-de-fogo.md)).

O nome `creature_type`, e não `type`, é escolha do tutorial. `type` já é o nome de uma função
embutida do Python (`type(42)` devolve `int`); um parâmetro com esse nome esconderia a função
dentro do construtor e misturaria, para quem lê, o tipo do Python com o tipo da criatura.

Os atributos não levam `_` no começo: `name` é lido de fora, pelos scripts de teste e pelo torneio
do exercício 4.

## attack

`attack` é abstrato: toda criatura ataca, cada uma do seu jeito. O enunciado diz que o ataque
**devolve** uma mensagem; por isso o tipo de retorno é `str`, e o método não imprime nada. Quem
imprime é o script que chama, com `print(criatura.attack())`.

## describe

`describe` é um método comum: a frase é a mesma para todas as criaturas, só mudam os valores. A
f-string monta `Flameling is a Fire type Creature` a partir de `name` e `creature_type`. As
filhas herdam `describe` como está.
