---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(python3 ft_distillation_0.py) - <<'FIM'
=== Distillation 0 ===
Direct access to alchemy/potions.py
Testing strength_potion: Strength potion brewed with 'Fire element created' and 'Water element created'
Testing healing_potion: Healing potion brewed with 'Earth element created' and 'Air element created'
FIM
```

```bash
diff <(python3 ft_transmutation_0.py) - <<'FIM'
=== Transmutation 0 ===
Using file alchemy/transmutation/recipes.py directly
Testing lead to gold: Recipe transmuting Lead to Gold: brew 'Air element created' and 'Strength potion brewed with 'Fire element created' and 'Water element created'' mixed with 'Fire element created'
FIM
```

Nenhum dos dois imprime nada: as saídas são as do enunciado, com a frase longa da transmutação
numa linha só.

## Estilo e tipos

```bash
.venv/bin/flake8 alchemy/potions.py alchemy/transmutation ft_distillation_0.py ft_transmutation_0.py
.venv/bin/mypy --disallow-untyped-defs alchemy/potions.py alchemy/transmutation ft_distillation_0.py ft_transmutation_0.py
```

```text
Success: no issues found in 5 source files
```

O flake8 não imprime nada. O mypy conta cinco arquivos: os quatro `.py` com código e o
`__init__.py` vazio da pasta `alchemy/transmutation`. Para conferir os imports, ele também lê os
módulos importados (`elements.py`, `alchemy/__init__.py`, `alchemy/elements.py`), sem contá-los.

## De outra pasta

A primeira pasta do `sys.path` é a pasta do programa, e não a do terminal. Rodado de dentro de
`alchemy`, o programa continua achando tudo:

```bash
cd alchemy
python3 ../ft_transmutation_0.py | tail -n 1 | cut -c1-60
cd ..
```

```text
Testing lead to gold: Recipe transmuting Lead to Gold: brew 
```

`../ft_transmutation_0.py` é o programa da pasta de cima (`..` é a pasta de cima); `tail -n 1`
guarda a última linha da saída, e `cut -c1-60` corta os 60 primeiros caracteres, só para caber
aqui. A receita foi preparada: `elements`, `alchemy.potions` e o resto foram achados a partir da
raiz, a pasta do programa.
