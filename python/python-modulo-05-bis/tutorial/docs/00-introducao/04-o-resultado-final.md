---
sidebar_position: 4
title: O resultado final
---

# O resultado final

Esta é a saída de cada programa pronto. Os programas não recebem argumentos nem leem o teclado:
cada um roda uma demonstração fixa. Os comandos são rodados na pasta do projeto
([A pasta do projeto](../01-ambiente/02-a-pasta-do-projeto.md)) e só funcionam depois que os
arquivos existirem: a página "Rodar e conferir" de cada exercício os roda.

Algumas saídas têm caminhos de pastas, que mudam de máquina para máquina. Como o enunciado faz com
`/path/to/lab_env`, o tutorial escreve `/path/to/` no lugar da parte que muda: `/path/to/the-codex`
é a pasta do projeto, e `/path/to/python3.15` é o executável do Python global. No terminal aparecem
os caminhos completos. Algumas linhas são longas: o terminal as quebra na largura da janela, mas
cada uma é uma linha só.

## Exercício 0

Fora de um ambiente virtual:

```bash
python3 ex0/construct.py
```

```text

LABORATORY STATUS: You are working in the open

Current Python: /path/to/python3.15
Virtual Environment: None detected

WARNING: You are in the global environment!
Every reagent you install here leaks into the whole system.

To seal the laboratory, run:
python3 -m venv lab_env
source lab_env/bin/activate # On Unix
lab_env\Scripts\activate  # On Windows

Then run this program again.
```

Dentro do ambiente `lab_env`, ativado:

```bash
python3 ex0/construct.py
```

```text

LABORATORY STATUS: The laboratory is sealed

Current Python: /path/to/the-codex/lab_env/bin/python3
Virtual Environment: lab_env
Environment Path: /path/to/the-codex/lab_env

SUCCESS: You are working in an isolated environment!
Safe to install reagents without affecting
the global system.

Reagent installation path:
/path/to/the-codex/lab_env/lib/python3.15/site-packages
```

Com as bibliotecas instaladas (as versões mudam com o tempo):

```bash
python3 ex0/loading.py
```

```text

REAGENT STATUS: Loading reagents...

Checking dependencies:
[OK] pandas (3.1.1) - Data manipulation ready
[OK] numpy (2.5.4) - Numerical computation ready

pip vs Poetry:
  requirements.txt declares what to install; pip resolves it at install time.
  pyproject.toml declares the same constraints, and Poetry pins the resolved
  versions in poetry.lock so every install is identical.

All reagents present and accounted for.
```

## Exercício 1

Com o `lab_env` ativado e o `ex1/.env` preenchido:

```bash
python3 ex1/oracle.py
```

```text

ORACLE STATUS: Consulting the configuration...

Configuration loaded:
Mode: development
Database: Connected to local instance
API Access: Authenticated
Log Level: DEBUG
Remote Network: Online

Configuration security check:
[OK] No hardcoded secrets detected
[OK] .env file properly ignored by git
[OK] Production overrides available

The Oracle sees all configurations.
```

## Exercício 2

```bash
python3 ft_alembic_0.py
```

```text
=== Alembic 0 ===
Using: 'import ...' structure to access elements.py
Testing create_fire: Fire element created
```

```bash
python3 ft_alembic_1.py
```

```text
=== Alembic 1 ===
Accessing the alchemy module using 'import alchemy'
Testing create_air: Air element created
Now show that not all functions can be reached
This will raise an exception!
Testing the hidden create_earth: Traceback (most recent call last):
  File "/path/to/the-codex/ft_alembic_1.py", line 10, in <module>
    print(f"{alchemy.create_earth()}")
             ^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'alchemy' has no attribute 'create_earth'. Did you mean '.create_air' instead of '.create_earth'?
```

## Exercício 3

```bash
python3 ft_distillation_0.py
```

```text
=== Distillation 0 ===
Direct access to alchemy/potions.py
Testing strength_potion: Strength potion brewed with 'Fire element created' and 'Water element created'
Testing healing_potion: Healing potion brewed with 'Earth element created' and 'Air element created'
```

```bash
python3 ft_transmutation_0.py
```

```text
=== Transmutation 0 ===
Using file alchemy/transmutation/recipes.py directly
Testing lead to gold: Recipe transmuting Lead to Gold: brew 'Air element created' and 'Strength potion brewed with 'Fire element created' and 'Water element created'' mixed with 'Fire element created'
```

## Exercício 4

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
  File "/path/to/the-codex/ft_kaboom_1.py", line 5, in <module>
    from alchemy.grimoire.dark_spellbook import dark_spell_record
  File "/path/to/the-codex/alchemy/grimoire/dark_spellbook.py", line 1, in <module>
    from .dark_validator import validate_ingredients
  File "/path/to/the-codex/alchemy/grimoire/dark_validator.py", line 1, in <module>
    from .dark_spellbook import dark_spell_allowed_ingredients
ImportError: cannot import name 'dark_spell_allowed_ingredients' from partially initialized module 'alchemy.grimoire.dark_spellbook' (most likely due to a circular import) (/path/to/the-codex/alchemy/grimoire/dark_spellbook.py)
```

Do Python 3.10 ao 3.14, a sugestão da última linha do `ft_alembic_1.py` é
`Did you mean: 'create_air'?`, como no enunciado; no 3.10, o traceback também não tem a linha de
`^`. As saídas mostradas no tutorial são as do Python 3.15; as diferenças das outras versões estão na
página de cada programa.

Os dois tracebacks são de propósito: o exercício 2 mostra que `create_earth` não está na interface
do pacote, e o 4, que o par das trevas explode. Os números de linha dos tracebacks são os dos
arquivos do tutorial; os do enunciado são outros, porque os arquivos de quem o escreveu têm outra
disposição.
