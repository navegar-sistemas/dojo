---
sidebar_position: 5
title: O arquivo completo
---

# O arquivo completo

As funções `parse_inventory`, `show_percentages` e `show_extremes` estão prontas. O `main` as
chama na ordem da saída do enunciado e, no fim, acrescenta o item novo.

## O main

```python
def main() -> None:
    """Fill the inventory from the command line and analyse it."""
    print("=== Inventory System Analysis ===")
    inventory = parse_inventory(sys.argv[1:])
    print(f"Got inventory: {inventory}")
    print(f"Item list: {list(inventory.keys())}")
    total = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {total}")
    if total > 0:
        show_percentages(inventory, total)
    if len(inventory) > 0:
        show_extremes(inventory)
    if "magic_item" in inventory:
        inventory.update({"magic_item": inventory["magic_item"] + 1})
    else:
        inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")
```

- `{inventory}` imprime o dicionário com chaves, aspas e dois-pontos, como no enunciado;
- as porcentagens dependem do total ser maior que zero, e o mais e o menos abundante dependem de
  haver pelo menos um item. Com o inventário vazio, as duas partes são puladas, e o resto roda
  normalmente;
- `update({"magic_item": 1})` acrescenta o item novo no fim, com quantidade 1. Uma chave aparece
  uma vez só, e um `update` com uma chave que já existe troca o valor dela: se a linha de comando
  trouxer um `magic_item`, o mesmo `update` substitui a quantidade digitada por 1. O enunciado não
  diz o que fazer quando o item já existe. A escolha deste projeto é somar 1 à quantidade que já
  estava lá, para não perder a quantidade digitada.

## O arquivo inteiro

```python title="ex4/ft_inventory_system.py"
import sys

MAX_QUANTITY = 2 ** 53


def printable(text: str) -> str:
    """Return the text, or a marker if it is not valid UTF-8."""
    try:
        text.encode()
    except UnicodeEncodeError:
        return "<not valid UTF-8>"
    return text


def parse_inventory(arguments: list[str]) -> dict[str, int]:
    """Build the inventory from 'name:quantity' arguments."""
    inventory: dict[str, int] = {}
    for argument in arguments:
        parts = argument.split(":")
        valid_text = printable(argument) == argument
        if len(parts) != 2 or parts[0] == "" or not valid_text:
            print(f"Error - invalid parameter '{printable(argument)}'")
            continue
        name = parts[0]
        if name in inventory:
            print(f"Redundant item '{name}' - discarding")
            continue
        try:
            quantity = int(parts[1])
        except ValueError as error:
            print(f"Quantity error for '{name}': {error}")
            continue
        if quantity < 0:
            print(f"Quantity error for '{name}': negative quantity {quantity}")
            continue
        if quantity > MAX_QUANTITY:
            print(f"Quantity error for '{name}': quantity above "
                  f"{MAX_QUANTITY}")
            continue
        inventory[name] = quantity
    return inventory


def show_percentages(inventory: dict[str, int], total: int) -> None:
    """Print the share of the total that each item represents."""
    for name in inventory:
        percentage = inventory[name] / total * 100
        print(f"Item {name} represents {round(percentage, 1)}%")


def show_extremes(inventory: dict[str, int]) -> None:
    """Print the most and the least abundant items; ties keep the first."""
    names = list(inventory.keys())
    most = names[0]
    least = names[0]
    for name in names:
        if inventory[name] > inventory[most]:
            most = name
        if inventory[name] < inventory[least]:
            least = name
    print(f"Item most abundant: {most} with quantity {inventory[most]}")
    print(f"Item least abundant: {least} with quantity {inventory[least]}")


def main() -> None:
    """Fill the inventory from the command line and analyse it."""
    print("=== Inventory System Analysis ===")
    inventory = parse_inventory(sys.argv[1:])
    print(f"Got inventory: {inventory}")
    print(f"Item list: {list(inventory.keys())}")
    total = sum(inventory.values())
    print(f"Total quantity of the {len(inventory)} items: {total}")
    if total > 0:
        show_percentages(inventory, total)
    if len(inventory) > 0:
        show_extremes(inventory)
    if "magic_item" in inventory:
        inventory.update({"magic_item": inventory["magic_item"] + 1})
    else:
        inventory.update({"magic_item": 1})
    print(f"Updated inventory: {inventory}")


if __name__ == "__main__":
    main()
```

Como no [exercício 0](../03-ex0/05-o-arquivo-completo.md), o arquivo termina com uma única quebra
de linha depois da última linha, `    main()`, que o botão de copiar não leva.

O arquivo traz a mesma função `printable` do
[exercício 0](../03-ex0/05-o-arquivo-completo.md#um-argumento-que-não-é-texto-válido), usada na
conferência do formato ([Ler os parâmetros](./03-ler-os-parametros.md#o-formato)), e a constante
`MAX_QUANTITY`, o teto das quantidades ([A quantidade](./03-ler-os-parametros.md#a-quantidade)).

Além das funções autorizadas, o arquivo usa `int()` e os métodos `split` e `encode` (dentro de
`printable`), liberados pela regra dos tipos. Do dicionário, usa só `keys`, `values` e `update`,
os colchetes e o `in`.
