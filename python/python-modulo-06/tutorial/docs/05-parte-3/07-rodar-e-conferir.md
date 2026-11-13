---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(for i in 0 1 2; do python3 ft_transmutation_$i.py; done) - <<'FIM'
=== Transmutation 0 ===
Using file alchemy/transmutation/recipes.py directly
Testing lead to gold: Recipe transmuting Lead to Gold: brew 'Air element created' and 'Strength potion brewed with 'Fire element created' and 'Water element created'' mixed with 'Fire element created'
=== Transmutation 1 ===
Import transmutation module directly
Testing lead to gold: Recipe transmuting Lead to Gold: brew 'Air element created' and 'Strength potion brewed with 'Fire element created' and 'Water element created'' mixed with 'Fire element created'
=== Transmutation 2 ===
Import alchemy module only
Testing lead to gold: Recipe transmuting Lead to Gold: brew 'Air element created' and 'Strength potion brewed with 'Fire element created' and 'Water element created'' mixed with 'Fire element created'
FIM
```

O `for i in 0 1 2` roda `ft_transmutation_0.py`, `ft_transmutation_1.py` e
`ft_transmutation_2.py`: o `$i` dentro do nome é trocado por cada número. Sem nenhuma linha
impressa, as três saídas são as esperadas.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 *.py alchemy
.venv/bin/mypy --disallow-untyped-defs *.py alchemy
```

```text
ft_alembic_4.py:12: error: Module has no attribute "create_earth"; maybe "create_air"?  [attr-defined]
Found 1 error in 1 file (checked 17 source files)
```

O flake8 não imprime nada, e o mypy confere os dezessete arquivos e acusa só a linha proposital
da Parte I. O mypy entende os imports relativos: ele faz a mesma conta dos pontos que o Python.

## As partes anteriores continuam iguais

```bash
python3 ft_alembic_4.py 2>&1 | tail -n 1
```

```text
AttributeError: module 'alchemy' has no attribute 'create_earth'. Did you mean '.create_air' instead of '.create_earth'?
```

A interface de `alchemy` cresceu de novo, e `create_earth` continua de fora (no Python 3.10 e no
3.14, a sugestão é escrita `Did you mean: 'create_air'?`). Os `diff` das
Partes [I](../03-parte-1/08-rodar-e-conferir.md) e [II](../04-parte-2/06-rodar-e-conferir.md)
continuam dando o mesmo resultado.

## Os três caminhos chegam à mesma função

```bash
python3 -c "import alchemy; print(alchemy.transmutation.recipes.lead_to_gold is alchemy.lead_to_gold)"
```

```text
True
```

`is` responde se dois nomes apontam para o **mesmo** objeto. `alchemy.lead_to_gold` não é uma
cópia da receita: é outro nome para a própria função escrita em `recipes.py`.
