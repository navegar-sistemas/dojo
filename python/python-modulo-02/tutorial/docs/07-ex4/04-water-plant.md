---
sidebar_position: 4
title: water_plant
---

# water_plant

## As classes de erro, de novo

`water_plant` lança o `PlantError` do exercício 3. Mas cada exercício é um programa independente,
na sua própria pasta, e o enunciado pede um arquivo por exercício. Importar do exercício 3 faria
o exercício 4 depender da pasta `ex3`, e o `import` nem a encontraria sem configuração extra,
porque ela não é a pasta do arquivo em execução. Por isso as classes são **copiadas** para o
arquivo:

```python
class GardenError(Exception):
    def __init__(self, message: str = "Unknown garden error") -> None:
        self.message = message

    def __str__(self) -> str:
        return self.message


class PlantError(GardenError):
    def __init__(self, message: str = "Unknown plant error") -> None:
        self.message = message
```

Só as duas que o exercício usa: `PlantError` e a mãe dela, `GardenError`, de onde vem o
`__str__`. A `WaterError` não é usada aqui.

## A função

```python
def water_plant(plant_name: str) -> None:
    if plant_name != plant_name.capitalize():
        raise PlantError(f"Invalid plant name to water: '{plant_name}'")
    print(f"Watering {plant_name}: [OK]")
```

1. Se o nome **não** é igual à sua versão capitalizada (`!=`), a função lança `PlantError` com a
   mensagem da saída esperada: `Invalid plant name to water: 'lettuce'` ("nome de planta inválido
   para regar").
2. Se o nome passou, ela "rega": imprime `Watering Tomato: [OK]`.

O `raise` vem antes do `print`, então um nome inválido nunca aparece como regado. A função não
captura o próprio erro: quem decide o que fazer é a função de teste, como nos exercícios
anteriores.
