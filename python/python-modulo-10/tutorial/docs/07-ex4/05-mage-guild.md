---
sidebar_position: 5
title: MageGuild
---

# MageGuild

Conferir se um nome de mago é válido não depende de nenhuma guilda em particular: a regra é a
mesma para todas. Um método que não usa o objeto não precisa recebê-lo. O `@staticmethod` é o
decorador do Python para esse caso. A classe entra depois de `retry_spell`:

```python
class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and all(
            char.isalpha() or char == " " for char in name)

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"
```

## validate_mage_name: o método estático

`@staticmethod` faz o método não receber o `self`: ele é uma função comum guardada dentro da
classe. Pode ser chamado pela classe, sem criar objeto nenhum
(`MageGuild.validate_mage_name("Alex")`), ou por um objeto (`guild.validate_mage_name("Alex")`),
com o mesmo resultado.

A regra do enunciado: pelo menos 3 caracteres, e só letras e espaços.

- `len(name) >= 3` confere o tamanho;
- `char.isalpha() or char == " " for char in name` produz, para cada caractere, `True` se ele é
  uma letra (`isalpha()` é o método de `str` que responde se todos os caracteres são letras) ou um
  espaço;
- `all(...)` exige que todos sejam `True` ([A conferência de uma lista](../04-ex1/06-spell-sequence.md#a-conferência-de-uma-lista));
- o `and` só olha os caracteres quando o tamanho já passou.

`"Alex"` e `"Mage Lord"` são válidos; `"Jo"` (curto), `"Alex123"` (números) e `"Test@Name"`
(`@`) não são. `isalpha()` também aceita letras acentuadas, como `"José"`. Um nome só de espaços,
como `"   "`, passa na regra como o enunciado a escreve; recusá-lo seria uma regra a mais.

## cast_spell: o método de instância

`cast_spell` é um método comum: recebe o `self` (a guilda) como primeiro argumento. O
`@power_validator(min_power=10)` embrulha o método como embrulharia uma função solta: quando
`guild.cast_spell("Lightning", 15)` é chamado, o `wrapper` recebe `args = (guild, "Lightning", 15)`,
acha o poder no último argumento e decide:

| Chamada | Poder ≥ 10? | Resultado |
|---|---|---|
| `guild.cast_spell("Lightning", 15)` | sim | `Successfully cast Lightning with 15 power` |
| `guild.cast_spell("Fireball", 5)` | não | `Insufficient power for this spell` (o corpo do método nem roda) |

O corpo de `cast_spell` só cuida do caso válido; a recusa fica toda no decorador. Essa é a
**separação de responsabilidades**: a regra de poder mínimo é escrita uma vez, no decorador, e
vale para qualquer feitiço ou método que o use.

| | `@staticmethod` | método de instância |
|---|---|---|
| primeiro parâmetro | nenhum especial | `self`, o objeto |
| chamado por | a classe ou um objeto | um objeto |
| enxerga os atributos do objeto | não | sim, por `self` |
| no projeto | `validate_mage_name` | `cast_spell` |
