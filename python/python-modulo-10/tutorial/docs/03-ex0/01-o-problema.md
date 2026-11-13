---
sidebar_position: 1
title: O problema
---

# O problema

Ordenar uma lista de artefatos pelo poder, escolher os magos fortes o bastante, enfeitar nomes de
feitiços, achar o maior e o menor poder: são tarefas pequenas, e cada uma depende de uma regra
curta ("compare pelo poder", "o poder é pelo menos 70?"). O exercício 0 escreve cada regra como
uma **lambda**, passada direto para as funções embutidas que fazem o trabalho
([Lambda](../02-conceitos/02-lambda.md)).

## O que o enunciado pede

Um arquivo `ex0/lambda_spells.py`. Funções embutidas autorizadas: `map`, `filter`, `sorted`,
`min`, `max`, `round`, `sum` e `len`.

O exercício traz um aviso: **toda transformação usa lambda**, e o `def` não deve ser usado para
criar funções com nome para operações simples, como tarefas de uma vez só ou operações fáceis de
ler. Na prática: nada de `def get_power(mage)` para passar como `key`; a regra vai numa lambda no
próprio `sorted`, `max` ou `min`.

As quatro funções, com as assinaturas do enunciado:

```python
def artifact_sorter(artifacts: list[dict]) -> list[dict]
def power_filter(mages: list[dict], min_power: int) -> list[dict]
def spell_transformer(spells: list[str]) -> list[str]
def mage_stats(mages: list[dict]) -> dict
```

| Função | O que faz |
|---|---|
| `artifact_sorter(artifacts)` | devolve os artefatos ordenados pelo poder, do maior para o menor, com `sorted` e uma lambda |
| `power_filter(mages, min_power)` | devolve uma lista com os magos de poder maior ou igual a `min_power`, com `filter` e uma lambda |
| `spell_transformer(spells)` | devolve os nomes de feitiço com `"* "` antes e `" *"` depois, com `map` e uma lambda |
| `mage_stats(mages)` | devolve o maior poder, o menor poder e a média dos poderes (arredondada para 2 casas), usando lambdas com `max` e `min` |

Os dados são dicionários:

- um artefato: `{'name': str, 'power': int, 'type': str}`, como
  `{"name": "Fire Staff", "power": 92, "type": "weapon"}`;
- um mago: `{'name': str, 'power': int, 'element': str}`, como
  `{"name": "Alex", "power": 90, "element": "fire"}`;
- o resultado de `mage_stats`: `{'max_power': int, 'min_power': int, 'avg_power': float}`.

`list[dict]` é o type hint de "uma lista de dicionários"; `dict` sem colchetes aceita qualquer
chave e qualquer valor.

## A saída esperada

```text

Testing artifact sorter...
Fire Staff (92 power) comes before Crystal Orb (85 power)

Testing spell transformer...
* fireball * * heal * * shield *
```

A saída começa com uma linha vazia: no exemplo do enunciado há uma linha em branco entre o comando
e o primeiro `Testing`. O exemplo testa duas das quatro funções; as outras duas são testadas em
[Rodar e conferir](./07-rodar-e-conferir.md).

## O def do main

Além das quatro funções, o arquivo tem um `def main()` com a demonstração. Ele não é uma operação
simples nem uma transformação, e existe para que as variáveis da demonstração fiquem dentro de uma
função: escritas soltas no arquivo, seriam variáveis globais, que o enunciado proíbe. Essa é a
leitura do tutorial para o aviso sobre o `def`.
