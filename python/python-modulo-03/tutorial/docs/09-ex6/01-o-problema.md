---
sidebar_position: 1
title: O problema
---

# O problema

Muito do trabalho com dados é transformar uma coleção em outra: corrigir todos os nomes de uma
lista, ficar só com os que passam num teste, montar uma tabela a partir de uma lista. Com um
laço, cada transformação ocupa três ou quatro linhas. As **comprehensions** fazem o mesmo numa
linha só, dizendo o que entra na coleção nova.

## O que o enunciado pede

Um arquivo `ex6/ft_data_alchemist.py`, que pode usar `import random`, qualquer função de
`random`, `print()`, `len()`, `sum()` e `round()`.

1. Uma lista de nomes de jogadores, alguns começando com maiúscula e outros não.
2. Duas *list comprehensions*: uma cria uma lista nova com **todos** os nomes com a inicial
   maiúscula; a outra cria uma lista nova **só com os nomes que já começavam** com maiúscula.
3. Uma *dict comprehension* que cria um dicionário a partir da lista com todos os nomes
   corrigidos: cada nome é uma chave, e o valor é uma pontuação sorteada num intervalo.
4. Outra *dict comprehension* com só as pontuações acima da média.

O enunciado lembra que cada comprehension deve caber numa linha, a menos que passe dos 79
caracteres que o flake8 aceita, e que também existem comprehensions de set.

## A saída esperada

As pontuações são sorteadas, e mudam a cada execução. O exemplo do enunciado:

```text
=== Game Data Alchemist ===

Initial list of players: ['Alice', 'bob', 'Charlie', 'dylan', 'Emma', 'Gregory', 'john', 'kevin', 'Liam']
New list with all names capitalized: ['Alice', 'Bob', 'Charlie', 'Dylan', 'Emma', 'Gregory', 'John', 'Kevin', 'Liam']
New list of capitalized names only: ['Alice', 'Charlie', 'Emma', 'Gregory', 'Liam']

Score dict: {'Alice': 263, 'Bob': 666, 'Charlie': 907, 'Dylan': 170, 'Emma': 568, 'Gregory': 446, 'John': 90, 'Kevin': 527, 'Liam': 54}
Score average is 410.11
High scores: {'Bob': 666, 'Charlie': 907, 'Emma': 568, 'Gregory': 446, 'Kevin': 527}
```

A média é a soma das nove pontuações dividida por nove, 3691 / 9 = 410.111…, mostrada com duas
casas. Os cinco jogadores com mais de 410.11 pontos formam o último dicionário.
