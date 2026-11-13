---
sidebar_position: 5
title: ft_kaboom_0.py e ft_kaboom_1.py
---

# ft_kaboom_0.py e ft_kaboom_1.py

Os dois programas testam os dois grimórios: um registra um feitiço da luz, o outro tenta um das
trevas e explode.

## ft_kaboom_0.py

Crie `ft_kaboom_0.py`, na raiz:

```python title="ft_kaboom_0.py"
from alchemy.grimoire import light_spell_record

if __name__ == "__main__":
    print("=== Kaboom 0 ===")
    print("Using grimoire module directly")
    print("Testing record light spell: "
          f"{light_spell_record('Fantasy', 'Earth, wind and fire')}")
```

`from alchemy.grimoire import light_spell_record` pede a função à interface do pacote `grimoire`,
o nome que o `__init__.py` dele expõe. O feitiço `Fantasy`, com os ingredientes
`Earth, wind and fire`, é o da saída do enunciado. Dentro da f-string de aspas duplas, os textos
passados à função vão entre aspas simples.

```bash
python3 ft_kaboom_0.py
```

```text
=== Kaboom 0 ===
Using grimoire module directly
Testing record light spell: Spell recorded: Fantasy (Earth, wind and fire - VALID)
```

## ft_kaboom_1.py

O segundo programa precisa imprimir três linhas **antes** de tentar o import das trevas, e o
traceback do enunciado mostra o import dentro do próprio programa (`in <module>`). O import fica,
então, depois dos `print`. Crie `ft_kaboom_1.py`, na raiz:

```python title="ft_kaboom_1.py"
if __name__ == "__main__":
    print("=== Kaboom 1 ===")
    print("Access to alchemy/grimoire/dark_spellbook.py directly")
    print("Test import now - THIS WILL RAISE AN UNCAUGHT EXCEPTION")
    from alchemy.grimoire.dark_spellbook import dark_spell_record

    print("Testing record dark spell: "
          f"{dark_spell_record('Curse', 'bats and frogs')}")
```

- o import vem depois dos `print`, dentro do bloco `if __name__ == "__main__":`. Um import solto
  no meio do arquivo, fora de qualquer bloco, faria o flake8 acusar `E402 module level import not
  at top of file` ("import de nível de módulo fora do topo do arquivo"); dentro do bloco `if`, a
  regra não se aplica, porque o import fica num trecho condicional;
- o código dentro do `if` ainda roda no nível do módulo, e por isso o traceback mostra
  `in <module>`, como no enunciado;
- a última linha tenta registrar o feitiço `Curse` ("maldição") com `bats and frogs`. Ela nunca
  roda: o import da linha de cima explode antes. Ela fica no programa porque o enunciado pede que
  ele **tente** registrar um feitiço das trevas;
- a exceção não é capturada, escolha do tutorial: o programa termina com o traceback, como no
  exemplo.

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

A mesma sequência do enunciado. As diferenças são o caminho (`/path/to/the-codex` está no lugar da
pasta do projeto) e os números de linha: aqui o import do programa está na linha 5, e os imports
dos dois arquivos das trevas estão na linha 1; no arquivo de quem escreveu o enunciado, as linhas
eram 7 e 2. O traceback é igual no Python 3.10.
