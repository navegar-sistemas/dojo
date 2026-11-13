---
sidebar_position: 6
title: spell_sequence
---

# spell_sequence

`spell_sequence` transforma uma lista de feitiços num feitiço só, que lança todos em ordem, com os
mesmos argumentos, e devolve a lista dos resultados. A função entra depois de
`conditional_caster`:

```python
def spell_sequence(spells: list[Callable]) -> Callable:
    if not all(callable(spell) for spell in spells):
        raise TypeError("spell_sequence needs a list of callable spells")

    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]

    return sequence
```

## A conferência de uma lista

`callable(spell) for spell in spells` produz um `True` ou `False` para cada item da lista; é como
uma compreensão de lista sem os colchetes (uma **expressão geradora**), que entrega os valores um a
um. `all(...)` é uma função embutida que responde se **todos** os valores são verdadeiros: basta um
item que não pode ser chamado para dar `False`, e a função lança `TypeError`. Com a lista vazia,
`all` dá `True`, e o feitiço criado devolve uma lista vazia.

## O feitiço em sequência

`[spell(target, power) for spell in spells]` é uma compreensão de lista: para cada feitiço da
lista, na ordem, chama `spell(target, power)` e guarda o resultado. O tipo do retorno é
`list[str]`.

Na demonstração, a sequência mistura feitiços comuns com um feitiço criado por outra função do
exercício:

```python
combo = spell_sequence([fireball, heal, mega_echo])
```

`combo("Wizard", 12)` devolve `['Fireball hits Wizard', 'Heals Wizard', '36']`: o terceiro item é
o `power_echo` amplificado por 3, lançado com 12.

```mermaid
flowchart LR
    call["combo('Wizard', 12)"] --> f["fireball"] --> r1["'Fireball hits Wizard'"]
    call --> h["heal"] --> r2["'Heals Wizard'"]
    call --> m["mega_echo<br/>(power_echo com poder × 3)"] --> r3["'36'"]
    r1 --> lst["lista na ordem dos feitiços"]
    r2 --> lst
    r3 --> lst
```
