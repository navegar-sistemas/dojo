---
sidebar_position: 3
title: A receita
---

# A receita

Crie a pasta do subpacote:

```bash
mkdir alchemy/transmutation
```

E, dentro dela, a receita:

```python title="alchemy/transmutation/recipes.py"
from elements import create_fire
from ..elements import create_air
from ..potions import strength_potion


def lead_to_gold() -> str:
    return ("Recipe transmuting Lead to Gold: "
            f"brew '{create_air()}' and '{strength_potion()}' "
            f"mixed with '{create_fire()}'")
```

## Os três imports

| Linha | Tipo | Por que assim |
|---|---|---|
| `from elements import create_fire` | absoluto | o `elements.py` da raiz não está em pacote nenhum: o único caminho até ele é o absoluto. É o import absoluto que o enunciado pede |
| `from ..elements import create_air` | relativo | sobe de `alchemy.transmutation` para `alchemy` e pega `elements`: o `alchemy/elements.py` |
| `from ..potions import strength_potion` | relativo | sobe do mesmo jeito e pega `potions`: o `alchemy/potions.py` |

Os três seguem o [critério do tutorial](./02-absoluto-e-relativo.md#o-critério-do-tutorial):
relativo para os arquivos do pacote `alchemy`, absoluto para o que está fora dele. O enunciado
pede pelo menos um de cada, e o arquivo tem um absoluto e dois relativos. O absoluto vem primeiro,
antes dos relativos, como de costume.

## O texto

O `return` junta três pedaços dentro dos parênteses: um texto comum e duas f-strings. O texto
devolvido por `strength_potion()` já vem com aspas simples dentro dele, e por isso a saída tem
`''` no fim da poção.

Falta o `__init__.py` da pasta `transmutation`, que a transforma num pacote de verdade
([O pacote](../03-parte-1/03-o-pacote.md#o-que-falta-o-__init__py)) e leva até a receita quem
importa só o pacote. A [próxima página](./04-o-subpacote.md) cria esse arquivo.
