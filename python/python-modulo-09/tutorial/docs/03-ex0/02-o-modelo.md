---
sidebar_position: 2
title: O modelo SpaceStation
---

# O modelo SpaceStation

Crie o arquivo `ex0/space_station.py` e escreva nele os `import` e o modelo. A
[próxima página](./03-a-demonstracao.md) acrescenta, no fim do arquivo, as funções da
demonstração.

```python
from datetime import datetime

from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    # Text such as "2024-01-15T10:30:00" is also accepted and converted.
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)
```

## Os import

- `datetime`, do módulo `datetime`, é o tipo do campo de data e hora;
- de `pydantic` vêm `BaseModel`, a classe base do modelo, `Field`, para os limites, e
  `ValidationError`, a exceção que a demonstração captura.

A ordem segue o costume do Python: primeiro os módulos da biblioteca padrão, depois uma linha em
branco, depois as bibliotecas instaladas.

## Campo a campo

Cada linha do enunciado vira uma linha do modelo:

| Enunciado | No modelo |
|---|---|
| *String, 3-10 characters* | `str` com `Field(min_length=3, max_length=10)` |
| *Integer, 1-20 people* | `int` com `Field(ge=1, le=20)` |
| *Float, 0.0-100.0 percent* | `float` com `Field(ge=0.0, le=100.0)` |
| *DateTime field* | `datetime`, sem limites |
| *Boolean, defaults to True* | `bool = True` |
| *Optional string, max 200 characters* | `str \| None = Field(default=None, max_length=200)` |

- os limites são fechados: "de 1 a 20" aceita o 1 e o 20, e por isso `ge` e `le` ("maior ou
  igual", "menor ou igual"), e não `gt` e `lt`;
- os seis primeiros campos não têm valor padrão, e por isso são **obrigatórios**: um relatório
  sem qualquer um deles é recusado com `Field required`;
- `is_operational` tem o padrão `True`, e `notes` o padrão `None`: os dois podem ficar de fora;
- `notes` é o campo opcional: aceita um texto de até 200 caracteres ou `None`
  ([Campo opcional](../02-conceitos/03-field-e-restricoes.md#campo-opcional)).

O comentário em inglês, em cima de `last_maintenance`, registra o que a
[conversão de tipos](../02-conceitos/04-conversao-de-tipos.md) faz com esse campo. O enunciado
pede que o código documente o aprendizado com comentários; os comentários do tutorial explicam o
que o código sozinho não mostra.

## O que o Pydantic faz com isso

A classe não tem nenhum `if`, nenhum `raise` e nenhum `__init__`. Todo o trabalho de conferir
vem do `BaseModel`, que lê os tipos e os `Field` de cada linha. Uma `SpaceStation` criada com
sucesso tem todos os campos dentro dos limites, e um valor fora deles nunca chega a virar
objeto.
