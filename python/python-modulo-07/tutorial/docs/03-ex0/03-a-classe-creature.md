---
sidebar_position: 3
title: A classe Creature
---

# A classe Creature

Toda criatura tem um nome e um tipo, sabe se descrever e sabe atacar. A descrição segue o mesmo
modelo para todas; o ataque é próprio de cada uma. `Creature` guarda o que é comum e deixa o
ataque para as filhas.

Crie o arquivo `ex0/creature.py` com:

```python
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

É o formato do `Vehicle` de [Classe abstrata e super](../02-conceitos/02-classe-abstrata-e-super.md):

- `Creature` herda de `ABC`, o que faz o Python cobrar os métodos abstratos: com o `attack`
  abstrato, ela não pode ser instanciada;
- o `__init__` guarda os dois atributos que o enunciado pede, o nome e o tipo, em `self.name` e
  `self.creature_type`;
- `attack` é abstrato: toda criatura concreta escreve o seu;
- `describe` é o método concreto pedido: devolve a mensagem padrão, como
  `Flameling is a Fire type Creature`. As filhas o herdam sem mudança.

## Os nomes dos atributos

O enunciado pede "atributos para o nome e o tipo", sem dar os nomes. `name` é direto. Para o tipo,
o tutorial escolhe `creature_type`, e não `type`: `type` é o nome de uma função embutida do
Python (`type(42)` responde `<class 'int'>`), e um parâmetro chamado `type` esconderia essa
função dentro do `__init__`. Um atributo cujo nome começa com `_` é, por costume, **interno**: só o
código da própria classe deveria usá-lo. Os dois atributos não levam `_` porque o código de fora,
como o torneio, lê o nome da criatura.

## Devolver em vez de imprimir

`attack` e `describe` **devolvem** o texto, e quem chama decide o que fazer com ele: o
`battle.py` imprime, e a estratégia do exercício 2 junta os textos numa lista, que o torneio
imprime. O enunciado pede assim: o `attack` "vai devolver uma mensagem de texto apropriada", e o
`describe` "vai devolver uma mensagem padrão".

As quatro criaturas entram no fim deste mesmo arquivo ([As quatro criaturas](./04-as-quatro-criaturas.md)).
