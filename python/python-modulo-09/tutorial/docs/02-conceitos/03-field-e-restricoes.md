---
sidebar_position: 3
title: Field e restrições
---

# Field e restrições

O tipo de um campo diz **que** valor ele aceita (um `int`, um `str`), mas não **quanto**: uma
tripulação de 25 pessoas é um `int` perfeito, e mesmo assim não cabe numa estação de 20. Os
limites de cada campo são as **restrições**, e entram com a função **`Field`**, do Pydantic.

## As restrições do projeto

`Field(...)` vai no lugar do valor padrão do campo, depois do `=`, e recebe as restrições pelo
nome:

| Restrição | Vale para | Quer dizer |
|---|---|---|
| `min_length=3` | textos (e listas) | pelo menos 3 caracteres (ou itens) |
| `max_length=10` | textos (e listas) | no máximo 10 caracteres (ou itens) |
| `ge=1` | números | maior ou igual a 1 (*greater or equal*) |
| `le=20` | números | menor ou igual a 20 (*less or equal*) |
| `default=None` | qualquer campo | o valor padrão, quando o campo fica de fora |

Os limites do enunciado são todos fechados ("de 1 a 20 pessoas" aceita o 1 e o 20), e por isso o
projeto usa `ge` e `le`. Para limites abertos existem `gt` ("maior que") e `lt` ("menor que").

## Campo opcional

Um campo **opcional** pode ficar sem valor. No Pydantic, isso se escreve com o tipo
`str | None` ("um texto **ou** `None`") e o padrão `None`:

```python
note: str | None = Field(default=None, max_length=10)
```

O `|` entre dois tipos forma uma **união**: o campo aceita um ou outro. A restrição
`max_length=10` vale para o texto; o `None` passa sem ela. Quando não há restrição nenhuma, o
`Field` não é preciso: `note: str | None = None`.

## O experimento

Crie `experimentos/restricoes.py`:

```python title="experimentos/restricoes.py"
from typing import Any

from pydantic import BaseModel, Field, ValidationError


class Probe(BaseModel):
    code: str = Field(min_length=3, max_length=6)
    fuel: float = Field(ge=0.0, le=100.0)
    crew: int = Field(ge=0, le=4)
    active: bool = True
    note: str | None = Field(default=None, max_length=10)


def attempt(data: dict[str, Any]) -> None:
    try:
        probe = Probe.model_validate(data)
        print(f"OK: {probe}")
    except ValidationError as error:
        print(f"{error.error_count()} errors:")
        for detail in error.errors():
            print(f"  {detail['loc'][0]}: {detail['msg']}")


attempt({"code": "VOY1", "fuel": 50.0, "crew": 0})
attempt({"code": "VOY1", "fuel": 100.0, "crew": 4, "note": "all good"})
attempt({"code": "V", "fuel": 100.5, "crew": 5, "note": "a" * 11})
attempt({"code": "VOYAGER", "fuel": -1.0, "crew": 2, "note": None})
```

- `Any` vem do módulo `typing`, da biblioteca padrão. Como type hint, quer dizer "qualquer tipo":
  `dict[str, Any]` é um dicionário com chaves `str` e valores de qualquer tipo, que é o que um
  dado de fora costuma ser;
- `attempt` tenta criar o objeto e imprime `OK` com os campos, ou cada erro com o nome do campo
  (`detail['loc'][0]`, o primeiro passo do caminho) e a mensagem. Dentro da f-string de aspas
  duplas, as chaves do dicionário vão entre aspas simples;
- `"a" * 11` é um texto com 11 letras `a`.

```bash
.venv/bin/python experimentos/restricoes.py
```

```text
OK: code='VOY1' fuel=50.0 crew=0 active=True note=None
OK: code='VOY1' fuel=100.0 crew=4 active=True note='all good'
4 errors:
  code: String should have at least 3 characters
  fuel: Input should be less than or equal to 100
  crew: Input should be less than or equal to 4
  note: String should have at most 10 characters
2 errors:
  code: String should have at most 6 characters
  fuel: Input should be greater than or equal to 0
```

## O que aconteceu

- os dois primeiros objetos passam. `crew=0` e `crew=4` estão nos limites, e os limites são
  aceitos. `active` e `note` ficaram com os valores padrão no primeiro;
- o terceiro tem quatro problemas, e o Pydantic lista os quatro de uma vez;
- no quarto, `note=None` passa: o `None` é um valor permitido do campo opcional.

As mensagens seguem um padrão: `String should have at least 3 characters` ("o texto deveria ter
pelo menos 3 caracteres"), `Input should be less than or equal to 100` ("a entrada deveria ser
menor ou igual a 100"), `Input should be greater than or equal to 0` ("maior ou igual a 0"). O
limite `100.0` aparece como `100`, sem a parte decimal.

## No projeto

O modelo do exercício 0 tem um campo de cada jeito: textos com `min_length` e `max_length`,
números com `ge` e `le`, um `bool` com padrão e um texto opcional
([O modelo SpaceStation](../03-ex0/02-o-modelo.md)).

```bash
.venv/bin/flake8 experimentos/restricoes.py
.venv/bin/mypy --disallow-untyped-defs experimentos/restricoes.py
```

```text
Success: no issues found in 1 source file
```
