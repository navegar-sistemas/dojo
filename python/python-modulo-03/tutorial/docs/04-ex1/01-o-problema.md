---
sidebar_position: 1
title: O problema
---

# O problema

As pontuações de uma partida chegam pela linha de comando, uma por argumento. Quem digita pode
errar e mandar uma palavra no lugar de um número. O programa separa o que é número do que não é,
guarda os números numa lista própria e calcula estatísticas sobre ela.

![Os argumentos 1500, ab, 2300 e 1800 são filtrados: os três números entram na lista scores, nas posições 0 a 2, e ab é avisado com Invalid parameter e descartado. Embaixo, um gráfico de barras das três pontuações com linhas tracejadas na maior, 2300, na média, 1866.67, e na menor, 1500, e a amplitude de 800 entre a maior e a menor; quantidade 3, total 5600](/img/ex1/filtro.svg)

## O que o enunciado pede

Um arquivo `ex1/ft_score_analytics.py`, que pode usar `import sys`, `sys.argv`, `len()`,
`sum()`, `max()`, `min()` e `print()`. O programa:

- lê os argumentos da linha de comando;
- trata os erros: argumento que não é número e falta de argumentos, cada um com uma mensagem;
- cria uma **lista nova** com as pontuações válidas;
- calcula a quantidade, o total, a média, a maior, a menor e a **amplitude** (*range*), que é a
  maior menos a menor;
- se vierem argumentos válidos e inválidos misturados, descarta os inválidos e segue com os
  válidos; se não sobrar nenhum válido, mostra a mensagem de uso.

Os argumentos são textos, e a conversão para número usa `int()`, que não está na lista do
exercício. Ela é permitida pela regra geral do enunciado: `int`, `float` e `str` podem ser usados
com os seus construtores em qualquer exercício.

## A saída esperada

```text
=== Player Score Analytics ===
Scores processed: [1500, 2300, 1800, 2100, 1950]
Total players: 5
Total score: 9650
Average score: 1930.0
High score: 2300
Low score: 1500
Score range: 800
```

Sem argumentos:

```text
=== Player Score Analytics ===
No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...
```

Só com argumentos inválidos, `ab` e `ac`:

```text
=== Player Score Analytics ===
Invalid parameter: 'ab'
Invalid parameter: 'ac'
No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...
```

A **mensagem de uso** (*usage*) é o costume dos programas de linha de comando para dizer como
devem ser chamados: `<score1> <score2> ...` quer dizer "uma pontuação, outra, e quantas mais
quiser".
