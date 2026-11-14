---
sidebar_position: 3
title: O método de classe
---

# O método de classe

Criar uma planta exige nome, altura e idade. Às vezes ainda não se sabe nada dela, e o enunciado
pede um jeito de criar uma planta "anônima" direto, sem passar dados. Um **método de classe**
serve para isso: em vez do objeto, ele recebe a **classe**, e pode usá-la para criar objetos.

## O decorador @classmethod

```python
    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant", 0.0, 0, 0.0)
```

- `@classmethod` passa o método pela função `classmethod()`, autorizada neste exercício;
- o primeiro parâmetro, por costume chamado `cls` (de *class*), é a classe em que o método foi
  chamado. Em `Plant.anonymous()`, o `cls` é `Plant`;
- `cls("Unknown plant", 0.0, 0, 0.0)` é o mesmo que `Plant("Unknown plant", 0.0, 0, 0.0)`: cria
  uma planta com o nome `Unknown plant`, 0 cm e 0 dias, os valores da saída do enunciado. A taxa
  de crescimento não aparece na saída, e a planta anônima fica com `0.0`: sem dados, ela não
  cresce.

Quem chama não passa nada: `Plant.anonymous()` devolve a planta pronta.

## Um experimento

```python title="experimentos/de_classe.py"
class Plant:
    def __init__(self, name: str) -> None:
        self._name = name

    @classmethod
    def anonymous(cls) -> "Plant":
        return cls("Unknown plant")

    def show(self) -> None:
        print(f"Plant: {self._name}")


unknown = Plant.anonymous()
unknown.show()
```

```bash
python3 experimentos/de_classe.py
```

```text
Plant: Unknown plant
```

`Plant.anonymous()` foi chamado na classe, criou um objeto e o devolveu; `unknown.show()` é um
método comum desse objeto.

## Por que "Plant" entre aspas

O type hint de retorno, `-> "Plant"`, vem entre aspas. Nas versões do Python antes da 3.14, as
anotações de um método são lidas no momento em que o `def` é lido, e nesse momento a classe
`Plant` ainda está sendo escrita e o nome `Plant` ainda não existe: sem aspas, o programa pararia
com um erro dizendo que `Plant` não está definido. Entre aspas, a anotação é só um texto que o
mypy lê depois, quando a classe já existe. O enunciado aceita o Python 3.10, e as aspas fazem o
código funcionar nele.

## Por que cls, e não Plant

Escrever `Plant(...)` dentro do método também funcionaria aqui. Com `cls`, o método respeita a
classe em que foi chamado: numa classe filha que tivesse o mesmo construtor, `Filha.anonymous()`
criaria um objeto da filha. É o uso típico de um método de classe: um **construtor alternativo**,
com um nome que diz o que ele cria.

As filhas deste projeto têm construtores com mais parâmetros (a cor da flor, o diâmetro do
tronco), e por isso `Flower.anonymous()` pararia com um erro de argumentos faltando. Só
`Plant.anonymous()` é usado.
