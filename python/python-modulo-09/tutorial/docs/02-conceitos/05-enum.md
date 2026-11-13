---
sidebar_position: 5
title: Enum
---

# Enum

Alguns campos só aceitam alguns valores: o tipo de um contato é `radio`, `visual`, `physical` ou
`telepathic`, e nada mais. Um campo `str` aceitaria `"laser"` ou `"Radio"` sem reclamar. O tipo
certo para uma lista fechada de valores é o **Enum** (de *enumeration*, "enumeração"), do módulo
`enum` da biblioteca padrão.

## Uma classe Enum

Um Enum é uma classe que herda de `Enum` e lista os valores permitidos, chamados **membros**,
como atributos de classe (escritos no corpo da classe, fora de qualquer método):

```python
class Signal(Enum):
    RADIO = "radio"
    LIGHT = "light"
```

Cada membro tem um **nome** (`RADIO`, em maiúsculas por costume) e um **valor** (`"radio"`).
`Signal.RADIO` é o membro; `Signal.RADIO.value` é o texto `"radio"`.

## O experimento

Crie `experimentos/enumeracao.py`:

```python title="experimentos/enumeracao.py"
from enum import Enum

from pydantic import BaseModel, ValidationError


class Signal(Enum):
    RADIO = "radio"
    LIGHT = "light"


class Report(BaseModel):
    signal: Signal


print(Signal.RADIO, Signal.RADIO.name, Signal.RADIO.value)
print(Signal("light"))
print(list(Signal))
report = Report.model_validate({"signal": "radio"})
print(repr(report))
print(report.signal is Signal.RADIO)
try:
    Report.model_validate({"signal": "laser"})
except ValidationError as error:
    print(error.errors()[0]["msg"])
```

```bash
.venv/bin/python experimentos/enumeracao.py
```

```text
Signal.RADIO RADIO radio
Signal.LIGHT
[<Signal.RADIO: 'radio'>, <Signal.LIGHT: 'light'>]
Report(signal=<Signal.RADIO: 'radio'>)
True
Input should be 'radio' or 'light'
```

## O que aconteceu

- `print(Signal.RADIO)` mostra o membro como `Classe.NOME`; `.name` e `.value` dão o nome e o
  valor;
- `Signal("light")` procura o membro pelo **valor** e devolve `Signal.LIGHT`;
- `list(Signal)` lista todos os membros, na ordem em que foram escritos;
- o campo `signal: Signal` recebeu o texto `"radio"`, e o Pydantic o trocou pelo membro
  `Signal.RADIO`, procurando pelo valor. `is` confere que é o próprio membro;
- `"laser"` não é o valor de nenhum membro, e a mensagem lista os valores aceitos: `Input should
  be 'radio' or 'light'` ("a entrada deveria ser `'radio'` ou `'light'`").

Para comparar um campo Enum, use o membro: `report.signal is Signal.RADIO`. O membro não é igual
ao texto: `Signal.RADIO == "radio"` dá `False`. Para mostrar o texto, use `.value`.

## No projeto

Os exercícios 1 e 2 pedem um Enum cada um: `ContactType`, com os tipos de contato, e `Rank`, com
as patentes da tripulação ([O enum e o modelo](../04-ex1/02-o-enum-e-o-modelo.md)). A saída
mostra o valor (`Type: radio`, `(commander)`), e por isso o código imprime `.value`.

```bash
.venv/bin/flake8 experimentos/enumeracao.py
.venv/bin/mypy --disallow-untyped-defs experimentos/enumeracao.py
```

```text
Success: no issues found in 1 source file
```
