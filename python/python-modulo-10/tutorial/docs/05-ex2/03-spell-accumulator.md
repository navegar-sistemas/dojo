---
sidebar_position: 3
title: spell_accumulator
---

# spell_accumulator

O acumulador é um contador que começa num valor escolhido e soma uma quantidade variável a cada
chamada. A função entra depois de `mage_counter`:

```python
def spell_accumulator(initial_power: int) -> Callable:
    total = initial_power

    def accumulate(amount: int) -> int:
        nonlocal total
        total += amount
        return total

    return accumulate
```

- `total` começa com o valor de `initial_power`, a base do enunciado;
- `accumulate(amount)` soma `amount` ao total e devolve o total novo;
- `nonlocal total` é necessário pelo mesmo motivo do contador: `total += amount` é uma
  atribuição.

Com `accumulate = spell_accumulator(100)`:

| Chamada | `total` antes | `total` depois e devolvido |
|---|---|---|
| `accumulate(20)` | 100 | 120 |
| `accumulate(30)` | 120 | 150 |

O parâmetro `initial_power` também é uma variável de `spell_accumulator` e também ficaria na
closure se `accumulate` o usasse. A variável separada `total` deixa claro qual valor muda (o total)
e qual é só o ponto de partida (o poder inicial).
