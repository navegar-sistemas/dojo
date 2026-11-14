---
sidebar_position: 2
title: grow e age
---

# grow e age

Os valores dos atributos de um objeto num dado momento formam o **estado** dele: a rosa, agora,
tem 25 cm e 30 dias. O método `show()` do exercício 1 só lê o estado. Os dois métodos novos o
**mudam**: depois de `rose.grow()`, a rosa tem 25,8 cm.

## A taxa de crescimento

Plantas diferentes crescem em ritmos diferentes: a rosa cresce 0,8 cm por dia, e um cacto, bem
menos. O ritmo é uma característica da planta, e por isso vira um atributo novo,
`growth_rate` ("taxa de crescimento"), em centímetros por dia:

```python
class Plant:
    name: str
    height: float
    age_days: int
    growth_rate: float
```

Ele é preenchido como os outros, depois de instanciar: `rose.growth_rate = 0.8`.

## Os métodos

```python
    def grow(self) -> None:
        self.height += self.growth_rate

    def age(self) -> None:
        self.age_days += 1
```

- `grow()` soma à altura a taxa **da própria planta**: `rose.grow()` faz a rosa crescer 0,8 cm, e
  uma planta com taxa 1,5 cresceria 1,5 cm com a mesma chamada;
- `age()` soma um dia à idade;
- `self.height += self.growth_rate` muda o atributo `height` **do objeto em que o método foi
  chamado**: `rose.grow()` muda a rosa, e nenhuma outra planta;
- os dois devolvem `None`: o efeito deles é a mudança no objeto, não um valor devolvido.

## Por que um atributo, e não um parâmetro

Esta é uma escolha do projeto. O enunciado deixa livre o jeito de crescer, aceita tanto atributos
novos quanto parâmetros novos nos métodos, e sugere dar às plantas **comportamentos** que façam o
`grow()` funcionar de forma diferente de planta para planta. Com a taxa guardada na planta, cada
planta já sabe quanto cresce, e quem chama `grow()` não precisa saber.

Outra opção seria `grow()` receber os centímetros como parâmetro (`rose.grow(0.8)`). Aí o ritmo
ficaria em quem chama, e não na planta, e duas chamadas `grow(0.4)` cresceriam o mesmo que uma
`grow(0.8)`. Isso pesa no [exercício 5](../07-ex5/06-vegetable.md), em que cada crescimento de
uma hortaliça aumenta o valor nutricional dela: com o parâmetro, o valor dependeria de como o
crescimento foi dividido em chamadas.

## A altura vira float

Com 0,8 cm por dia, a altura deixa de ser um número inteiro: passa a ser um `float`, o tipo dos
números com casas decimais. A declaração na classe muda de `height: int` para `height: float`. O
`float` pede um cuidado na impressão ([O float e o round](./03-o-float-e-o-round.md)).
