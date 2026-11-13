---
sidebar_position: 6
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 ft_distillation_0.py; python3 ft_distillation_1.py) - <<'FIM'
=== Distillation 0 ===
Direct access to alchemy/potions.py
Testing strength_potion: Strength potion brewed with 'Fire element created' and 'Water element created'
Testing healing_potion: Healing potion brewed with 'Earth element created' and 'Air element created'
=== Distillation 1 ===
Using: 'import alchemy' structure to access potions
Testing strength_potion: Strength potion brewed with 'Fire element created' and 'Water element created'
Testing heal alias: Healing potion brewed with 'Earth element created' and 'Air element created'
FIM
```

Dentro do `<( ... )`, os dois scripts rodam um depois do outro (o `;` separa os comandos), e o
`diff` recebe as duas saídas juntas
([Rodar e conferir da Parte I](../03-parte-1/08-rodar-e-conferir.md)). Sem nenhuma linha
impressa, as saídas são as esperadas.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 *.py alchemy
.venv/bin/mypy --disallow-untyped-defs *.py alchemy
```

```text
ft_alembic_4.py:12: error: Module has no attribute "create_earth"; maybe "create_air"?  [attr-defined]
Found 1 error in 1 file (checked 12 source files)
```

O flake8 não imprime nada: `__all__` cobre os dois nomes novos do `__init__.py`. O mypy confere
os doze arquivos e acusa só a linha proposital da Parte I.

## A Parte I continua igual

O `__init__.py` mudou, e a interface do pacote cresceu. O `create_earth` continua de fora, e o
`ft_alembic_4.py` termina com o mesmo erro. `tail -n 1` mostra só a última linha do que recebe:

```bash
python3 ft_alembic_4.py 2>&1 | tail -n 1
```

```text
AttributeError: module 'alchemy' has no attribute 'create_earth'. Did you mean '.create_air' instead of '.create_earth'?
```

A sugestão continua sendo `create_air`, o nome do pacote mais parecido com `create_earth`. Do
Python 3.10 ao 3.14, ela é escrita `Did you mean: 'create_air'?`, como no enunciado. Os `diff`
da [Parte I](../03-parte-1/08-rodar-e-conferir.md) continuam dando o mesmo resultado.
