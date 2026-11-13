---
sidebar_position: 2
title: A porta do pacote
---

# A porta do pacote

O pacote `ex4` também precisa do seu `__init__.py`, e ele vem primeiro: com ele, a pasta `ex4`
já é um pacote, e os imports relativos dos módulos das próximas páginas (`from .strategy import
...`) têm para onde apontar. O enunciado não limita o que o pacote expõe; o torneio precisa das
duas estratégias concretas, da classe abstrata (para o type hint dos oponentes) e da exceção
(para o `except`).

Crie o arquivo `ex4/__init__.py`. Os três módulos que ele importa (`aggressive`, `normal` e
`strategy`) são criados nas próximas páginas; até lá, o pacote ainda não pode ser importado:

```python title="ex4/__init__.py"
from .aggressive import AggressiveStrategy
from .normal import NormalStrategy
from .strategy import BattleStrategy, StrategyError

__all__ = [
    "AggressiveStrategy",
    "BattleStrategy",
    "NormalStrategy",
    "StrategyError",
]
```

- os três imports relativos trazem os quatro nomes dos três módulos do pacote;
- `__all__` lista os quatro, um por linha, e evita o aviso `F401` do flake8
  ([O aviso do flake8](../06-pacotes/01-o-pacote.md#o-aviso-do-flake8)). Uma lista entre
  colchetes pode ocupar várias linhas, e a vírgula depois do último item é permitida.

Com isso, `tournament.py` escreve `from ex4 import AggressiveStrategy` em vez de
`from ex4.aggressive import AggressiveStrategy`.
