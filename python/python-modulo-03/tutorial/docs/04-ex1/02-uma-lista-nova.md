---
sidebar_position: 2
title: Uma lista nova
---

# Uma lista nova

No exercício 0, a lista já existia: o Python a montou. Agora o programa constrói a sua, começando
vazia e acrescentando cada pontuação válida.

```python title="experimentos/lista_nova.py"
scores: list[int] = []
print(scores, len(scores))
scores.append(1500)
scores.append(2300)
print(scores, len(scores))
scores[0] = 1600
print(scores)
```

```bash
python3 experimentos/lista_nova.py
```

```text
[] 0
[1500, 2300] 2
[1600, 2300]
```

- `[]` cria uma lista vazia;
- `scores.append(1500)` acrescenta `1500` no **fim** da lista (*append* é "anexar"). `append` é
  um **método** da lista: uma função que pertence a ela e é chamada com ponto;
- `scores[0] = 1600` troca o elemento do índice 0.

`append` e a troca pelo índice **mudam a própria lista**; não criam uma nova. É isso que quer
dizer a lista ser **mutável**. A tupla, do [exercício 2](../05-ex2/02-tuplas.md), não aceita
nenhuma das duas operações.

## A anotação list[int]

`scores: list[int] = []` anota o tipo da variável: uma lista de inteiros. O tipo entre colchetes
é o tipo dos **elementos**. Sem a anotação, o mypy tenta deduzir o tipo pelo primeiro `append`
que vem depois; quando não há nenhum, ele exige a anotação. Escrevê-la deixa o tipo explícito
para quem lê, e o mypy acusa se o código tentar pôr um texto nessa lista.

O mesmo vale nos type hints das funções: `def parse_scores(arguments: list[str]) -> list[int]:`
recebe uma lista de textos e devolve uma lista de inteiros. Essa escrita, com o tipo da coleção
seguido dos colchetes, existe a partir do Python 3.9.
