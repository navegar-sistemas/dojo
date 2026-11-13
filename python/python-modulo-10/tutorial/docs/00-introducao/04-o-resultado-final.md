---
sidebar_position: 4
title: O resultado final
---

# O resultado final

Esta é a saída de cada programa pronto. Os programas não recebem argumentos nem leem o teclado:
cada um roda uma demonstração fixa. Os comandos são rodados na pasta do projeto
([A pasta do projeto](../01-ambiente/02-a-pasta-do-projeto.md)) e só funcionam depois que os
arquivos existirem: a página "Rodar e conferir" de cada exercício os roda.

## Exercício 0

```bash
python3 ex0/lambda_spells.py
```

```text

Testing artifact sorter...
Fire Staff (92 power) comes before Crystal Orb (85 power)

Testing spell transformer...
* fireball * * heal * * shield *
```

A saída começa com uma linha vazia, como no exemplo do enunciado, que mostra uma linha em branco
entre o comando e o primeiro `Testing`. Os exercícios 1 e 3 também começam assim; o 2 e o 4, não.

## Exercício 1

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

O enunciado mostra só as seis primeiras linhas, como um exemplo curto, e pede que o programa
demonstre todas as funções. As duas últimas seções são do tutorial.

## Exercício 2

```bash
python3 ex2/scope_mysteries.py
```

```text
Testing mage counter...
counter_a call 1: 1
counter_a call 2: 2
counter_b call 1: 1

Testing spell accumulator...
Base 100, add 20: 120
Base 100, add 30: 150

Testing enchantment factory...
Flaming Sword
Frozen Shield

Testing memory vault...
Store 'secret' = 42
Recall 'secret': 42
Recall 'unknown': Memory not found
```

## Exercício 3

```bash
python3 ex3/functools_artifacts.py
```

```text

Testing spell reducer...
Sum: 100
Product: 240000
Max: 40

Testing memoized fibonacci...
Fib(0): 0
Fib(1): 1
Fib(10): 55
Fib(15): 610

Testing spell dispatcher...
Damage spell: 42 damage
Enchantment: fireball
Multi-cast: 3 spells
Unknown spell type
```

## Exercício 4

```bash
python3 ex4/decorator_mastery.py
```

```text
Testing spell timer...
Casting fireball...
Spell completed in 0.104 seconds
Result: Fireball cast!

Testing retrying spell...
Spell failed, retrying... (attempt 1/3)
Spell failed, retrying... (attempt 2/3)
Spell casting failed after 3 attempts
Waaaaaaagh spelled !

Testing MageGuild...
True
False
Successfully cast Lightning with 15 power
Insufficient power for this spell
```

A terceira linha muda a cada execução: é o tempo medido de um feitiço que espera 0,1 segundo, e
os milésimos variam com a máquina e com o momento (`0.100`, `0.101`, `0.104`...). O enunciado
mostra `0.101`. As outras linhas são sempre iguais.
