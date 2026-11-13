---
sidebar_position: 6
title: Capturar pela base
---

# Capturar pela base

A regra da página [Os tipos embutidos](../02-excecoes/06-os-tipos-embutidos.md) vale para os
tipos novos: `except X` captura `X` **e todos os filhos de `X`**. Então:

| `except` | Captura `PlantError`? | Captura `WaterError`? |
|---|---|---|
| `except PlantError` | sim | não |
| `except WaterError` | não | sim |
| `except GardenError` | sim | sim |

É isso que o enunciado pede para demonstrar: capturar `GardenError` captura **todos** os erros do
jardim. Na prática, um trecho que só quer saber se "algo deu errado no jardim" captura a base;
um trecho que reage diferente a planta e a água captura cada filha.

## A ordem dos except importa

Com vários `except` num `try`, o Python roda **só o primeiro** que combina (página
[Vários except num try](../05-ex2/04-varios-except.md)). Se a base vier antes da filha, a
filha nunca é alcançada. Um experimento, `experimentos/ordem.py`:

```python
class GardenError(Exception):
    pass


class PlantError(GardenError):
    pass


try:
    raise PlantError("The tomato plant is wilting!")
except GardenError as error:
    print(f"First except: {error}")
except PlantError as error:
    print(f"Second except: {error}")
```

```bash
python3 experimentos/ordem.py
```

```text
First except: The tomato plant is wilting!
```

O `except GardenError` aceita a `PlantError` e o segundo `except` nunca roda. Quando os dois
aparecem juntos, a ordem certa é **do mais específico para o mais geral**: primeiro as filhas,
por último a base.
