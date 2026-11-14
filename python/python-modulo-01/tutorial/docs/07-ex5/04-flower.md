---
sidebar_position: 4
title: Flower
---

# Flower

A flor tem uma cor e pode estar florescendo ou não. Ela começa sem florescer, e `bloom()` a faz
florescer.

```python
class Flower(Plant):
    def __init__(
        self, name: str, height: float, age_days: int, growth_rate: float,
        color: str
    ) -> None:
        super().__init__(name, height, age_days, growth_rate)
        self._color = color
        self._blooming = False

    def bloom(self) -> None:
        self._blooming = True

    def show(self) -> None:
        super().show()
        print(f" Color: {self._color}")
        if self._blooming:
            print(f" {self._name} is blooming beautifully!")
        else:
            print(f" {self._name} has not bloomed yet")
```

- a assinatura do `__init__` não cabe numa linha de 79 caracteres, e os parâmetros vão para as
  linhas de baixo, dentro dos parênteses, como no construtor de `Plant`. O flake8 aceita a quebra
  porque ela está dentro de parênteses abertos;
- `super().__init__(name, height, age_days, growth_rate)` cuida de nome, altura, idade e taxa,
  **com a validação do exercício 4**: uma flor com altura negativa também é recusada;
- `_blooming` guarda se a flor está florescendo: começa `False`, e `bloom()` o põe em `True`. O
  enunciado pede só o atributo da cor; `_blooming` é o estado de que `bloom()` precisa para que o
  `show()` saiba o que imprimir;
- o `show()` imprime a linha de planta (`super().show()`), a cor e uma das duas frases, conforme
  o estado.

Na saída:

```text
Rose: 15.0cm, 10 days old
 Color: red
 Rose has not bloomed yet
[asking the rose to bloom]
Rose: 15.0cm, 10 days old
 Color: red
 Rose is blooming beautifully!
```

A mesma rosa, mostrada antes e depois do `bloom()`.

## color ou _color

O enunciado pede um atributo `color`, e o código guarda a cor em `_color`. É o mesmo atributo, com
a marca da convenção protected que o [exercício 4](../06-ex4/02-encapsulamento.md) pede para os
atributos da classe, do mesmo jeito que a altura virou `_height`. O mesmo vale para
`_trunk_diameter`, `_harvest_season` e `_nutritional_value`.

Estender a convenção aos atributos novos das filhas é escolha do projeto: o enunciado do
exercício 5 não volta a falar dela. A consequência é que `rose.color`, digitado de fora da
classe, não existe; o valor aparece pelo `show()`. Outras opções seriam deixar esses quatro
atributos públicos (sem `_`), já que o enunciado dispensa validá-los, ou acrescentar um getter
para cada um.
