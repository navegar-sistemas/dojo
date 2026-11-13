---
sidebar_position: 1
title: O problema
---

# O problema

Num jogo de RPG, o inventário é a mochila do personagem: cada item com a sua quantidade, como
uma espada e cinco poções. O programa monta o inventário a partir da linha de comando, recusa o
que vier errado e faz as contas: total de itens, a parte de cada um, o mais e o menos abundante.

## O que o enunciado pede

Um arquivo `ex4/ft_inventory_system.py`, que pode usar `import sys`, `sys.argv`, `len()`,
`print()`, `sum()`, `list()`, `round()` e os métodos `keys()`, `values()` e `update()` do
dicionário.

Cada argumento tem o formato `<item_name>:<quantity>`: o nome do item, dois-pontos e a
quantidade, como `potion:5`. O programa:

- descarta, com uma mensagem, os argumentos com formato errado e os itens **repetidos**, e
  guarda os válidos num **dicionário**, com a quantidade convertida em `int`;
- mostra o inventário;
- cria e mostra a lista dos nomes dos itens;
- calcula e mostra a quantidade total;
- mostra a porcentagem que cada item representa no total;
- mostra o item mais abundante e o menos abundante; num empate, vale o que veio **primeiro** na
  linha de comando;
- acrescenta um item novo ao inventário e o mostra de novo.

## A saída esperada

```bash
(cd ex4 && python3 ft_inventory_system.py sword:1 potion:5 shield:2 armor:3 helmet:1 sword:2 hello key:value)
```

```text
=== Inventory System Analysis ===
Redundant item 'sword' - discarding
Error - invalid parameter 'hello'
Quantity error for 'key': invalid literal for int() with base 10: 'value'
Got inventory: {'sword': 1, 'potion': 5, 'shield': 2, 'armor': 3, 'helmet': 1}
Item list: ['sword', 'potion', 'shield', 'armor', 'helmet']
Total quantity of the 5 items: 12
Item sword represents 8.3%
Item potion represents 41.7%
Item shield represents 16.7%
Item armor represents 25.0%
Item helmet represents 8.3%
Item most abundant: potion with quantity 5
Item least abundant: sword with quantity 1
Updated inventory: {'sword': 1, 'potion': 5, 'shield': 2, 'armor': 3, 'helmet': 1, 'magic_item': 1}
```

Três argumentos foram recusados, cada um por um motivo:

| Argumento | Motivo | Mensagem |
|---|---|---|
| `sword:2` | `sword` já entrou antes, com `sword:1` | `Redundant item 'sword' - discarding` |
| `hello` | não tem o formato `nome:quantidade` | `Error - invalid parameter 'hello'` |
| `key:value` | a quantidade não é um número | `Quantity error for 'key': ...` com a mensagem do `int()` |

`sword` e `helmet` empatam como menos abundantes, com 1 cada. `sword` vem primeiro na linha de
comando, e é ele que aparece.

O enunciado termina com uma dica: "no começo do jogo, o seu inventário normalmente está vazio".
Rodado sem argumentos, o programa precisa funcionar com um inventário vazio, sem travar.
