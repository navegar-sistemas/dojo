---
sidebar_position: 1
title: Conferir tudo
---

# Conferir tudo

Antes de entregar, os sete exercícios passam pelas mesmas conferências, de uma vez.

## Estilo e tipos

```bash
.venv/bin/flake8 ex0 ex1 ex2 ex3 ex4 ex5 ex6
.venv/bin/mypy --disallow-untyped-defs ex0 ex1 ex2 ex3 ex4 ex5 ex6
```

```text
Success: no issues found in 7 source files
```

O flake8 não imprime nada, e o mypy confere os sete arquivos sem achar problema.

O mypy tem uma opção ainda mais rigorosa, `--strict`, que liga de uma vez um grupo de conferências
opcionais, entre elas a `--disallow-untyped-defs`. Os sete arquivos também passam nela:

```bash
.venv/bin/mypy --strict ex0 ex1 ex2 ex3 ex4 ex5 ex6
```

```text
Success: no issues found in 7 source files
```

## As saídas

Os exercícios 0, 1, 2 e 4 têm saída fixa e são conferidos com os `diff` das páginas
"Rodar e conferir" de cada um: nenhum deles deve imprimir nada. Os exercícios 3, 5 e 6 sorteiam
valores, e a conferência é pelas regras: as contagens do exercício 5, as conquistas do exercício
3 e a média do exercício 6.

## Nenhum arquivo aberto

Os programas não podem abrir arquivos. Nenhum deles chama `open`:

```bash
grep -c 'open(' ex[0-6]/*.py
```

```text
ex0/ft_command_quest.py:0
ex1/ft_score_analytics.py:0
ex2/ft_coordinate_system.py:0
ex3/ft_achievement_tracker.py:0
ex4/ft_inventory_system.py:0
ex5/ft_data_stream.py:0
ex6/ft_data_alchemist.py:0
```

`ex[0-6]/*.py` quer dizer "todo arquivo `.py` dentro das pastas `ex0` a `ex6`": o `[0-6]` casa
com um dígito de 0 a 6, e deixa de fora a pasta `experimentos`, que também começa com `ex`. O
`grep -c` conta, em cada arquivo, as linhas que têm `open(`.
