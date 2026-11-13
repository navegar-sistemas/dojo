---
sidebar_position: 5
title: Rodar e conferir
---

# Rodar e conferir

## Rodar

```bash
(cd ex6 && python3 ft_data_alchemist.py)
```

```text
=== Game Data Alchemist ===

Initial list of players: ['Alice', 'bob', 'Charlie', 'dylan', 'Emma', 'Gregory', 'john', 'kevin', 'Liam']
New list with all names capitalized: ['Alice', 'Bob', 'Charlie', 'Dylan', 'Emma', 'Gregory', 'John', 'Kevin', 'Liam']
New list of capitalized names only: ['Alice', 'Charlie', 'Emma', 'Gregory', 'Liam']

Score dict: {'Alice': 875, 'Bob': 700, 'Charlie': 580, 'Dylan': 659, 'Emma': 924, 'Gregory': 455, 'John': 207, 'Kevin': 558, 'Liam': 554}
Score average is 612.44
High scores: {'Alice': 875, 'Bob': 700, 'Dylan': 659, 'Emma': 924}
```

As quatro primeiras linhas depois do título são sempre iguais às do enunciado. As pontuações
mudam a cada execução.

## Conferir as contas

Nesta execução, a soma é 875 + 700 + 580 + 659 + 924 + 455 + 207 + 558 + 554 = 5512, e
5512 / 9 = 612.444…, que arredonda para `612.44`. Os jogadores acima disso são Alice (875), Bob
(700), Dylan (659) e Emma (924), exatamente os de `High scores`. Charlie, com 580, fica abaixo e
de fora.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex6
.venv/bin/mypy --disallow-untyped-defs ex6
```

```text
Success: no issues found in 1 source file
```
