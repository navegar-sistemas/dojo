---
sidebar_position: 5
title: conditional_caster
---

# conditional_caster

`conditional_caster` cria um feitiço com uma trava: ele só é lançado se uma condição for
verdadeira; se não for, devolve `"Spell fizzled"`. A função entra depois de `power_amplifier`:

```python
def conditional_caster(condition: Callable, spell: Callable) -> Callable:
    if not callable(condition) or not callable(spell):
        raise TypeError("conditional_caster needs a callable condition "
                        "and a callable spell")

    def caster(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return caster
```

- a condição também é uma função, e também passa pela conferência com `callable()`. A mensagem
  de erro foi dividida em dois textos seguidos para caber em 79 caracteres; o Python os junta num
  só;
- `caster` chama `condition(target, power)` com os mesmos argumentos que vão para o feitiço, como
  o enunciado pede. A condição pode olhar o alvo, o poder ou os dois;
- se a condição dá verdadeiro, `caster` devolve o resultado do feitiço; se não, o `return` de
  dentro do `if` não acontece, e a função chega ao `return "Spell fizzled"`.

Com `careful_fireball = conditional_caster(is_strong, fireball)`:

| Chamada | `is_strong` | Resultado |
|---|---|---|
| `careful_fireball("Goblin", 20)` | `True` (20 ≥ 15) | `Fireball hits Goblin` |
| `careful_fireball("Goblin", 5)` | `False` | `Spell fizzled` |

A condição não precisa ser um `def`: qualquer função serve, inclusive uma lambda, como
`lambda target, power: target != "Dragon"` ("não lance em dragões"),
usada em [Rodar e conferir](./09-rodar-e-conferir.md).
