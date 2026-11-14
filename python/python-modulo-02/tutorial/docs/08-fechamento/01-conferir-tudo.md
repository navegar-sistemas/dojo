---
sidebar_position: 1
title: Conferir tudo
---

# Conferir tudo

Antes de entregar, as conferências de todos os exercícios rodam de uma vez, a partir da pasta
`garden-guardian`.

## Os arquivos

```bash
ls ex0 ex1 ex2 ex3 ex4
```

```text
ex0:
ft_first_exception.py

ex1:
ft_raise_exception.py

ex2:
ft_different_errors.py

ex3:
ft_custom_errors.py

ex4:
ft_finally_block.py
```

Um arquivo por pasta, com o nome exato que o enunciado pede. Um nome errado (uma letra trocada,
`.py` faltando) deixa o arquivo diferente do que o enunciado pede.

## Estilo

```bash
.venv/bin/flake8 ex0 ex1 ex2 ex3 ex4
```

O flake8 não imprime nada.

## Tipos

```bash
.venv/bin/mypy --disallow-untyped-defs ex0 ex1 ex2 ex3 ex4
```

```text
ex2/ft_different_errors.py:10: error: Unsupported operand types for + ("str" and "int")  [operator]
Found 1 error in 1 file (checked 5 source files)
```

Só o erro proposital do exercício 2 ([O erro proposital do mypy](../05-ex2/03-o-erro-proposital-do-mypy.md)).
Os outros quatro arquivos passam sem nenhuma reclamação.

## As saídas

Rode de novo o `diff` da página "Rodar e conferir" de cada exercício:
[0](../03-ex0/06-rodar-e-conferir.md), [1](../04-ex1/06-rodar-e-conferir.md),
[2](../05-ex2/06-rodar-e-conferir.md), [3](../06-ex3/09-rodar-e-conferir.md) e
[4](../07-ex4/07-rodar-e-conferir.md). Nenhum deles pode imprimir nada.

## Nenhum programa trava

Todos os programas terminam com código de saída `0`, o "terminou bem" da página
[O programa que trava](../02-excecoes/01-o-programa-que-trava.md):

```bash
for f in ex0/ft_first_exception.py ex1/ft_raise_exception.py ex2/ft_different_errors.py ex3/ft_custom_errors.py ex4/ft_finally_block.py; do
    python3 "$f" > /dev/null
    echo "$f: $?"
done
```

```text
ex0/ft_first_exception.py: 0
ex1/ft_raise_exception.py: 0
ex2/ft_different_errors.py: 0
ex3/ft_custom_errors.py: 0
ex4/ft_finally_block.py: 0
```

O `for` roda cada programa; `> /dev/null` descarta a saída, que já foi conferida pelo `diff`, e
`echo "$f: $?"` mostra o código de saída de cada um.
