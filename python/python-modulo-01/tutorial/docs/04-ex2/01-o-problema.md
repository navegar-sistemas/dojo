---
sidebar_position: 1
title: O problema
---

# O problema

As plantas do exercício 1 são retratos parados: os dados são preenchidos uma vez e só lidos.
Plantas de verdade mudam. O gerente do jardim quer **simular** o crescimento ao longo do tempo,
e para isso a planta precisa de ações que mudem os seus próprios dados.

## O que o enunciado pede

Um arquivo `ex2/ft_plant_growth.py`, que só pode chamar `print()`, `range()` e `round()`, com:

- a classe `Plant` do exercício 1, reaproveitada;
- dois métodos novos: **`grow()`**, para a planta crescer, e **`age()`**, para ela envelhecer;
- a simulação de **uma semana** (sete dias) de uma planta: a cada dia ela cresce, envelhece e é
  mostrada;
- no fim, o crescimento total da semana, calculado a partir da altura final guardada na planta.

O enunciado deixa livre o como: acrescentar atributos à classe, parâmetros aos métodos, o que for
preciso. Também lembra que plantas diferentes podem crescer de jeitos diferentes.

## A saída esperada

```text
=== Garden Plant Growth ===
Rose: 25.0cm, 30 days old
=== Day 1 ===
Rose: 25.8cm, 31 days old
=== Day 2 ===
Rose: 26.6cm, 32 days old
=== Day 3 ===
Rose: 27.4cm, 33 days old
=== Day 4 ===
Rose: 28.2cm, 34 days old
=== Day 5 ===
Rose: 29.0cm, 35 days old
=== Day 6 ===
Rose: 29.8cm, 36 days old
=== Day 7 ===
Rose: 30.6cm, 37 days old
Growth this week: 5.6cm
```

A rosa começa com 25 cm e 30 dias. A cada dia, cresce **0,8 cm** e envelhece **1 dia**. Em sete
dias, cresce 7 × 0,8 = 5,6 cm. As alturas agora têm uma casa decimal (`25.0cm`), diferente do
exercício 1 (`25cm`).

![Gráfico da altura da rosa do dia 0 ao dia 7: uma reta subindo de 25,0 cm a 30,6 cm, 0,8 cm por dia, com o crescimento total de 5,6 cm marcado à direita](/img/ex2/crescimento-da-semana.svg)
