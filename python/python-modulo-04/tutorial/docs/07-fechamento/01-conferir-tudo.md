---
sidebar_position: 1
title: Conferir tudo
---

# Conferir tudo

As conferências de todos os exercícios, rodadas da pasta `data-archivist`.

## Os arquivos

```bash
ls ex0 ex1 ex2 ex3
```

```text
ex0:
ft_ancient_text.py

ex1:
ft_archive_creation.py

ex2:
ft_stream_management.py

ex3:
ft_vault_security.py
```

Um arquivo por pasta, com o nome exato que o enunciado pede: um nome com uma letra trocada ou sem o
`.py` já não é o arquivo do exercício.

## Estilo e tipos

```bash
.venv/bin/flake8 ex0 ex1 ex2 ex3
.venv/bin/mypy --disallow-untyped-defs ex0 ex1 ex2 ex3
```

```text
Success: no issues found in 4 source files
```

O flake8 não imprime nada, e o mypy não acha problema em nenhum dos quatro arquivos.

## As saídas

Rode de novo os `diff` da página "Rodar e conferir" de cada exercício:
[0](../03-ex0/06-rodar-e-conferir.md), [1](../04-ex1/08-rodar-e-conferir.md),
[2](../05-ex2/06-rodar-e-conferir.md) e [3](../06-ex3/07-rodar-e-conferir.md). Nenhum deles pode
imprimir nada.

## Nenhum programa trava

Todos os programas terminam com código de saída `0`, o "terminou bem", inclusive nas falhas. O laço
abaixo roda cada programa com um arquivo inexistente, e o exercício 3 com a demonstração:

```bash
for f in ex0/ft_ancient_text.py ex1/ft_archive_creation.py ex2/ft_stream_management.py; do
    python3 "$f" foo > /dev/null 2>&1
    echo "$f: $?"
done
python3 ex3/ft_vault_security.py > /dev/null
echo "ex3/ft_vault_security.py: $?"
```

```text
ex0/ft_ancient_text.py: 0
ex1/ft_archive_creation.py: 0
ex2/ft_stream_management.py: 0
ex3/ft_vault_security.py: 0
```

- `for f in ...; do ...; done` repete os comandos entre `do` e `done` uma vez para cada nome da
  lista, com o nome na variável `f`; `"$f"` é o valor dela;
- `> /dev/null 2>&1` descarta as duas saídas, que já foram conferidas pelos `diff` ([Os três
  fluxos](../05-ex2/02-os-tres-fluxos.md));
- `echo "$f: $?"` mostra o nome e o código de saída de cada programa.

## O with no lugar certo

```bash
grep -n "with " ex0/*.py ex1/*.py ex2/*.py
```

O `grep` não acha nada: o `with` só aparece no exercício 3.
