---
sidebar_position: 2
title: As quatro coleções
---

# As quatro coleções

Cada coleção do Python guarda vários valores, mas cada uma do seu jeito. Escolher a certa depende
de três perguntas: a ordem dos elementos importa? Os valores podem mudar depois? Pode haver
repetidos? Este experimento cria uma de cada:

```python title="experimentos/quatro.py"
scores = [1500, 2300, 1500]
position = (1.0, 2.5, 3.0)
levels = {10, 20, 33, 10}
inventory = {"sword": 1, "potion": 5}
print(scores)
print(position)
print(levels)
print(inventory)
```

```bash
python3 experimentos/quatro.py
```

```text
[1500, 2300, 1500]
(1.0, 2.5, 3.0)
{33, 10, 20}
{'sword': 1, 'potion': 5}
```

- **lista** (`list`), entre colchetes `[]`: guarda os elementos na ordem em que foram postos,
  aceita repetidos (o `1500` aparece duas vezes) e pode mudar depois de criada;
- **tupla** (`tuple`), entre parênteses `()`: também guarda a ordem e aceita repetidos, mas
  **não muda** depois de criada;
- **set** (`set`, "conjunto"), entre chaves `{}`: guarda cada valor **uma vez só** (o segundo
  `10` sumiu) e **não guarda a ordem** (o `33` saiu primeiro, fora da ordem da escrita e fora da
  ordem crescente);
- **dicionário** (`dict`), entre chaves com pares `chave: valor`: associa cada **chave**
  (`"sword"`) a um **valor** (`1`), como um verbete associado à sua definição.

## Lado a lado

| | lista | tupla | set | dicionário |
|---|---|---|---|---|
| exemplo | `[1500, 2300]` | `(1.0, 2.5, 3.0)` | `{"Survivor", "Legend"}` | `{"sword": 1}` |
| vazio | `[]` | `()` | `set()` | `{}` |
| guarda a ordem | sim | sim | não | sim, a ordem em que as chaves entraram |
| acesso | pela posição: `scores[0]` | pela posição: `position[0]` | só `in` e `for` | pela chave: `inventory["sword"]` |
| muda depois de criada | sim | não | sim | sim |
| aceita repetidos | sim | sim | não | chaves não; valores sim |
| exercícios | 0 e 1 | 2 | 3 | 4 |

Duas palavras da tabela aparecem no projeto inteiro:

- **mutável** é a coleção que pode mudar depois de criada: ganhar, perder ou trocar elementos.
  Lista, set e dicionário são mutáveis;
- **imutável** é a que nunca muda. A tupla é imutável, e também `int`, `float` e `str`: uma
  operação sobre um texto, como `"bob".capitalize()`, devolve um texto **novo** e deixa o
  original como estava.

O vazio do set é `set()`, e não `{}`, porque as chaves vazias já eram o dicionário vazio antes
de o set existir no Python. O [exercício 3](../06-ex3/02-sets.md) volta a esse detalhe.

Os elementos de um set e as chaves de um dicionário precisam ser **imutáveis**, por inteiro: uma
tupla que contém uma lista ou um set não serve. O motivo é o mesmo que torna o set e o dicionário
rápidos ([A estrutura e o algoritmo](./03-a-estrutura-e-o-algoritmo.md)).
