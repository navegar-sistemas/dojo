---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(cd ex4 && python3 ft_inventory_system.py sword:1 potion:5 shield:2 armor:3 helmet:1 sword:2 hello key:value) - <<'FIM'
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
FIM
```

O `diff` não imprime nada.

## O inventário vazio

```bash
(cd ex4 && python3 ft_inventory_system.py)
```

```text
=== Inventory System Analysis ===
Got inventory: {}
Item list: []
Total quantity of the 0 items: 0
Updated inventory: {'magic_item': 1}
```

Sem itens, não há porcentagens nem mais e menos abundante, e o programa segue até o fim.

## Os casos de borda

Argumentos que testam cada regra de uma vez:

```bash
(cd ex4 && python3 ft_inventory_system.py arrow:0 potion:-3 :5 a:1:2 bow: arrow:4)
```

```text
=== Inventory System Analysis ===
Quantity error for 'potion': negative quantity -3
Error - invalid parameter ':5'
Error - invalid parameter 'a:1:2'
Quantity error for 'bow': invalid literal for int() with base 10: ''
Redundant item 'arrow' - discarding
Got inventory: {'arrow': 0}
Item list: ['arrow']
Total quantity of the 1 items: 0
Item most abundant: arrow with quantity 0
Item least abundant: arrow with quantity 0
Updated inventory: {'arrow': 0, 'magic_item': 1}
```

- `arrow:0` entra, com quantidade 0, e o `arrow:4` do fim é recusado como repetido;
- `potion:-3` é recusado pela quantidade negativa, e `bow:`, pela quantidade vazia;
- `:5` e `a:1:2` não têm o formato;
- o total é 0, e as porcentagens são puladas sem divisão por zero.

## Um magic_item que já existe

```bash
(cd ex4 && python3 ft_inventory_system.py magic_item:7 sword:1)
```

```text
=== Inventory System Analysis ===
Got inventory: {'magic_item': 7, 'sword': 1}
Item list: ['magic_item', 'sword']
Total quantity of the 2 items: 8
Item magic_item represents 87.5%
Item sword represents 12.5%
Item most abundant: magic_item with quantity 7
Item least abundant: sword with quantity 1
Updated inventory: {'magic_item': 8, 'sword': 1}
```

O item novo soma 1 aos 7 que já estavam no inventário.

## Um argumento que não é UTF-8

```bash
(cd ex4 && python3 ft_inventory_system.py sword:1 $'\xff':3 potion:2)
```

```text
=== Inventory System Analysis ===
Error - invalid parameter '<not valid UTF-8>'
Got inventory: {'sword': 1, 'potion': 2}
Item list: ['sword', 'potion']
Total quantity of the 2 items: 3
Item sword represents 33.3%
Item potion represents 66.7%
Item most abundant: potion with quantity 2
Item least abundant: sword with quantity 1
Updated inventory: {'sword': 1, 'potion': 2, 'magic_item': 1}
```

O argumento com o byte `\xff` no nome não entra no inventário, e o resto segue.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex4
.venv/bin/mypy --disallow-untyped-defs ex4
```

```text
Success: no issues found in 1 source file
```
