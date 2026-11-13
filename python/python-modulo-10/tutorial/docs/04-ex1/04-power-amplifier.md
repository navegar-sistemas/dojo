---
sidebar_position: 4
title: power_amplifier
---

# power_amplifier

`power_amplifier` cria a versão mais forte de um feitiço: o feitiço novo tem a mesma assinatura
do original e multiplica o poder antes de lançá-lo. A função entra depois de `spell_combiner`:

```python
def power_amplifier(base_spell: Callable, multiplier: int) -> Callable:
    if not callable(base_spell):
        raise TypeError("power_amplifier needs a callable spell")

    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplified
```

- a conferência com `callable()` é a mesma de `spell_combiner`;
- `amplified` recebe `(target, power)`, como o original, e lança `base_spell` com
  `power * multiplier`. O alvo passa sem mudança;
- `amplified` lembra `base_spell` e `multiplier` por closure.

Com `mega_echo = power_amplifier(power_echo, 3)`, a chamada `mega_echo("Dragon", 10)` vira
`power_echo("Dragon", 30)`, que devolve `"30"`. É a linha `Original: 10, Amplified: 30` da saída.

Como o feitiço amplificado tem a assinatura de um feitiço, ele pode ser amplificado de novo, ou
entrar em qualquer outra função do exercício: `power_amplifier(power_amplifier(power_echo, 2), 3)`
multiplica o poder por 6 ([Rodar e conferir](./09-rodar-e-conferir.md)). Essa é a
**composição**: funções pequenas que se encaixam umas nas outras porque seguem o mesmo contrato.
