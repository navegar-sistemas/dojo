---
sidebar_position: 1
title: O problema
---

# O problema

Criar uma planta, até aqui, leva quatro linhas: instanciar e preencher três atributos, um por
um. Entre a primeira linha e a última, a planta existe pela metade: um `rose.show()` no meio do
caminho tentaria ler um atributo que ainda não tem valor, e o programa pararia com um erro.

O centro de jardinagem precisa criar muitas plantas depressa. O jeito é **instanciar e preencher
ao mesmo tempo**, numa linha só, de modo que a planta já nasça completa.

## O que o enunciado pede

Um arquivo `ex3/ft_plant_factory.py`, que só pode chamar `print()`, `range()` e `round()`, com:

- a classe `Plant` dos exercícios anteriores, melhorada: as plantas são criadas **diretamente com
  os dados iniciais** (nome, altura inicial, idade inicial);
- cada planta pronta para uso logo depois de criada, por exemplo para crescer com `grow()`;
- pelo menos **cinco** plantas com dados variados;
- todas impressas de forma organizada.

O enunciado avisa que o método `show()` deve servir **sem mudança** para imprimir a saída abaixo.

## A saída esperada

```text
=== Plant Factory Output ===
Created: Rose: 25.0cm, 30 days old
Created: Oak: 200.0cm, 365 days old
Created: Cactus: 5.0cm, 90 days old
Created: Sunflower: 80.0cm, 45 days old
Created: Fern: 15.0cm, 120 days old
```

Cada linha é a linha do `show()` do exercício 2, com `Created: ` na frente.
