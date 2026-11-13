---
sidebar_position: 4
title: As contas
---

# As contas

Com o inventário montado, faltam as linhas de análise da saída: o total, a porcentagem de cada
item e o item mais e o menos abundante.

## O total

`sum(inventory.values())` soma as quantidades: 1 + 5 + 2 + 3 + 1 = 12. A quantidade de itens
diferentes é `len(inventory)`, 5. Os dois aparecem na mesma linha:
`Total quantity of the 5 items: 12`.

## A porcentagem de cada item

A parte de um item é a quantidade dele dividida pelo total, vezes 100. O enunciado mostra uma
casa depois do ponto, e `round(..., 1)` arredonda:

| Item | Conta | `round(..., 1)` |
|---|---|---|
| sword | 1 / 12 × 100 = 8.333… | `8.3` |
| potion | 5 / 12 × 100 = 41.666… | `41.7` |
| shield | 2 / 12 × 100 = 16.666… | `16.7` |
| armor | 3 / 12 × 100 = 25.0 | `25.0` |
| helmet | 1 / 12 × 100 = 8.333… | `8.3` |

```python
def show_percentages(inventory: dict[str, int], total: int) -> None:
    """Print the share of the total that each item represents."""
    for name in inventory:
        percentage = inventory[name] / total * 100
        print(f"Item {name} represents {round(percentage, 1)}%")
```

A conta divide pelo total, e um total 0 faria a divisão lançar `ZeroDivisionError`. Isso
acontece com o inventário vazio, a dica do enunciado, e também quando todos os itens têm
quantidade 0. O `main` só chama esta função quando o total é maior que zero.

## O mais e o menos abundante

`max()` e `min()` não estão na lista deste exercício, e o resultado precisa do **nome** do item,
não só da quantidade. Um laço resolve: começa com o primeiro item como candidato aos dois títulos
e troca de candidato quando acha uma quantidade **estritamente** maior ou menor.

```python
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
```

O empate fica com o primeiro por causa de duas coisas juntas:

- o dicionário guarda os itens na ordem da linha de comando, e o laço os visita nessa ordem;
- a comparação é `<`, e não `<=`. Quando `helmet` (1) é comparado com o candidato `sword` (1),
  `1 < 1` é falso, e `sword` continua.

| Volta | Item | Candidato a mais abundante | Candidato a menos abundante |
|---|---|---|---|
| início | | sword (1) | sword (1) |
| 1 | sword (1) | sword | sword |
| 2 | potion (5) | **potion** | sword |
| 3 | shield (2) | potion | sword |
| 4 | armor (3) | potion | sword |
| 5 | helmet (1) | potion | sword: 1 não é menor que 1 |

`names[0]` lança `IndexError` numa lista vazia: esta função também só é chamada com o inventário
não vazio.
