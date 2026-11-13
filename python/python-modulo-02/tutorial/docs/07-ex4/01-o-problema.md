---
sidebar_position: 1
title: O problema
---

# O problema

Alguns trabalhos têm um começo e um fim obrigatório: um arquivo aberto precisa ser fechado, uma
válvula de irrigação aberta precisa ser fechada. Essas coisas que se abrem e precisam ser
devolvidas são chamadas de **recursos**. Se um erro acontece no meio do trabalho, o código que
fecharia o recurso pode ser pulado, e a válvula fica aberta. O bloco **`finally`** resolve isso:
ele roda **sempre**, com erro ou sem erro.

## O que o enunciado pede

Um arquivo `ex4/ft_finally_block.py`, que só pode chamar `print()` e o método
`str.capitalize()`, com:

- uma função **`water_plant(plant_name)`** que tenta regar uma planta: dá certo se o nome
  estiver **capitalizado** (primeira letra maiúscula, o resto minúsculo, como `Tomato`), imprime
  uma mensagem de sucesso, e lança o `PlantError` do exercício 3 se o nome não estiver
  capitalizado;
- uma função **`test_watering_system()`** que:
  - "abre" o sistema de irrigação (só imprime uma mensagem);
  - rega várias plantas com `water_plant()`;
  - usa a estrutura `try` / `except` / `finally`;
  - quando o nome de uma planta é inválido, trata o erro, **interrompe o teste e volta
    imediatamente para o main**;
  - **sempre** "fecha" o sistema de irrigação, num bloco `finally`;
  - mostra que essa limpeza acontece mesmo quando há erro.

## A saída esperada

```text
=== Garden Watering System ===

Testing valid plants...
Opening watering system
Watering Tomato: [OK]
Watering Lettuce: [OK]
Watering Carrots: [OK]
Closing watering system

Testing invalid plants...
Opening watering system
Watering Tomato: [OK]
Caught PlantError: Invalid plant name to water: 'lettuce'
.. ending tests and returning to main
Closing watering system

Cleanup always happens, even with errors!
```

Dois testes. No primeiro, com plantas válidas (Tomato, Lettuce e Carrots: tomate, alface e
cenouras), o sistema abre, rega as três e fecha. No segundo, a segunda planta está escrita
`lettuce`, com minúscula: o erro é capturado, o teste para ali (`Carrots` não é regada), e mesmo
assim o sistema fecha. A última linha, "a limpeza sempre acontece, mesmo com erros", é impressa
pelo main.
