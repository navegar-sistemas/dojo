---
sidebar_position: 3
title: partial_enchanter
---

# partial_enchanter

Uma função de encantamento recebe três argumentos: o poder, o elemento e o alvo. Se o poder é
quase sempre 50 e há só três elementos, repetir `enchant(50, "fire", ...)` em todo lugar é
desperdício. `functools.partial` cria uma função nova com alguns argumentos já preenchidos: a
**aplicação parcial**.

## partial

Crie `experimentos/parcial.py`:

```python title="experimentos/parcial.py"
from functools import partial


def enchant(power: int, element: str, target: str) -> str:
    return f"{element} enchantment on {target} with {power} power"


fire = partial(enchant, 50, "fire")
print(fire("Sword"))
print(fire.func.__name__, fire.args, fire.keywords)
ice = partial(enchant, power=50, element="ice")
print(ice(target="Shield"))
try:
    ice("Shield")
except TypeError as error:
    print(f"TypeError: {error}")
```

```bash
python3 experimentos/parcial.py
```

```text
fire enchantment on Sword with 50 power
enchant (50, 'fire') {}
ice enchantment on Shield with 50 power
TypeError: enchant() got multiple values for argument 'power'
```

- `partial(enchant, 50, "fire")` devolve um objeto que funciona como função. Chamado com
  `"Sword"`, ele chama `enchant(50, "fire", "Sword")`: os argumentos guardados vêm primeiro, e os
  novos vão depois;
- o objeto guarda a função original em `func` e os argumentos pré-preenchidos em `args`
  (posicionais) e `keywords` (nomeados);
- `partial(enchant, power=50, element="ice")` pré-preenche por **nome**. Chamado com
  `target="Shield"`, também por nome, funciona.

## A armadilha dos argumentos nomeados

A última chamada, `ice("Shield")`, falha: `"Shield"` é posicional, e um argumento posicional vai
para o **primeiro** parâmetro, `power`. Como `power` também já veio por nome (`power=50`),
`enchant` recebe dois valores para o mesmo parâmetro: "`enchant()` recebeu vários valores para o
argumento `power`".

O mypy acha o erro sem rodar o programa:

```bash
.venv/bin/mypy --disallow-untyped-defs experimentos/parcial.py
```

```text
experimentos/parcial.py:14: error: Too many positional arguments for "enchant"  [call-arg]
experimentos/parcial.py:14: error: Too few arguments for "enchant"  [call-arg]
experimentos/parcial.py:14: error: Argument 1 to "enchant" has incompatible type "str"; expected "int"  [arg-type]
Found 3 errors in 1 file (checked 1 source file)
```

Apague o bloco `try` do fim do arquivo, que já mostrou o que tinha para mostrar:

```python title="experimentos/parcial.py"
from functools import partial


def enchant(power: int, element: str, target: str) -> str:
    return f"{element} enchantment on {target} with {power} power"


fire = partial(enchant, 50, "fire")
print(fire("Sword"))
print(fire.func.__name__, fire.args, fire.keywords)
ice = partial(enchant, power=50, element="ice")
print(ice(target="Shield"))
```

```bash
python3 experimentos/parcial.py
.venv/bin/mypy --disallow-untyped-defs experimentos/parcial.py
```

```text
fire enchantment on Sword with 50 power
enchant (50, 'fire') {}
ice enchantment on Shield with 50 power
Success: no issues found in 1 source file
```

## A função

`partial_enchanter` entra depois de `spell_reducer`:

```python
def partial_enchanter(base_enchantment: Callable) -> dict[str, Callable]:
    return {
        "fire": functools.partial(base_enchantment, 50, "fire"),
        "ice": functools.partial(base_enchantment, 50, "ice"),
        "lightning": functools.partial(base_enchantment, 50, "lightning"),
    }
```

- as três versões pré-preenchem `power=50` e o elemento, como o enunciado pede. Elas preenchem
  por **posição**: a assinatura da função base, `(power, element, target)`, põe o poder e o
  elemento nas duas primeiras posições, e a versão criada é chamada só com o alvo, também por
  posição: `enchanters["fire"]("Sword")`. Pré-preencher por nome cairia na armadilha acima
  sempre que o alvo fosse passado por posição;
- o enunciado não diz quais elementos nem como entregar as três versões; a assinatura pede um
  `dict[str, Callable]`. O tutorial escolhe os elementos `fire`, `ice` e `lightning` (três dos
  elementos do gerador de dados) e usa o próprio elemento como chave.
