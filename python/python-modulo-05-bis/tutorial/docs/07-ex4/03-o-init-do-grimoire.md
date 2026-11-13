---
sidebar_position: 3
title: O __init__.py do grimoire
---

# O \_\_init\_\_.py do grimoire

O `ft_kaboom_0.py` acessa "o pacote `grimoire`" e registra um feitiço da luz. Para o pacote ter
essa função na interface, o `__init__.py` dele a expõe, como o de `alchemy` expõe `create_air`
([O \_\_init\_\_.py de alchemy](../05-ex2/03-o-init-de-alchemy.md)). Crie
`alchemy/grimoire/__init__.py`:

```python title="alchemy/grimoire/__init__.py"
from .light_spellbook import light_spell_record

__all__ = ["light_spell_record"]
```

- o pacote expõe só `light_spell_record`, a única função que o programa usa; expor só ela é escolha
  do tutorial;
- a `__all__` evita o aviso `F401` do flake8, como no `alchemy/__init__.py`.

O `__init__.py` **não** importa nada das trevas. Ele roda sempre que alguém importa qualquer coisa
de dentro do `grimoire`, inclusive o `ft_kaboom_0.py`; se ele importasse o `dark_spellbook`, o
pacote inteiro explodiria no `import`, e nem o feitiço da luz funcionaria. O par das trevas só é
carregado por quem o pede pelo caminho completo, como o `ft_kaboom_1.py`.
