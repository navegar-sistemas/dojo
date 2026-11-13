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
from alchemy.elements import create_air
from elements import create_fire
from ..potions import strength_potion


def lead_to_gold() -> str:
    return ("Recipe transmuting Lead to Gold: "
            f"brew '{create_air()}' and '{strength_potion()}' "
            f"mixed with '{create_fire()}'")
```

## Os três imports

| Linha | Tipo | Por que assim |
|---|---|---|
| `from alchemy.elements import create_air` | absoluto | o import absoluto pedido pelo enunciado; mostra o caminho inteiro a partir da raiz |
| `from elements import create_fire` | absoluto | o `elements.py` da raiz não está em pacote nenhum: o único caminho até ele é o absoluto |
| `from ..potions import strength_potion` | relativo | o import relativo pedido pelo enunciado: sobe de `alchemy.transmutation` para `alchemy` e pega `potions` |

`create_air` também poderia vir por um import relativo (`from ..elements import create_air`); a
escolha de um absoluto e um relativo para os dois vizinhos do pacote deixa os dois jeitos lado a
lado no mesmo arquivo, que é o que o enunciado quer ver.

## O texto

O `return` junta três pedaços dentro dos parênteses: um texto comum e duas f-strings. O texto
devolvido por `strength_potion()` já vem com aspas simples dentro dele, e por isso a saída tem
`''` no fim da poção.

Falta o `__init__.py` da pasta `transmutation`, que a transforma num pacote de verdade
([O pacote](../03-parte-1/03-o-pacote.md#o-que-falta-o-__init__py)) e leva até a receita quem
importa só o pacote. A [próxima página](./04-o-subpacote.md) cria esse arquivo.
