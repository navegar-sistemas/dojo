---
sidebar_position: 1
title: O problema
---

# O problema

Um contador, um acumulador de poder, um cofre de memórias: todos precisam guardar um estado que
dura de uma chamada para a outra. Sem variáveis globais, esse estado fica numa **closure**: cada
função criada carrega as próprias variáveis, invisíveis para o resto do programa
([Escopo e closures](../02-conceitos/04-escopo-e-closures.md)). O exercício 2 escreve quatro
fábricas de closures.

## O que o enunciado pede

Um arquivo `ex2/scope_mysteries.py`. Autorizado: a instrução `nonlocal`.

As quatro funções, com as assinaturas do enunciado:

```python
def mage_counter() -> Callable
def spell_accumulator(initial_power: int) -> Callable
def enchantment_factory(enchantment_type: str) -> Callable
def memory_vault() -> dict[str, Callable]
```

| Função | Devolve |
|---|---|
| `mage_counter()` | uma função que conta quantas vezes foi chamada: cada chamada devolve a contagem atual, começando em 1. A contagem persiste entre as chamadas, e dois contadores criados separadamente têm contagens independentes. Sem variáveis globais |
| `spell_accumulator(initial_power)` | uma função que acumula poder: começa em `initial_power`, cada chamada soma a quantidade recebida ao total e devolve o total novo |
| `enchantment_factory(enchantment_type)` | uma função que recebe o nome de um item e devolve o item encantado, no formato `"tipo item"`, como `"Flaming Sword"`. Cada fábrica cria funções com um tipo de encantamento diferente |
| `memory_vault()` | um dicionário com duas funções: `'store'` recebe `(chave, valor)` e guarda a memória; `'recall'` recebe a chave e devolve o valor guardado, ou `"Memory not found"`. A memória fica numa closure, privada |

`dict[str, Callable]` é o type hint de um dicionário com chaves de texto e funções como valores.

## A saída esperada

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

Aqui a saída não começa com linha vazia: no exemplo do enunciado, o primeiro `Testing` vem logo
depois do comando.

- `counter_b call 1: 1` mostra a independência: `counter_b` começa do 1, mesmo depois de duas
  chamadas de `counter_a`;
- `Base 100, add 30: 150` mostra o acúmulo: o acumulador começou em 100, recebeu 20 (120) e depois
  30, chegando a 150. O `Base 100` da mensagem é o valor inicial, que não muda.
