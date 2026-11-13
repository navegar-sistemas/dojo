---
sidebar_position: 6
title: Vegetable
---

# Vegetable

A hortaliça tem uma época de colheita e um valor nutricional, que começa em 0 e aumenta quando a
hortaliça cresce e envelhece. É o único tipo que precisa **mudar** o que `grow()` e `age()`
fazem: além de crescer e envelhecer como qualquer planta, cada chamada aumenta o valor
nutricional.

```python
class Vegetable(Plant):
    def __init__(
        self, name: str, height: float, age_days: int,
        harvest_season: str
    ) -> None:
        super().__init__(name, height, age_days)
        self._harvest_season = harvest_season
        self._nutritional_value = 0.0

    def grow(self, centimeters: float) -> None:
        super().grow(centimeters)
        self._nutritional_value += 0.5

    def age(self, days: int) -> None:
        super().age(days)
        self._nutritional_value += 0.5

    def show(self) -> None:
        super().show()
        print(f" Harvest season: {self._harvest_season}")
        print(f" Nutritional value: {round(self._nutritional_value)}")
```

- `grow()` e `age()` são sobrescritos, e cada um chama o método da classe pai com `super()`: a
  altura e a idade continuam mudando pelo caminho de `Plant`, com a validação;
- depois, cada um soma 0,5 ao valor nutricional;
- o `show()` imprime o valor com `round()` sem casas, que devolve um inteiro: `0` e `20`, como na
  saída.

## Quanto o valor nutricional sobe

Esta é uma escolha do projeto. O enunciado diz que o valor sobe quando `grow()` e `age()` são
chamados, e a saída mostra que 20 dias de crescer e envelhecer o levam de 0 a 20. São 40
chamadas (20 de cada), e 40 × 0,5 = 20. Com 0,5 por chamada, **os dois** métodos aumentam o
valor, como o enunciado diz, e a soma bate com a saída.

O `round()` sem casas arredonda um valor terminado em ,5 para o **par** mais próximo: depois de
uma única chamada, `round(0.5)` imprime `0`, e depois de três, `round(1.5)` imprime `2`. Nas
chamadas em pares da simulação (um `grow` e um `age` por dia), o valor é sempre inteiro e o
arredondamento não muda nada. Na avaliação, se pedirem um único `grow()` seguido de `show()`, a
linha continua `Nutritional value: 0`: o valor guardado subiu para `0.5`, e só a exibição
arredondou.

Os atributos `_harvest_season` e `_nutritional_value` são os `harvest_season` e
`nutritional_value` pedidos, com a marca protected
([color ou _color](./04-flower.md#color-ou-_color)).

Outra opção seria só `age()` somar 1 por chamada, com um valor inteiro desde o começo. A saída
seria a mesma, mas o crescimento não teria efeito nenhum no valor nutricional, ao contrário do que
o enunciado descreve.

## A simulação de 20 dias

```python
    tomato = Vegetable("Tomato", 5.0, 10, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for _ in range(20):
        tomato.grow(2.1)
        tomato.age(1)
    tomato.show()
```

- `range(20)` produz `0` a `19`: vinte voltas. O número da volta não é usado, e o nome `_` é o
  costume para "variável que não interessa";
- a cada dia, o tomate cresce 2,1 cm e envelhece 1 dia. Em 20 dias, 42 cm a mais: de 5,0 para
  47,0 cm, e de 10 para 30 dias.

![Os 20 dias do tomate: a altura sobe em linha reta de 5,0 a 47,0 cm, e o valor nutricional sobe em degraus de 0 a 20, um ponto por dia](/img/ex5/tomate.svg)
