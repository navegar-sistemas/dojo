---
sidebar_position: 2
title: grow e age
---

# grow e age

Os valores dos atributos de um objeto num dado momento formam o **estado** dele: a rosa, agora,
tem 25 cm e 30 dias. O método `show()` do exercício 1 só lê o estado. Os dois métodos novos o
**mudam**: depois de `rose.grow(0.8)`, a rosa tem 25,8 cm.

## Os métodos

```python
    def grow(self, centimeters: float) -> None:
        self.height += centimeters

    def age(self, days: int) -> None:
        self.age_days += days
```

- além do `self`, cada método recebe **quanto** mudar: `grow` recebe os centímetros a crescer, e
  `age` os dias a envelhecer;
- `self.height += centimeters` soma ao atributo `height` **do objeto em que o método foi
  chamado**: `rose.grow(0.8)` muda a rosa, e nenhuma outra planta;
- os dois devolvem `None`: o efeito deles é a mudança no objeto, não um valor devolvido.

## A quantidade como parâmetro

Esta é uma escolha do projeto. O enunciado deixa livre o jeito de crescer e permite acrescentar
parâmetros aos métodos. Com a quantidade como parâmetro, `grow` e `age` fazem só a conta, e o
ritmo de cada planta (0,8 cm por dia para a rosa) fica na simulação.

O enunciado também sugere pensar em **comportamentos** que façam plantas diferentes crescerem de
jeitos diferentes. No projeto, isso aparece no exercício 5: a hortaliça tem o seu próprio
`grow()`, que cresce como qualquer planta e ainda aumenta o valor nutricional
([Vegetable](../07-ex5/06-vegetable.md)).

A escolha também prepara o exercício 6, em que uma única chamada a `grow()` faz um girassol
crescer 30 cm, e uma única chamada a `age()` o envelhece 20 dias.

Outra opção seria guardar na planta um atributo de **taxa de crescimento** (`growth_rate`) e
fazer `grow()` sem parâmetro somar essa taxa. Cada planta teria o seu ritmo próprio, mas o
exercício 6 precisaria de outro jeito para o crescimento de 30 cm de uma vez.

## A altura vira float

Com 0,8 cm por dia, a altura deixa de ser um número inteiro: passa a ser um `float`, o tipo dos
números com casas decimais. A declaração na classe muda de `height: int` para `height: float`. O
`float` pede um cuidado na impressão ([O float e o round](./03-o-float-e-o-round.md)).
