---
sidebar_position: 5
title: "*args e **kwargs"
---

# \*args e \*\*kwargs

Um decorador embrulha funções que ele não conhece: uma pode receber dois argumentos, outra
nenhum, outra argumentos com nome. A função que embrulha precisa aceitar **qualquer** combinação
de argumentos e repassá-la intacta. Dois parâmetros especiais fazem isso: `*args` e `**kwargs`.

## Os dois jeitos de passar um argumento

Numa chamada como `describe("Dragon", power=10)`:

- `"Dragon"` é um **argumento posicional**: vai para o parâmetro que estiver naquela posição (o
  primeiro);
- `power=10` é um **argumento nomeado** (*keyword argument*): vai para o parâmetro com esse nome,
  em qualquer posição.

## O experimento

Crie `experimentos/argumentos.py`:

```python title="experimentos/argumentos.py"
from typing import Any


def show(*args: Any, **kwargs: Any) -> None:
    print(f"args={args} kwargs={kwargs}")


def describe(target: str, power: int) -> str:
    return f"{target} with {power} power"


show()
show("Dragon", 10)
show("Dragon", power=10)
values = ("Goblin", 5)
print(describe(*values))
options: dict[str, Any] = {"target": "Troll", "power": 7}
print(describe(**options))
```

```bash
python3 experimentos/argumentos.py
```

```text
args=() kwargs={}
args=('Dragon', 10) kwargs={}
args=('Dragon',) kwargs={'power': 10}
Goblin with 5 power
Troll with 7 power
```

## O que aconteceu

**Na definição, `*` e `**` recolhem.** Em `def show(*args, **kwargs)`:

- `*args` recolhe todos os argumentos posicionais numa **tupla**: `('Dragon', 10)`;
- `**kwargs` recolhe todos os argumentos nomeados num **dicionário**: `{'power': 10}`;
- sem argumentos, os dois ficam vazios: `()` e `{}`.

Os nomes `args` e `kwargs` são só o costume; o que importa são os asteriscos. O type hint `Any`
(de `typing`, "qualquer tipo") vale para **cada** argumento recolhido.

**Na chamada, `*` e `**` espalham.** O caminho inverso:

- `describe(*values)` espalha a tupla `("Goblin", 5)` em dois argumentos posicionais, como se
  fosse `describe("Goblin", 5)`;
- `describe(**options)` espalha o dicionário em argumentos nomeados, como se fosse
  `describe(target="Troll", power=7)`.

A anotação `dict[str, Any]` em `options` diz ao mypy que os valores podem ser de qualquer tipo.
Sem ela, ele deduziria `dict[str, object]` (o dicionário mistura `str` e `int`) e recusaria
espalhá-lo em `describe`, que pede um `str` e um `int`.

## Repassar tudo

Juntando os dois lados, uma função consegue receber qualquer coisa e repassar exatamente o que
recebeu:

```python
def wrapper(*args: Any, **kwargs: Any) -> Any:
    return func(*args, **kwargs)
```

`wrapper("Dragon", power=10)` recolhe `args = ("Dragon",)` e `kwargs = {"power": 10}`, e
`func(*args, **kwargs)` espalha os dois de volta: `func` recebe `func("Dragon", power=10)`, igual
à chamada original. É a peça central de todo decorador
([Decoradores](./06-decoradores.md)).
