---
sidebar_position: 4
title: A semana
---

# A semana

A simulação repete o mesmo dia sete vezes: crescer, envelhecer, mostrar. Um laço `for` com
`range()` faz a repetição.

## range

`range(início, fim)` produz os números inteiros do `início` até o `fim`, **sem incluir o fim**.
`range(1, 8)` produz `1, 2, 3, 4, 5, 6, 7`: os sete dias, já com o número que a saída imprime
(`=== Day 1 ===` a `=== Day 7 ===`). O `range` é uma das funções autorizadas.

## O laço

```python
    print("=== Garden Plant Growth ===")
    rose.show()
    start_height = rose.height
    for day in range(1, 8):
        print(f"=== Day {day} ===")
        rose.grow()
        rose.age()
        rose.show()
```

- antes do laço, a rosa é mostrada no estado inicial: `Rose: 25.0cm, 30 days old`;
- `start_height` guarda a altura do começo da semana, para a conta do fim;
- a cada volta, `day` vale o número do dia, e a rosa cresce a sua taxa (0,8 cm), envelhece 1 dia
  e é mostrada.

## O crescimento da semana

O aumento total vem **dos dados da classe**, como o enunciado pede: a altura final é lida da
própria planta, e não somada à parte.

```python
    growth = rose.height - start_height
    print(f"Growth this week: {round(growth, 1)}cm")
```

`rose.height` é a altura guardada no objeto depois dos sete dias. A subtração dá
`5.600000000000005`, pela aproximação do `float`
([O float e o round](./03-o-float-e-o-round.md)), e o `round(growth, 1)` imprime `5.6`.
