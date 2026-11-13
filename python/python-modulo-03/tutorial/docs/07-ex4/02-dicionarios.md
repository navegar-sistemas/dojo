---
sidebar_position: 2
title: Dicionários
---

# Dicionários

Um inventário associa cada nome de item a uma quantidade. Com duas listas, uma de nomes e outra
de quantidades, seria preciso manter as duas sempre alinhadas e procurar a posição de um nome
para achar a quantidade. O **dicionário** (`dict`) guarda os pares juntos: cada **chave** (o nome
do item) aponta para um **valor** (a quantidade), e a busca pela chave é rápida, pelo hash
([A estrutura e o algoritmo](../02-colecoes/03-a-estrutura-e-o-algoritmo.md)).

![O dicionário do exemplo do enunciado como uma tabela de duas colunas: cada chave, sword, potion, shield, armor e helmet, aponta para a sua quantidade, 1, 5, 2, 3 e 1. Ao lado, uma barra por item com a porcentagem que ele representa no total de 12: 8.3, 41.7, 16.7, 25.0 e 8.3. Embaixo, as legendas: mais abundante, potion (5); menos abundante, sword (1), o primeiro do empate com helmet](/img/ex4/inventario.svg)

```python title="experimentos/dicionarios.py"
inventory = {"sword": 1, "potion": 5}
print(inventory["potion"], len(inventory))
inventory["shield"] = 2
inventory["sword"] = 3
print(inventory)
print("potion" in inventory, 5 in inventory)
for name in inventory:
    print(name, inventory[name])
print(inventory.keys())
print(list(inventory.keys()))
print(sum(inventory.values()))
inventory.update({"magic_item": 1})
print(inventory)
try:
    print(inventory["bow"])
except KeyError as error:
    print(f"KeyError: {error}")
```

```bash
python3 experimentos/dicionarios.py
```

```text
5 2
{'sword': 3, 'potion': 5, 'shield': 2}
True False
sword 3
potion 5
shield 2
dict_keys(['sword', 'potion', 'shield'])
['sword', 'potion', 'shield']
10
{'sword': 3, 'potion': 5, 'shield': 2, 'magic_item': 1}
KeyError: 'bow'
```

## Ler, acrescentar e trocar

- `{"sword": 1, "potion": 5}` cria um dicionário com dois pares; `len` conta os pares;
- `inventory["potion"]` lê o valor da chave `"potion"`: 5;
- `inventory["shield"] = 2` acrescenta um par, porque `"shield"` ainda não existia;
- `inventory["sword"] = 3` **troca** o valor de `"sword"`: uma chave aparece uma vez só, e
  atribuir a uma chave que já existe substitui o valor;
- ler uma chave que não existe lança `KeyError` ("erro de chave"), com a chave como mensagem.

## in e for olham as chaves

`"potion" in inventory` pergunta se `"potion"` é uma **chave**: `True`. `5 in inventory` é
`False`, mesmo existindo uma quantidade 5: o `in` não olha os valores. Do mesmo jeito,
`for name in inventory` percorre as chaves, e o valor de cada uma se lê com `inventory[name]`.

## A ordem é a de chegada

O dicionário guarda as chaves na ordem em que entraram: `sword`, `potion`, `shield`,
`magic_item`. Trocar o valor de uma chave não muda o lugar dela. Essa ordem é o que permite ao
exercício respeitar "o primeiro da linha de comando" no empate: os itens entram no dicionário na
ordem dos argumentos.

## Os três métodos autorizados

| Método | Devolve | No exercício |
|---|---|---|
| `inventory.keys()` | as chaves | `list(inventory.keys())` vira a lista de nomes de `Item list` |
| `inventory.values()` | os valores | `sum(inventory.values())` é o total |
| `inventory.update({...})` | nada; acrescenta ou troca os pares do dicionário dado | acrescenta o `magic_item` no fim |

`keys()` e `values()` não devolvem listas: devolvem uma **visão** (*view*) do dicionário,
impressa como `dict_keys([...])` ou `dict_values([...])`. Uma visão pode ser percorrida, e `sum`
soma uma visão de números, mas ela não é uma lista. Para mostrar `['sword', 'potion', 'shield']`,
como o enunciado, a visão das chaves é convertida com `list()`.

O dicionário tem outros métodos, como `items()`, que devolve os pares, e `get()`, que lê uma
chave sem lançar erro. Pela regra geral do enunciado, o dicionário, apresentado neste exercício,
pode ser usado com todos os seus métodos; a lista do exercício cita só `keys`, `values` e
`update`. O programa usa só esses três, os colchetes e o `in`.
