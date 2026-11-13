---
sidebar_position: 4
title: memoized_fibonacci
---

# memoized_fibonacci

A definição de Fibonacci é **recursiva**: `Fib(n)` é `Fib(n - 1) + Fib(n - 2)`, e uma função que
segue a definição chama a si mesma duas vezes. Escrita assim, ela recalcula os mesmos valores um
número enorme de vezes. A **memoização** resolve: cada resultado calculado é guardado num
**cache** (uma memória de resultados), e uma chamada repetida devolve o valor guardado em vez de
recalcular. `functools.lru_cache` é um decorador que faz isso com qualquer função.

## Quantas chamadas o cache economiza

Crie `experimentos/fibonacci.py`, com uma versão sem cache, que conta as próprias chamadas, e
outra com `lru_cache`:

```python title="experimentos/fibonacci.py"
from functools import lru_cache

calls = {"slow": 0}


def slow_fibonacci(n: int) -> int:
    calls["slow"] += 1
    if n < 2:
        return n
    return slow_fibonacci(n - 1) + slow_fibonacci(n - 2)


@lru_cache(maxsize=None)
def fast_fibonacci(n: int) -> int:
    if n < 2:
        return n
    return fast_fibonacci(n - 1) + fast_fibonacci(n - 2)


print(slow_fibonacci(20), calls["slow"])
print(fast_fibonacci(20), fast_fibonacci.cache_info())
print(fast_fibonacci(20), fast_fibonacci.cache_info())
print(fast_fibonacci(25), fast_fibonacci.cache_info())
```

O dicionário `calls`, no nível de cima do arquivo, é justamente o tipo de variável global que os
exercícios evitam; aqui ele só serve para contar as chamadas da versão sem cache.

```bash
python3 experimentos/fibonacci.py
```

```text
6765 21891
6765 CacheInfo(hits=18, misses=21, maxsize=None, currsize=21)
6765 CacheInfo(hits=19, misses=21, maxsize=None, currsize=21)
75025 CacheInfo(hits=25, misses=26, maxsize=None, currsize=26)
```

- **sem cache:** `slow_fibonacci(20)` dá 6765 e faz **21891** chamadas. `Fib(20)` chama `Fib(19)`
  e `Fib(18)`; `Fib(19)` chama `Fib(18)` de novo, e cada uma recalcula tudo abaixo dela. O número
  de chamadas cresce quase tão rápido quanto o próprio resultado;
- **com cache:** `cache_info()` mostra o que aconteceu. `misses` ("faltas") são as chamadas que
  não acharam o resultado no cache e calcularam: 21, uma para cada `n` de 0 a 20. `hits`
  ("acertos") são as que acharam o resultado pronto: 18. `currsize` é quantos resultados o cache
  guarda, e `maxsize` o limite;
- **repetir a chamada:** `fast_fibonacci(20)` de novo é um acerto só (`hits` passa a 19), sem
  nenhum cálculo;
- **um n maior:** `fast_fibonacci(25)` só calcula os valores novos, de 21 a 25 (`misses` passa a
  26); o resto vem do cache.

`lru_cache` vem de *least recently used* ("menos usado recentemente"): quando o cache enche, o
resultado usado há mais tempo é descartado. `maxsize` é o tamanho do cache, e `maxsize=None` tira
o limite: nada é descartado.

## A função

`memoized_fibonacci` entra depois de `partial_enchanter`:

```python
@functools.lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Fibonacci is not defined for negative numbers")
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)
```

- `@functools.lru_cache(maxsize=None)` decora a função: o nome `memoized_fibonacci` passa a ser
  um embrulho que consulta o cache antes de rodar o corpo. As chamadas recursivas, dentro do
  corpo, também passam pelo embrulho, e por isso também usam o cache;
- `Fib(0)` é 0 e `Fib(1)` é 1: o `if n < 2: return n` cobre os dois casos e para a recursão;
- um `n` negativo não tem número de Fibonacci. Sem a conferência, `n < 2` devolveria o próprio
  negativo, um resultado sem sentido; a função lança `ValueError` (escolha do tutorial, para
  proteger o resultado como o enunciado pede). Uma exceção não é guardada no cache;
- o embrulho do `lru_cache` acrescenta à função os métodos `cache_info()`, que o enunciado sugere
  para conferir o cache, e `cache_clear()`, que esvazia o cache.

## O limite da recursão

Cada chamada recursiva ocupa um lugar numa pilha de chamadas que o Python limita (cerca de mil
níveis). Com o cache vazio, `memoized_fibonacci(1000)` desceria mil níveis antes do primeiro
resultado, e o Python lança `RecursionError`; no Python 3.10, o limite chega antes (`n = 500` já
falha, `n = 400` funciona), porque lá o embrulho do cache também conta como um nível. Com o cache já preenchido até
perto do valor pedido, a chamada desce pouco e funciona
([Rodar e conferir](./08-rodar-e-conferir.md)). Os valores do enunciado, até 15, ficam muito longe
do limite.
