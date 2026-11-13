---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

Os três exemplos do enunciado, cada um rodado de dentro da pasta `ex1`
([por quê](../03-ex0/02-a-linha-de-comando.md#o-nome-do-programa)) e comparado com `diff`:

```bash
diff <(cd ex1 && python3 ft_score_analytics.py 1500 2300 1800 2100 1950) - <<'FIM'
=== Player Score Analytics ===
Scores processed: [1500, 2300, 1800, 2100, 1950]
Total players: 5
Total score: 9650
Average score: 1930.0
High score: 2300
Low score: 1500
Score range: 800
FIM
diff <(cd ex1 && python3 ft_score_analytics.py) - <<'FIM'
=== Player Score Analytics ===
No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...
FIM
diff <(cd ex1 && python3 ft_score_analytics.py ab ac) - <<'FIM'
=== Player Score Analytics ===
Invalid parameter: 'ab'
Invalid parameter: 'ac'
No scores provided. Usage: python3 ft_score_analytics.py <score1> <score2> ...
FIM
```

Nenhum `diff` imprime nada.

## Válidos e inválidos misturados

O enunciado pede que, com os dois tipos de argumento, os inválidos sejam descartados e os válidos
sigam:

```bash
(cd ex1 && python3 ft_score_analytics.py 1500 ab 2300 1800)
```

```text
=== Player Score Analytics ===
Invalid parameter: 'ab'
Scores processed: [1500, 2300, 1800]
Total players: 3
Total score: 5600
Average score: 1866.6666666666667
High score: 2300
Low score: 1500
Score range: 800
```

A média `1866.6666666666667` mostra como o Python imprime um `float` que não termina: com até 17
dígitos significativos, o suficiente para identificar o valor guardado. O enunciado não pede
arredondamento nesta linha.

## Pontuações fora da faixa

2⁵³ = 9007199254740992 é aceito; um a mais não é:

```bash
(cd ex1 && python3 ft_score_analytics.py 9007199254740992 9007199254740993 1500)
```

```text
=== Player Score Analytics ===
Invalid parameter: '9007199254740993'
Scores processed: [9007199254740992, 1500]
Total players: 2
Total score: 9007199254742492
Average score: 4503599627371246.0
High score: 9007199254740992
Low score: 1500
Score range: 9007199254739492
```

Um número de centenas de dígitos recebe o mesmo aviso, e a média nunca estoura o `float`.

## Um argumento que não é UTF-8

```bash
(cd ex1 && python3 ft_score_analytics.py 1500 $'\xff' 2300)
```

```text
=== Player Score Analytics ===
Invalid parameter: '<not valid UTF-8>'
Scores processed: [1500, 2300]
Total players: 2
Total score: 3800
Average score: 1900.0
High score: 2300
Low score: 1500
Score range: 800
```

O argumento com o byte `\xff` é descartado como os outros inválidos, e as pontuações válidas
seguem.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex1
.venv/bin/mypy --disallow-untyped-defs ex1
```

```text
Success: no issues found in 1 source file
```
