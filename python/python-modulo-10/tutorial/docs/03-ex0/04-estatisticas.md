---
sidebar_position: 4
title: As estatísticas
---

# As estatísticas

`mage_stats` resume uma lista de magos em três números: o maior poder, o menor poder e a média.
A função entra depois de `spell_transformer`:

```python
def mage_stats(mages: list[dict]) -> dict:
    if not mages:
        return {"max_power": 0, "min_power": 0, "avg_power": 0.0}
    strongest = max(mages, key=lambda mage: mage["power"])
    weakest = min(mages, key=lambda mage: mage["power"])
    total = sum(map(lambda mage: mage["power"], mages))
    return {
        "max_power": strongest["power"],
        "min_power": weakest["power"],
        "avg_power": round(total / len(mages), 2),
    }
```

## Maior e menor

`max(mages, key=lambda mage: mage["power"])` compara os magos pelo poder e devolve o **mago**
inteiro de maior poder, não só o número. `strongest["power"]` lê o poder dele. `min` faz o mesmo
para o menor. É o uso de lambdas com `max` e `min` que o enunciado pede.

## A média

- `map(lambda mage: mage["power"], mages)` tira o poder de cada mago;
- `sum(...)` soma esses poderes;
- `total / len(mages)` divide pela quantidade de magos. A divisão com `/` sempre dá um `float`;
- `round(..., 2)` arredonda para duas casas decimais: `72.333...` vira `72.33`.

## A lista vazia

Sem magos, não há maior nem menor: `max` de uma lista vazia lança `ValueError`, e a média
dividiria por zero (`ZeroDivisionError`). O `if not mages:` (uma lista vazia conta como "falso"
num `if`) trata o caso antes: a função devolve zeros, `{"max_power": 0, "min_power": 0,
"avg_power": 0.0}`. O enunciado não diz o que fazer com a lista vazia; devolver zeros é escolha do
tutorial, no mesmo espírito da regra do exercício 3 para uma lista vazia de poderes ("devolva 0").
Outra opção seria lançar um `ValueError` com uma mensagem própria.

## O dicionário devolvido

O `return` monta o dicionário com as três chaves do enunciado, em várias linhas: dentro de
chaves, o Python aceita quebrar a linha, e a vírgula depois do último par é permitida.
