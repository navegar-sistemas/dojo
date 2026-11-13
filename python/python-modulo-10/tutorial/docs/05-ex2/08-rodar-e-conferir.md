---
sidebar_position: 8
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 ex2/scope_mysteries.py) - <<'FIM'
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
FIM
```

Sem nenhuma linha impressa, a saída é a esperada
([o diff explicado](../03-ex0/07-rodar-e-conferir.md#comparar-com-o-enunciado)).

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex2
.venv/bin/mypy --disallow-untyped-defs ex2
```

```text
Success: no issues found in 1 source file
```

## Estado independente e privado

```bash
PYTHONPATH=ex2 python3 -B - <<'FIM'
from scope_mysteries import mage_counter, memory_vault, spell_accumulator
first = memory_vault()
second = memory_vault()
first["store"]("secret", 42)
first["store"]("secret", 7)
print(first["recall"]("secret"), second["recall"]("secret"))
print(sorted(first))
print(first["recall"].__code__.co_freevars)
weak = spell_accumulator(10)
strong = spell_accumulator(100)
print(weak(5), strong(5), weak(5))
counter = mage_counter()
print(counter(), counter(), counter())
print(counter.__code__.co_freevars, counter.__closure__[0].cell_contents)
FIM
```

```text
7 Memory not found
['recall', 'store']
('memories',)
15 105 20
1 2 3
('count',) 3
```

- gravar de novo a mesma chave troca o valor: `first` devolve 7. O segundo cofre não sabe de
  nada: tem o seu próprio dicionário;
- o cofre só tem as duas chaves, `recall` e `store` (`sorted` lista as chaves de um dicionário em
  ordem alfabética); o dicionário das memórias está na closure, na variável livre `memories`;
- os dois acumuladores andam separados: `weak` vai de 10 para 15 e 20, sem ser afetado pelo
  `strong`;
- depois de três chamadas, a célula do contador guarda 3. O `[0]` pega a primeira célula da
  tupla `__closure__` (aqui não há o `or ()` de [Escopo e closures](../02-conceitos/04-escopo-e-closures.md#nonlocal),
  porque este teste não passa pelo mypy).

## Com dados do gerador

As quatro linhas de dados foram coladas de uma execução do gerador:

```bash
PYTHONPATH=ex2 python3 -B - <<'FIM'
from scope_mysteries import enchantment_factory, spell_accumulator
initial_powers = [75, 72, 80]
power_additions = [19, 10, 6, 13, 13]
enchantment_types = ['Earthen', 'Shocking', 'Flaming']
items_to_enchant = ['Staff', 'Shield', 'Cloak', 'Amulet']
accumulate = spell_accumulator(initial_powers[0])
print(list(map(accumulate, power_additions)))
enchanters = list(map(enchantment_factory, enchantment_types))
for enchant, item in zip(enchanters, items_to_enchant):
    print(enchant(item))
FIM
```

```text
[94, 104, 110, 123, 136]
Earthen Staff
Shocking Shield
Flaming Cloak
```

- `map(accumulate, power_additions)` chama o acumulador com cada acréscimo, em ordem: 75 + 19 =
  94, + 10 = 104, e assim por diante. A lista mostra o total depois de cada chamada;
- `map(enchantment_factory, enchantment_types)` chama a **fábrica** com cada tipo e devolve três
  funções de encantamento; `map` aceita qualquer função, inclusive uma que devolve funções;
- `zip` junta cada encantamento com um item e para na lista mais curta (três encantamentos), por
  isso o `Amulet` fica de fora.
