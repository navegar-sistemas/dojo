---
sidebar_position: 4
title: As estatísticas
---

# As estatísticas

Com a lista montada, cada estatística é uma função pronta do Python ou uma conta simples:

```python title="experimentos/estatisticas.py"
scores = [1500, 2300, 1800, 2100, 1950]
print(len(scores), sum(scores), max(scores), min(scores))
print(sum(scores) / len(scores))
print(10 / 4, 10 // 4)
try:
    max([])
except ValueError as error:
    print(f"ValueError: {error}")
```

```bash
python3 experimentos/estatisticas.py
```

```text
5 9650 2300 1500
1930.0
2.5 2
ValueError: max() iterable argument is empty
```

| Estatística | Linha da saída | Código |
|---|---|---|
| quantidade | `Total players` | `len(scores)` |
| total | `Total score` | `sum(scores)`, a soma dos elementos |
| média | `Average score` | `sum(scores) / len(scores)` |
| maior | `High score` | `max(scores)` |
| menor | `Low score` | `min(scores)` |
| amplitude | `Score range` | `max(scores) - min(scores)` |

## A média é um float

A barra `/` é a **divisão comum**, e o resultado é sempre um `float`, mesmo quando a conta é
exata: `9650 / 5` dá `1930.0`, e é esse `1930.0` que o enunciado mostra. A barra dupla `//` é a
divisão **inteira**, que arredonda o resultado para baixo: `10 // 4` dá `2`, e `-10 // 4` dá
`-3`. A média usa `/`.

## Lista vazia não tem maior nem menor

`max([])` lança `ValueError`: não existe maior elemento numa lista sem elementos. A média também
quebraria, com uma divisão por zero. Por isso as estatísticas só são calculadas depois de conferir
que a lista não está vazia.

## A função das estatísticas

```python
def show_stats(scores: list[int]) -> None:
    """Print the statistics of a non-empty list of scores."""
    total = sum(scores)
    high = max(scores)
    low = min(scores)
    print(f"Scores processed: {scores}")
    print(f"Total players: {len(scores)}")
    print(f"Total score: {total}")
    print(f"Average score: {total / len(scores)}")
    print(f"High score: {high}")
    print(f"Low score: {low}")
    print(f"Score range: {high - low}")
```

- `total`, `high` e `low` guardam os valores usados mais de uma vez, para não percorrer a lista de
  novo a cada uso;
- `{scores}` dentro da f-string imprime a lista inteira, com colchetes e vírgulas:
  `[1500, 2300, 1800, 2100, 1950]`, como no enunciado;
- a docstring diz que a lista não pode estar vazia: quem chama a função é quem confere isso.
