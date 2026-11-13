---
sidebar_position: 1
title: O problema
---

# O problema

No exercício 0, qualquer número passava. Mas `100` e `-50` são números válidos e, mesmo assim,
temperaturas em que nenhuma planta cresce. Agora a função precisa recusar também temperaturas
fora de uma faixa razoável: de **0 a 40 graus Celsius**, com os dois limites incluídos (0 e 40
são aceitos).

![Uma linha de temperaturas com a faixa de 0 a 40 destacada em verde. "25" cai dentro e é aceita; "100" fica à direita, quente demais; "-50" fica à esquerda, fria demais; "abc" nem chega à linha, porque int() falha antes de conferir a faixa](/img/ex1/faixa-de-temperatura.svg)

## O que o enunciado pede

Um arquivo `ex1/ft_raise_exception.py`, com as mesmas funções autorizadas do exercício 0 (`int()`
e `print()`), que parte do código do exercício 0 e o melhora:

- em **`input_temperature`**: conferir se a temperatura está entre 0 e 40, com os limites
  incluídos; devolvê-la se estiver, e **lançar** uma exceção se não estiver;
- em **`test_temperature`**: acrescentar os testes com valores extremos, `"100"` e `"-50"`;
- o main do arquivo chama `test_temperature()`.

## A saída esperada

```text
=== Garden Temperature Checker ===

Input data is '25'
Temperature is now 25°C

Input data is 'abc'
Caught input_temperature error: invalid literal for int() with base 10: 'abc'

Input data is '100'
Caught input_temperature error: 100°C is too hot for plants (max 40°C)

Input data is '-50'
Caught input_temperature error: -50°C is too cold for plants (min 0°C)

All tests completed - program didn't crash!
```

Duas mudanças em relação ao exercício 0: o título termina em `Checker`, e há duas mensagens de
erro novas, que não vêm do Python: `100°C is too hot for plants (max 40°C)` ("quente demais
para plantas") e `-50°C is too cold for plants (min 0°C)` ("fria demais"). Quem as escreve é a
própria `input_temperature`, como mostra a [próxima página](./02-raise.md).
