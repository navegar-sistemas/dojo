---
sidebar_position: 3
title: Dict comprehension
---

# Dict comprehension

A mesma ideia monta um dicionário: entre chaves, um par `chave: valor` à esquerda e o `for` à
direita.

```python title="experimentos/dict_comprehension.py"
numbers = [1, 2, 3, 4, 5]
print({n: n * n for n in numbers})
print({n: n * n for n in numbers if n > 3})
print({n % 3 for n in numbers})
```

```bash
python3 experimentos/dict_comprehension.py
```

```text
{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
{4: 16, 5: 25}
{0, 1, 2}
```

- `{n: n * n for n in numbers}` cria um par para cada número: a chave é o número, o valor é o
  quadrado;
- o `if` filtra do mesmo jeito que na lista;
- sem os dois-pontos, a comprehension entre chaves cria um **set**: `{n % 3 for n in numbers}` são
  os restos da divisão por 3, sem repetição. É a comprehension de set que o enunciado menciona.

## As pontuações

```python
scores = {name: random.randint(0, 1000) for name in capitalized}
```

Cada nome da lista corrigida vira uma chave, com uma pontuação sorteada de 0 a 1000. A chamada a
`random.randint` acontece uma vez para cada nome, então cada jogador recebe o seu sorteio. O
enunciado deixa o intervalo por conta de quem faz; 0 a 1000 cobre as pontuações do exemplo dele.

## A média

```python
average = sum(scores.values()) / len(scores)
```

`sum(scores.values())` soma as pontuações, e `len(scores)` conta os jogadores. O enunciado mostra a
média com duas casas, e `round(average, 2)` arredonda **só na hora de imprimir**. A comparação da
próxima linha usa a média exata. Com a arredondada, a comparação poderia errar em geral, por
exemplo com pontuações decimais ou outra quantidade de jogadores: uma média exata de 409.996
arredonda para 410.0, e um jogador com 410 pontos está acima da média de verdade, mas não acima
de 410.0.

`round` devolve um número, e as casas finais iguais a zero não aparecem: uma média de 4509 / 9 =
501.0 sai `Score average is 501.0`, com uma casa só, como acontece com as distâncias do
[exercício 2](../05-ex2/05-a-distancia.md#quatro-casas-com-round).

## Acima da média

```python
high = {name: scores[name] for name in scores if scores[name] > average}
```

- `for name in scores` percorre as chaves do dicionário, os nomes;
- `scores[name]` é a pontuação do nome;
- o `if` deixa entrar só quem tem mais que a média.

O dicionário tem o método `items()`, que dá os pares direto
(`for name, score in scores.items()`), e ele também é permitido pela regra geral desde o
exercício 4. O programa usa só `values()` e lê cada valor com colchetes.

O novo dicionário mantém a ordem do original, porque a comprehension percorre `scores` na ordem
em que as chaves entraram.
