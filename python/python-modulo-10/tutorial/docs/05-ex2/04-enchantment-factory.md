---
sidebar_position: 4
title: enchantment_factory
---

# enchantment_factory

A fábrica de encantamentos não guarda um estado que muda: cada função criada lembra um valor fixo,
o tipo de encantamento, e o aplica a qualquer item. A função entra depois de
`spell_accumulator`:

```python
def enchantment_factory(enchantment_type: str) -> Callable:
    def enchant(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return enchant
```

- `enchant` recebe o nome do item e devolve `"tipo item"`, no formato do enunciado:
  `enchantment_factory("Flaming")("Sword")` dá `"Flaming Sword"`;
- `enchant` só **lê** `enchantment_type`, sem atribuir nada a ele: o nome é achado no escopo
  envolvente, e não há `nonlocal`;
- o `def enchant` é a primeira linha do corpo, e por isso não precisa de linha em branco antes.

Cada chamada da fábrica cria uma função nova, com o seu próprio `enchantment_type`:

| Função criada | `enchantment_type` lembrado | `função("Sword")` |
|---|---|---|
| `enchantment_factory("Flaming")` | `"Flaming"` | `Flaming Sword` |
| `enchantment_factory("Frozen")` | `"Frozen"` | `Frozen Sword` |

É o mesmo desenho de `make_multiplier`, de
[Funções que devolvem funções](../02-conceitos/03-funcoes-que-devolvem-funcoes.md).
