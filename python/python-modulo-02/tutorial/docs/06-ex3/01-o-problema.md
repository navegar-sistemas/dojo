---
sidebar_position: 1
title: O problema
---

# O problema

Os tipos embutidos descrevem problemas **genéricos**, que qualquer programa pode ter: valor
inválido, divisão por zero, arquivo ausente. Uma planta murchando ou um tanque de água vazio não
é nenhum deles. Para esses problemas, o programa pode criar **os seus próprios tipos de erro**,
com nomes que dizem exatamente o que aconteceu.

## O que o enunciado pede

Um arquivo `ex3/ft_custom_errors.py`, que só pode chamar `print()`, com três classes de exceção:

| Classe | Para quê | Herda de |
|---|---|---|
| `GardenError` | um erro básico do jardim | `Exception` |
| `PlantError` | problemas com plantas | `GardenError` |
| `WaterError` | problemas com a rega | `GardenError` |

Cada uma precisa:

- ser uma classe simples que herda de `Exception` ou de `GardenError`;
- ter uma **mensagem padrão** própria, usada quando o erro é criado sem mensagem (o exemplo do
  enunciado é `"Unknown plant error"`, "erro de planta desconhecido").

E funções que lancem esses erros em situações diferentes, mostrem como capturar cada tipo e
mostrem que capturar `GardenError` captura **todos** os erros do jardim.

## A saída esperada

```text
=== Custom Garden Errors Demo ===

Testing PlantError...
Caught PlantError: The tomato plant is wilting!

Testing WaterError...
Caught WaterError: Not enough water in the tank!

Testing catching all garden errors...
Caught GardenError: The tomato plant is wilting!
Caught GardenError: Not enough water in the tank!

All custom error types work correctly!
```

São três testes: um `PlantError` ("o tomateiro está murchando!") capturado como `PlantError`, um
`WaterError` ("falta água no tanque!") capturado como `WaterError`, e os **mesmos dois** erros
capturados por um `except GardenError`.

As regras gerais pedem que os programas mostrem operações que dão certo e que dão errado, mas a
saída de exemplo deste exercício só tem erros. O programa segue a saída de exemplo, que é a
descrição exata do que o exercício deve imprimir; o lado "dá certo" aparece no fim, quando o
programa chega à última linha sem travar.
