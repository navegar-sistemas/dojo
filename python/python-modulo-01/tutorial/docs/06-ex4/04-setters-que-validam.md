---
sidebar_position: 4
title: Setters que validam
---

# Setters que validam

Um **setter** ("ajustador") é um método que muda o valor de um atributo protegido, depois de
**validar** o valor novo, isto é, conferir se ele serve. Depois que a planta existe, ele é o
único caminho para mudar a altura e a idade: quem está de fora chama o setter, e os métodos da
própria classe que mudam esses valores também o chamam.

```python
    def set_height(self, height: float) -> bool:
        if height < 0:
            print(f"{self._name}: Error, height can't be negative")
            return False
        self._height = height
        return True

    def set_age(self, age_days: int) -> bool:
        if age_days < 0:
            print(f"{self._name}: Error, age can't be negative")
            return False
        self._age_days = age_days
        return True
```

- valor negativo: o setter imprime a mensagem de erro **de dentro da classe**, como o enunciado
  pede, e sai com `return False` **antes** de guardar. O atributo continua com o valor antigo;
- valor válido (zero ou positivo): o setter guarda e devolve `True`;
- a mensagem começa com o nome da planta, `Rose: Error, height can't be negative`, como na saída
  do enunciado.

![Duas chamadas ao setter de uma rosa com 15 cm: set_height(25.0) passa pela validação, a altura vira 25,0 e o setter devolve True; set_height(-5.0) é barrado, a mensagem de erro é impressa, a altura continua 25,0 e o setter devolve False](/img/ex4/setter.svg)

## Por que devolver um bool

O valor devolvido (`True` ou `False`, o tipo `bool`) conta a quem chamou se a mudança foi
aceita. É ele que permite ao programa imprimir `Height updated` ou `Height update rejected`
([As mensagens de atualização](./06-as-mensagens-de-atualizacao.md)), e ao construtor
reaproveitar os setters sem imprimir nada a mais
([O construtor usa os setters](./05-o-construtor-usa-os-setters.md)).

## grow e age também passam pelos setters

```python
    def grow(self, centimeters: float) -> None:
        self.set_height(self._height + centimeters)

    def age(self, days: int) -> None:
        self.set_age(self._age_days + days)
```

Crescer e envelhecer também mudam altura e idade, então também passam pela validação: um
`grow(-20.0)` numa planta de 15 cm daria altura negativa, e é recusado com a mesma mensagem. O
valor devolvido pelo setter não interessa a `grow` e `age`, que o ignoram.
