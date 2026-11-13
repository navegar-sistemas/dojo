---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

## ft_kaboom_0.py contra o enunciado

```bash
diff <(python3 ft_kaboom_0.py) - <<'FIM'
=== Kaboom 0 ===
Using grimoire module directly
Testing record light spell: Spell recorded: Fantasy (Earth, wind and fire - VALID)
FIM
```

Sem nenhuma linha impressa.

## ft_kaboom_1.py contra o enunciado

As linhas do meio do traceback têm números de linha diferentes dos do enunciado, e a comparação
pega as quatro primeiras e a última, com o caminho da pasta trocado pelo do enunciado:

```bash
diff <(python3 ft_kaboom_1.py 2>&1 | sed -n '1,4p;$p' | sed "s|$PWD|/tmp/Python/module-05-bis|") - <<'FIM'
=== Kaboom 1 ===
Access to alchemy/grimoire/dark_spellbook.py directly
Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION
Traceback (most recent call last):
ImportError: cannot import name 'dark_spell_allowed_ingredients' from partially initialized module 'alchemy.grimoire.dark_spellbook' (most likely due to a circular import) (/tmp/Python/module-05-bis/alchemy/grimoire/dark_spellbook.py)
FIM
```

Sem nenhuma linha impressa. O `2>&1` é o da
[conferência do exercício 2](../05-ex2/07-rodar-e-conferir.md#ft_alembic_1py-contra-o-enunciado).
`sed -n '1,4p;$p'` imprime só as linhas 1 a 4 e a última (`$` é a última linha), e o segundo
`sed` troca `$PWD`, a pasta atual, pelo caminho do enunciado. O programa termina com
código de saída `1`, como todo programa que para numa exceção:

```bash
python3 ft_kaboom_1.py > /dev/null 2>&1
echo $?
```

```text
1
```

## A outra ordem também explode

Começando pelo validador das trevas, o círculo se fecha do outro lado:

```bash
python3 -c 'import alchemy.grimoire.dark_validator' 2>&1 | tail -n 1
```

```text
ImportError: cannot import name 'validate_ingredients' from partially initialized module 'alchemy.grimoire.dark_validator' (most likely due to a circular import) (/path/to/the-codex/alchemy/grimoire/dark_validator.py)
```

(`/path/to/the-codex` está no lugar do caminho da pasta do projeto.) Agora é o livro, carregado
pelo validador, que pede ao validador pela metade o `validate_ingredients`.

## A ordem real dos imports

Um programa que pede só o validador da luz carrega também o livro, e antes dele:

```bash
python3 -c 'import sys
import alchemy.grimoire.light_validator
print("alchemy.grimoire.light_spellbook" in sys.modules)'
```

```text
True
```

`"nome" in sys.modules` pergunta se o módulo já foi carregado
([O import circular](../04-conceitos/05-o-import-circular.md#como-um-import-roda-passo-a-passo)).
Para chegar ao `light_validator`, o Python carrega antes o pacote `alchemy.grimoire`, e o
`__init__.py` dele importa o `light_spellbook`, que importa o validador. Neste pacote, o livro é
sempre o primeiro do par a carregar, venha o pedido de onde vier; por isso a luz não tem uma "outra
ordem" para testar, como as trevas.

## A luz não explode

Pedindo o validador da luz, com um ingrediente em maiúsculas e um conjunto inválido:

```bash
python3 -c 'from alchemy.grimoire.light_validator import validate_ingredients
print(validate_ingredients("FIRE and ice"))
print(validate_ingredients("ice and snow"))'
```

```text
FIRE and ice - VALID
ice and snow - INVALID
```

O código entre as aspas simples ocupa três linhas; o terminal espera a aspa final antes de rodar
o comando. `FIRE` foi reconhecido sem diferença de maiúsculas, e o texto devolvido mantém os
ingredientes como vieram. Um feitiço rejeitado, pelo livro:

```bash
python3 -c 'from alchemy.grimoire.light_spellbook import light_spell_record
print(light_spell_record("Frost", "ice and snow"))'
```

```text
Spell rejected: Frost (ice and snow - INVALID)
```

## Estilo e tipos

```bash
.venv/bin/flake8 alchemy/grimoire ft_kaboom_0.py ft_kaboom_1.py
.venv/bin/mypy --disallow-untyped-defs alchemy/grimoire ft_kaboom_0.py ft_kaboom_1.py
```

```text
Success: no issues found in 7 source files
```

O flake8 não imprime nada, e o mypy aceita os sete arquivos, inclusive o par das trevas: o ciclo
de imports não é erro de tipo, e só aparece quando o código roda.
