---
sidebar_position: 4
title: A capacidade
---

# A capacidade

Algumas criaturas sabem se transformar numa forma de combate e voltar ao normal; a família do fogo
não sabe. Se `transform` e `revert` ficassem em `Creature`, toda criatura seria obrigada a
escrevê-los, inclusive as que não se transformam. A habilidade fica numa classe abstrata à parte,
a **capacidade**, e só as criaturas que a têm herdam dela.

Crie o arquivo `ex3/capability.py`:

```python title="ex3/capability.py"
from abc import ABC, abstractmethod


class TransformCapability(ABC):
    def __init__(self) -> None:
        self.transformed = False

    @abstractmethod
    def transform(self) -> str:
        pass

    @abstractmethod
    def revert(self) -> str:
        pass
```

## Não é uma criatura

`TransformCapability` herda de `ABC`, e não de `Creature`: o enunciado proíbe que a capacidade
herde de `Creature`. Ela descreve só a habilidade, e por isso não tem nome, tipo nem ataque. Uma
criatura que se transforma herda das duas classes
([A família que se transforma](./05-a-familia-que-se-transforma.md)). O que se perderia com a
habilidade dentro de `Creature` é uma das perguntas do enunciado, respondida em
[As perguntas do enunciado](../09-fechamento/03-as-perguntas-do-enunciado.md#capacidade-na-base).

## O estado de transformação

O enunciado pede um atributo que guarde se a criatura está transformada. O construtor cria
`self.transformed`, que começa em `False`: toda criatura nasce na forma normal. Quem herda de
`TransformCapability` precisa rodar esse construtor
([A correção: chamar o construtor de cada mãe](../06-pacotes/02-heranca-multipla.md#a-correção-chamar-o-construtor-de-cada-mãe)).

O atributo também "muda o que `attack` devolve", como pede o enunciado. Essa parte fica em cada
criatura, porque cada uma tem as suas frases: o `attack` dela consulta `self.transformed`.

## transform e revert

Os dois métodos são abstratos: cada criatura escreve como se transforma e como volta ao normal.
O enunciado não diz o que eles devolvem. A escolha do tutorial é devolver a frase da saída, como
`attack` faz: todos os métodos de ação das criaturas ficam com o mesmo formato (fazem a ação e
devolvem a frase), e quem chama decide imprimir.
