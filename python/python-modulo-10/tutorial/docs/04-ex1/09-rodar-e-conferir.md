---
sidebar_position: 9
title: Rodar e conferir
---

# Rodar e conferir

## A saída inteira

```bash
python3 ex1/higher_magic.py
```

```text

Testing spell combiner...
Combined spell result: Fireball hits Dragon, Heals Dragon

Testing power amplifier...
Original: 10, Amplified: 30

Testing conditional caster...
Power 20: Fireball hits Goblin
Power 5: Spell fizzled

Testing spell sequence...
Sequence result: ['Fireball hits Wizard', 'Heals Wizard', '36']
```

## Comparar com o enunciado

O exemplo do enunciado tem seis linhas, contando a linha vazia do começo. O `head -n 6` deixa
passar só as seis primeiras linhas da saída, e o `diff` as compara com o exemplo:

```bash
diff <(python3 ex1/higher_magic.py | head -n 6) - <<'FIM'

Testing spell combiner...
Combined spell result: Fireball hits Dragon, Heals Dragon

Testing power amplifier...
Original: 10, Amplified: 30
FIM
```

O `|` liga a saída do programa à entrada do `head`. Sem nenhuma linha impressa, o começo da saída
é igual ao exemplo ([o diff explicado](../03-ex0/07-rodar-e-conferir.md#comparar-com-o-enunciado)).

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex1
.venv/bin/mypy --disallow-untyped-defs ex1
```

```text
Success: no issues found in 1 source file
```

## Um argumento que não é função

```bash
PYTHONPATH=ex1 python3 -B - <<'FIM'
from higher_magic import fireball, spell_combiner, spell_sequence
try:
    spell_combiner(fireball, "heal")
except TypeError as error:
    print(f"TypeError: {error}")
try:
    spell_sequence([fireball, 42])
except TypeError as error:
    print(f"TypeError: {error}")
FIM
```

```text
TypeError: spell_combiner needs two callable spells
TypeError: spell_sequence needs a list of callable spells
```

O texto `"heal"` e o número `42` são recusados na hora de criar o feitiço, antes de qualquer
lançamento. `PYTHONPATH`, `-B` e o `-` com `<<'FIM'` estão explicados em
[Rodar e conferir do exercício 0](../03-ex0/07-rodar-e-conferir.md#as-outras-duas-funções).

## Com dados do gerador

O gerador dá, para o exercício 1, três poderes (`test_values`) e quatro alvos (`test_targets`). As
duas linhas abaixo foram coladas de uma execução dele. O teste monta um feitiço com três funções
do exercício encaixadas: uma sequência que cura qualquer alvo menos dragões e lança um
`power_echo` com o dobro do poder.

```bash
PYTHONPATH=ex1 python3 -B - <<'FIM'
from higher_magic import conditional_caster, heal, power_amplifier, power_echo, spell_sequence
test_values = [5, 15, 14]
test_targets = ['Dragon', 'Goblin', 'Wizard', 'Knight']
not_on_dragons = conditional_caster(lambda target, power: target != "Dragon", heal)
combo = spell_sequence([not_on_dragons, power_amplifier(power_echo, 2)])
for target, power in zip(test_targets, test_values):
    print(target, power, combo(target, power))
ultra_echo = power_amplifier(power_amplifier(power_echo, 2), 3)
print(ultra_echo("Knight", 5))
FIM
```

```text
Dragon 5 ['Spell fizzled', '10']
Goblin 15 ['Heals Goblin', '30']
Wizard 14 ['Heals Wizard', '28']
30
```

- `zip(test_targets, test_values)` é uma função embutida que anda nas duas listas ao mesmo tempo
  e entrega os pares `(alvo, poder)`: `('Dragon', 5)`, `('Goblin', 15)`, `('Wizard', 14)`. Ela
  para na lista mais curta, e por isso o `Knight` fica de fora;
- a condição é uma lambda: o dragão faz o feitiço falhar, os outros alvos são curados;
- `ultra_echo` amplifica um feitiço já amplificado: 5 × 2 × 3 = 30.

Com os dados de outra execução do gerador, os poderes mudam, e a sequência continua devolvendo uma
lista com um resultado por feitiço.
