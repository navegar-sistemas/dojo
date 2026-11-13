---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

## A luz

```bash
diff <(python3 ft_kaboom_0.py) - <<'FIM'
=== Kaboom 0 ===
Using grimoire module directly
Testing record light spell: Spell recorded: Fantasy (Earth, wind and fire - VALID)
FIM
```

Sem nenhuma linha impressa, a saída é a esperada.

## As trevas

O mesmo comando da [Parte I](../03-parte-1/08-rodar-e-conferir.md#a-saída-com-o-traceback):
`2>&1` junta o traceback à saída, e o `sed` troca o caminho da sua pasta pelo do enunciado.

```bash
diff <(python3 ft_kaboom_1.py 2>&1 | sed "s|$(pwd -P)|/tmp/Python/module-06|") - <<'FIM'
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
FIM
```

Desta vez o `diff` não imprime nada, no Python 3.10 e no 3.14: o traceback inteiro é igual ao do
enunciado, com os mesmos arquivos, as mesmas linhas (7, 2 e 2) e a mesma mensagem.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 *.py alchemy
.venv/bin/mypy --disallow-untyped-defs *.py alchemy
```

```text
ft_alembic_4.py:12: error: Module has no attribute "create_earth"; maybe "create_air"?  [attr-defined]
Found 1 error in 1 file (checked 24 source files)
```

Os 24 arquivos da árvore final, e só o erro proposital da Parte I.

## Feitiços rejeitados e letras maiúsculas

```bash
python3 -c 'import alchemy.grimoire as g; print(g.light_spell_record("Gloom", "bats and frogs"))'
python3 -c 'import alchemy.grimoire as g; print(g.light_spell_record("Rain", "WATER"))'
```

```text
Spell rejected: Gloom (bats and frogs - INVALID)
Spell recorded: Rain (WATER - VALID)
```

- `import alchemy.grimoire as g` dá o apelido `g` ao subpacote, para o comando ficar curto;
- morcegos e sapos não são ingredientes da luz, e o feitiço é rejeitado, no formato escolhido
  pelo tutorial ([O problema](./01-o-problema.md#a-saída-esperada));
- `WATER`, em maiúsculas, é aceito: o validador compara em minúsculas e devolve o texto como veio.

## O validador sozinho

As trevas explodem também quando se importa o validador
([Pelo outro lado](./03-a-explosao.md#pelo-outro-lado)). O da luz pode ser importado e usado
sozinho:

```bash
python3 -c 'from alchemy.grimoire.light_validator import validate_ingredients; print(validate_ingredients("fire"))'
```

```text
fire - VALID
```

O import passa antes pelo `alchemy/grimoire/__init__.py`, que carrega o livro da luz, e o livro
carrega o validador. Na chamada, o import de dentro da função acha o livro já completo. O
`__init__.py` não interfere nas trevas: ele não importa nada delas, e o validador das trevas,
importado do mesmo jeito, começa o ciclo por conta própria.
