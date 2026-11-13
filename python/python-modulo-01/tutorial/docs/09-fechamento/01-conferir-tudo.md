---
sidebar_position: 1
title: Conferir tudo
---

# Conferir tudo

Antes de entregar, as conferências de cada exercício, agora todas juntas, a partir da pasta
`code-cultivation`.

## Os arquivos

```bash
ls -1 ex[0-6]/*.py
```

```text
ex0/ft_garden_intro.py
ex1/ft_garden_data.py
ex2/ft_plant_growth.py
ex3/ft_plant_factory.py
ex4/ft_garden_security.py
ex5/ft_plant_types.py
ex6/ft_garden_analytics.py
```

- `ex[0-6]/*.py` quer dizer "todo arquivo `.py` dentro das pastas `ex0` a `ex6`": `[0-6]` casa
  com um único caractere entre `0` e `6`, e `*` com qualquer sequência de caracteres. Um `ex*`
  não serviria, porque casaria também com `experimentos`;
- `-1` faz o `ls` listar um por linha.

Um arquivo por pasta, com o nome exato que o enunciado pede. Um nome errado (uma letra trocada,
`.py` faltando) faz o exercício não ser encontrado na avaliação.

## Estilo

```bash
.venv/bin/flake8 ex0 ex1 ex2 ex3 ex4 ex5 ex6
```

O flake8 não imprime nada.

## Tipos

```bash
.venv/bin/mypy --strict ex0 ex1 ex2 ex3 ex4 ex5 ex6
```

```text
Success: no issues found in 7 source files
```

## As saídas

Rode de novo o `diff` da página "Rodar e conferir" de cada exercício:
[0](../02-ex0/05-rodar-e-conferir.md), [1](../03-ex1/06-rodar-e-conferir.md),
[2](../04-ex2/06-rodar-e-conferir.md), [3](../05-ex3/06-rodar-e-conferir.md),
[4](../06-ex4/08-rodar-e-conferir.md), [5](../07-ex5/08-rodar-e-conferir.md) e
[6](../08-ex6/09-rodar-e-conferir.md). Nenhum deles pode imprimir nada.

## Nenhum programa termina com erro

Todo programa que termina bem devolve ao sistema o **código de saída** `0`; um programa que para
com um erro do Python devolve `1`. Todos os programas precisam terminar com `0`:

```bash
for f in ex[0-6]/*.py; do
    python3 "$f" > /dev/null
    echo "$f: $?"
done
```

```text
ex0/ft_garden_intro.py: 0
ex1/ft_garden_data.py: 0
ex2/ft_plant_growth.py: 0
ex3/ft_plant_factory.py: 0
ex4/ft_garden_security.py: 0
ex5/ft_plant_types.py: 0
ex6/ft_garden_analytics.py: 0
```

O `for` roda cada programa; `> /dev/null` descarta a saída, que já foi conferida pelo `diff`, e
`echo "$f: $?"` mostra o nome do arquivo e o código de saída dele (`$?` é o código de saída do
último comando).
