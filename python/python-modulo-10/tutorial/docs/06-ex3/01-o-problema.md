---
sidebar_position: 1
title: O problema
---

# O problema

Somar uma lista, criar versões pré-configuradas de uma função, não recalcular o que já foi
calculado, escolher o comportamento pelo tipo do dado: são problemas comuns, e o Python já traz
ferramentas prontas para eles no módulo **`functools`** ("ferramentas de funções"). O exercício 3
usa quatro delas, uma por função.

## O que o enunciado pede

Um arquivo `ex3/functools_artifacts.py`. Autorizados: os módulos `functools` e `operator`.

As quatro funções, com as assinaturas do enunciado:

```python
def spell_reducer(spells: list[int], operation: str) -> int
def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]
def memoized_fibonacci(n: int) -> int
def spell_dispatcher() -> Callable[[Any], str]
```

| Função | O que faz | Ferramenta |
|---|---|---|
| `spell_reducer(spells, operation)` | combina todos os poderes da lista numa operação: `"add"` (soma), `"multiply"` (produto), `"max"` (maior) ou `"min"` (menor), usando as funções do módulo `operator` (`add`, `mul`...). Lista vazia devolve 0; operação desconhecida é um erro a tratar | `functools.reduce` |
| `partial_enchanter(base_enchantment)` | recebe uma função de encantamento com a assinatura `(power: int, element: str, target: str) -> str` e cria três versões especializadas, cada uma com `power=50` e um elemento já preenchidos | `functools.partial` |
| `memoized_fibonacci(n)` | devolve o n-ésimo número de Fibonacci, com um cache que acelera as chamadas repetidas | `functools.lru_cache` |
| `spell_dispatcher()` | devolve uma função que reage ao tipo do argumento: `int` é um feitiço de dano, `str` um encantamento, `list` um lançamento múltiplo; qualquer outro tipo cai na função base, que trata o "tipo de feitiço desconhecido" | `functools.singledispatch` |

A **sequência de Fibonacci** começa com 0 e 1, e cada número seguinte é a soma dos dois
anteriores: 0, 1, 1, 2, 3, 5, 8, 13... O n-ésimo número conta a partir do 0: `Fib(0)` é 0,
`Fib(1)` é 1, `Fib(10)` é 55.

`Callable[[Any], str]`, no retorno de `spell_dispatcher`, é o type hint de "uma função que recebe
um argumento de qualquer tipo e devolve um `str`".

## A saída esperada

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

A saída começa com uma linha vazia, como no exercício 0. O exemplo usa os poderes 10, 20, 30 e 40
(soma 100, produto 240000, maior 40). Ele não mostra a operação `"min"` nem `partial_enchanter`;
os dois são testados em [Rodar e conferir](./08-rodar-e-conferir.md).

O enunciado avisa que dá para conferir o cache com `memoized_fibonacci.cache_info()`
([memoized_fibonacci](./04-memoized-fibonacci.md)).
