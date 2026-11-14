---
sidebar_position: 6
title: Vegetable
---

# Vegetable

A hortaliça tem uma época de colheita e um valor nutricional, que começa em 0 e aumenta quando a
hortaliça cresce e envelhece. É o único tipo que precisa **mudar** o que `grow()` e `age()`
fazem: além de crescer e envelhecer como qualquer planta, a hortaliça ganha valor nutricional.

```python
class Vegetable(Plant):
    def __init__(
        self, name: str, height: float, age_days: int, growth_rate: float,
        harvest_season: str
    ) -> None:
        super().__init__(name, height, age_days, growth_rate)
        self._harvest_season = harvest_season
        self._nutritional_value = 0.0

    def grow(self) -> None:
        previous_height = self._height
        super().grow()
        if self._height != previous_height:
            self._nutritional_value += 0.5

    def age(self) -> None:
        previous_age = self._age_days
        super().age()
        self._nutritional_value += 0.5 * (self._age_days - previous_age)

    def show(self) -> None:
        super().show()
        print(f" Harvest season: {self._harvest_season}")
        print(f" Nutritional value: {round(self._nutritional_value)}")
```

- `grow()` e `age()` são sobrescritos, e cada um chama o método da classe pai com `super()`: a
  altura e a idade continuam mudando pelo caminho de `Plant`, com a validação;
- antes de chamar a classe pai, cada um guarda o valor anterior (`previous_height`,
  `previous_age`). Depois, compara: o valor nutricional só sobe pelo que a planta **de fato**
  cresceu ou envelheceu. Um crescimento recusado pelo setter (uma taxa negativa que levaria a
  altura abaixo de zero) não muda a altura e não muda o valor nutricional;
- o `show()` imprime o valor com `round()` sem casas, que devolve um inteiro: `0` e `20`, como na
  saída.

## Quanto o valor nutricional sobe

Esta é uma escolha do projeto. O enunciado diz que o valor sobe quando `grow()` e `age()` são
chamados, e a saída mostra que 20 dias de crescer e envelhecer o levam de 0 a 20. O projeto soma
**0,5 por crescimento** e **0,5 por dia envelhecido**: em 20 dias, 20 crescimentos e 20 dias dão
20 × 0,5 + 20 × 0,5 = 20. Os **dois** métodos aumentam o valor, como o enunciado diz, e a soma
bate com a saída.

A conta pelos dias, e não pelas chamadas, prepara o [exercício 6](../08-ex6/01-o-problema.md),
em que `age()` passa a receber quantos dias envelhecer: uma chamada que envelhece 20 dias soma o
mesmo que 20 chamadas de um dia.

O `round()` sem casas arredonda um valor terminado em ,5 para o **par** mais próximo: depois de
uma única chamada, `round(0.5)` imprime `0`, e depois de três, `round(1.5)` imprime `2`. Nos dias
da simulação (um `grow` e um `age` por dia), o valor é sempre inteiro e o arredondamento não muda
nada. Um único `grow()` seguido de `show()` imprime `Nutritional value: 0`: o valor guardado
subiu para `0.5`, e só a exibição arredondou.

Os atributos `_harvest_season` e `_nutritional_value` são os `harvest_season` e
`nutritional_value` pedidos, com a marca protected
([color ou _color](./04-flower.md#color-ou-_color)).

Outra opção seria só `age()` somar 1 por dia, com um valor inteiro desde o começo. A saída seria
a mesma, mas o crescimento não teria efeito nenhum no valor nutricional, ao contrário do que o
enunciado descreve.

## A simulação de 20 dias

```python
    tomato = Vegetable("Tomato", 5.0, 10, 2.1, "April")
    tomato.show()
    print("[make tomato grow and age for 20 days]")
    for _ in range(20):
        tomato.grow()
        tomato.age()
    tomato.show()
```

- o tomate é criado com a taxa de 2,1 cm por dia;
- `range(20)` produz `0` a `19`: vinte voltas. O número da volta não é usado, e o nome `_` é o
  costume para "variável que não interessa";
- a cada dia, o tomate cresce 2,1 cm e envelhece 1 dia. Em 20 dias, 42 cm a mais: de 5,0 para
  47,0 cm, e de 10 para 30 dias.

![Os 20 dias do tomate: a altura sobe em linha reta de 5,0 a 47,0 cm, e o valor nutricional sobe em degraus de 0 a 20, um ponto por dia](/img/ex5/tomate.svg)
