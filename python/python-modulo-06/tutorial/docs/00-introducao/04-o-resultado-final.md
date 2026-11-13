---
sidebar_position: 4
title: O resultado final
---

# O resultado final

Esta é a saída de cada script pronto, como no enunciado. Os scripts não recebem argumentos nem
leem o teclado. Os comandos são rodados na pasta do projeto
([A pasta do projeto](../01-ambiente/02-a-pasta-do-projeto.md)) e só funcionam depois que os
arquivos existirem: a página "Rodar e conferir" de cada parte os roda.

Algumas linhas são longas: o terminal as quebra na largura da janela, mas cada uma é uma linha só.

## Parte I

```bash
python3 ft_alembic_0.py
python3 ft_alembic_1.py
python3 ft_alembic_2.py
python3 ft_alembic_3.py
```

```text
=== Alembic 0 ===
Using: 'import ...' structure to access elements.py
Testing create_fire: Fire element created
=== Alembic 1 ===
Using: 'from ... import ...' structure to access elements.py
Testing create_water: Water element created
=== Alembic 2 ===
Accessing alchemy/elements.py using 'import ...' structure
Testing create_earth: Earth element created
=== Alembic 3 ===
Accessing alchemy/elements.py using 'from ... import ...' structure
Testing create_air: Air element created
```

```bash
python3 ft_alembic_4.py
```

```text
=== Alembic 4 ===
Accessing the alchemy module using 'import alchemy'
Testing create_air: Air element created
Now show that not all functions can be reached
This will raise an exception!
Testing the hidden create_earth: Traceback (most recent call last):
  File "/tmp/Python/module-06/ft_alembic_4.py", line 12, in <module>
    print(f"{alchemy.create_earth()}")
            ^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'alchemy' has no attribute 'create_earth'. Did you mean: 'create_air'?
```

O erro é o resultado esperado ([O erro proposital](../03-parte-1/06-o-erro-proposital.md)).
`/tmp/Python/module-06` é a pasta onde o enunciado rodou o script; na sua máquina, aparece o
caminho da sua pasta. Duas linhas mudam com a versão do Python. A dos `^`: o enunciado foi gerado
com uma versão mais antiga, e nas versões recentes ela começa uma coluna depois; no 3.10, ela não
aparece. A última: no Python 3.15, a sugestão é escrita
`Did you mean '.create_air' instead of '.create_earth'?`.

```bash
python3 ft_alembic_5.py
```

```text
=== Alembic 5 ===
Accessing the alchemy module using 'from alchemy import ...'
Testing create_air: Air element created
```

## Parte II

```bash
python3 ft_distillation_0.py
python3 ft_distillation_1.py
```

```text
=== Distillation 0 ===
Direct access to alchemy/potions.py
Testing strength_potion: Strength potion brewed with 'Fire element created' and 'Water element created'
Testing healing_potion: Healing potion brewed with 'Earth element created' and 'Air element created'
=== Distillation 1 ===
Using: 'import alchemy' structure to access potions
Testing strength_potion: Strength potion brewed with 'Fire element created' and 'Water element created'
Testing heal alias: Healing potion brewed with 'Earth element created' and 'Air element created'
```

## Parte III

```bash
python3 ft_transmutation_0.py
python3 ft_transmutation_1.py
python3 ft_transmutation_2.py
```

```text
=== Transmutation 0 ===
Using file alchemy/transmutation/recipes.py directly
Testing lead to gold: Recipe transmuting Lead to Gold: brew 'Air element created' and 'Strength potion brewed with 'Fire element created' and 'Water element created'' mixed with 'Fire element created'
=== Transmutation 1 ===
Import transmutation module directly
Testing lead to gold: Recipe transmuting Lead to Gold: brew 'Air element created' and 'Strength potion brewed with 'Fire element created' and 'Water element created'' mixed with 'Fire element created'
=== Transmutation 2 ===
Import alchemy module only
Testing lead to gold: Recipe transmuting Lead to Gold: brew 'Air element created' and 'Strength potion brewed with 'Fire element created' and 'Water element created'' mixed with 'Fire element created'
```

## Parte IV

```bash
python3 ft_kaboom_0.py
```

```text
=== Kaboom 0 ===
Using grimoire module directly
Testing record light spell: Spell recorded: Fantasy (Earth, wind and fire - VALID)
```

```bash
python3 ft_kaboom_1.py
```

```text
=== Kaboom 1 ===
Access to alchemy/grimoire/dark_spellbook.py directly
Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION
Traceback (most recent call last):
  File "/tmp/Python/module-06/ft_kaboom_1.py", line 7, in <module>
    from alchemy.grimoire.dark_spellbook import dark_spell_record
  File "/tmp/Python/module-06/alchemy/grimoire/dark_spellbook.py", line 2, in <module>
    from .dark_validator import validate_ingredients
  File "/tmp/Python/module-06/alchemy/grimoire/dark_validator.py", line 2, in <module>
    from .dark_spellbook import dark_spell_allowed_ingredients
ImportError: cannot import name 'dark_spell_allowed_ingredients' from partially initialized module 'alchemy.grimoire.dark_spellbook' (most likely due to a circular import) (/tmp/Python/module-06/alchemy/grimoire/dark_spellbook.py)
```

Este erro também é o resultado esperado ([A explosão](../06-parte-4/03-a-explosao.md)), com o
caminho da sua pasta no lugar de `/tmp/Python/module-06`.
