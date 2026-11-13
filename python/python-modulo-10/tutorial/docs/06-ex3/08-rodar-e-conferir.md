---
sidebar_position: 8
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 ex3/functools_artifacts.py) - <<'FIM'

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
FIM
```

Sem nenhuma linha impressa, a saída é a esperada, inclusive a linha vazia do começo
([o diff explicado](../03-ex0/07-rodar-e-conferir.md#comparar-com-o-enunciado)).

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex3
.venv/bin/mypy --disallow-untyped-defs ex3
```

```text
Success: no issues found in 1 source file
```

## spell_reducer

A operação `"min"`, a lista vazia, a lista de um item só e uma operação desconhecida
(`PYTHONPATH`, `-B` e o `-` com `<<'FIM'` estão explicados em
[Rodar e conferir do exercício 0](../03-ex0/07-rodar-e-conferir.md#as-outras-duas-funções)):

```bash
PYTHONPATH=ex3 python3 -B - <<'FIM'
from functools_artifacts import spell_reducer
print(spell_reducer([10, 20, 30, 40], "min"))
print(spell_reducer([], "add"))
print(spell_reducer([7], "multiply"))
try:
    spell_reducer([1, 2], "divide")
except ValueError as error:
    print(f"ValueError: {error}")
FIM
```

```text
10
0
7
ValueError: Unknown operation: divide
```

Com um item só, o `reduce` devolve o próprio item. A operação `"divide"` não existe: a função
lança `ValueError`, e o `except` de quem chamou trata o erro.

## partial_enchanter

O teste escreve uma função de encantamento com a assinatura do enunciado,
`(power, element, target)`, e lança as três versões criadas contra o mesmo alvo:

```bash
PYTHONPATH=ex3 python3 -B - <<'FIM'
from functools_artifacts import partial_enchanter


def enchant(power: int, element: str, target: str) -> str:
    return f"{element} enchantment on {target} with {power} power"


enchanters = partial_enchanter(enchant)
for name, enchanter in enchanters.items():
    print(f"{name}: {enchanter('Sword')}")
FIM
```

```text
fire: fire enchantment on Sword with 50 power
ice: ice enchantment on Sword with 50 power
lightning: lightning enchantment on Sword with 50 power
```

Cada versão recebeu só o alvo; o poder 50 e o elemento já estavam preenchidos.

## O cache

```bash
PYTHONPATH=ex3 python3 -B - <<'FIM'
from functools_artifacts import memoized_fibonacci
print(memoized_fibonacci(15), memoized_fibonacci.cache_info())
print(memoized_fibonacci(15), memoized_fibonacci.cache_info())
print(memoized_fibonacci(16), memoized_fibonacci.cache_info())
try:
    memoized_fibonacci(-1)
except ValueError as error:
    print(f"ValueError: {error}")
FIM
```

```text
610 CacheInfo(hits=13, misses=16, maxsize=None, currsize=16)
610 CacheInfo(hits=14, misses=16, maxsize=None, currsize=16)
987 CacheInfo(hits=16, misses=17, maxsize=None, currsize=17)
ValueError: Fibonacci is not defined for negative numbers
```

- a primeira chamada calcula `Fib(0)` a `Fib(15)` uma vez cada: 16 faltas (`misses`);
- a mesma chamada de novo é só um acerto (`hits` vai de 13 a 14), sem cálculo;
- `Fib(16)` calcula um valor novo (uma falta) e acha `Fib(15)` e `Fib(14)` no cache (dois
  acertos);
- o `n` negativo é recusado com `ValueError`.

## O limite da recursão

```bash
PYTHONPATH=ex3 python3 -B - <<'FIM'
from functools_artifacts import memoized_fibonacci
try:
    memoized_fibonacci(1000)
except RecursionError as error:
    print(f"RecursionError: {error}")
for n in range(100, 1001, 100):
    memoized_fibonacci(n)
print(len(str(memoized_fibonacci(1000))))
FIM
```

```text
RecursionError: maximum recursion depth exceeded
209
```

Com o cache vazio, `Fib(1000)` estoura o limite de recursão
([O limite da recursão](./04-memoized-fibonacci.md#o-limite-da-recursão)). O `for` chama a função
com 100, 200, ..., 1000 (`range(100, 1001, 100)` conta de 100 em 100 até 1000): cada chamada só
desce os 100 níveis que ainda não estão no cache, e todas funcionam. `Fib(1000)` tem 209
algarismos (`len(str(...))` conta os caracteres do número escrito).

## spell_dispatcher

```bash
PYTHONPATH=ex3 python3 -B - <<'FIM'
from functools_artifacts import spell_dispatcher
dispatcher = spell_dispatcher()
print(dispatcher([]))
print(dispatcher({"fire": 1}))
print(dispatcher(True))
print(list(dispatcher.registry))
FIM
```

```text
Multi-cast: 0 spells
Unknown spell type
Damage spell: True damage
[<class 'object'>, <class 'int'>, <class 'str'>, <class 'list'>]
```

- a lista vazia é uma lista: `Multi-cast: 0 spells`;
- um dicionário não tem versão registrada e cai na função base;
- `True` é um `bool`, filho de `int`, e cai na versão de `int`
  ([Como o despacho escolhe](./05-spell-dispatcher.md#como-o-despacho-escolhe)). O tutorial
  mantém esse comportamento, que é o do `singledispatch`; para recusar `bool`, bastaria registrar
  mais uma versão, com `spell: bool`;
- `registry` é o dicionário dos tipos registrados: `object` é a função base (todo tipo é filho de
  `object`), e os outros três são os registros.

## Com dados do gerador

As três linhas de dados foram coladas de uma execução do gerador:

```bash
PYTHONPATH=ex3 python3 -B - <<'FIM'
from functools_artifacts import memoized_fibonacci, spell_reducer
spell_powers = [17, 49, 12, 30, 21, 18]
operations = ['add', 'multiply', 'max', 'min']
fibonacci_tests = [13, 15, 11]
for operation in operations:
    print(operation, spell_reducer(spell_powers, operation))
for n in fibonacci_tests:
    print(n, memoized_fibonacci(n))
print(memoized_fibonacci.cache_info())
FIM
```

```text
add 147
multiply 113354640
max 49
min 12
13 233
15 610
11 89
CacheInfo(hits=15, misses=16, maxsize=None, currsize=16)
```

Os três valores de Fibonacci custaram 16 cálculos ao todo: `Fib(13)` calculou de 0 a 13, `Fib(15)`
só acrescentou 14 e 15, e `Fib(11)` veio inteiro do cache.
