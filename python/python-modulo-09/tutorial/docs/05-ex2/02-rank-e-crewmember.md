---
sidebar_position: 2
title: Rank e CrewMember
---

# Rank e CrewMember

Crie o arquivo `ex2/space_crew.py`. Ele começa pelos mesmos `import` do exercício 1, pelo Enum
das patentes e pelo modelo do tripulante. As próximas páginas acrescentam `SpaceMission`, as
regras e a demonstração, sempre no fim do arquivo.

```python
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True
```

## Rank

Os valores são os textos do enunciado, em minúsculas, como em `ContactType`
([O enum e o modelo](../04-ex1/02-o-enum-e-o-modelo.md#contacttype)). A saída mostra o valor
entre parênteses: `(commander)`.

## CrewMember

`CrewMember` é um modelo comum, como `SpaceStation`: cada campo segue a tabela do enunciado, e
`is_active` tem o padrão `True`. O modelo não tem regras próprias; as regras que envolvem a
tripulação são da missão, que enxerga todos os tripulantes juntos.

Um `CrewMember` pode ser criado sozinho, pelo construtor ou por `model_validate`, e é validado
por inteiro. A [próxima página](./03-spacemission.md) o usa como tipo de um campo.
