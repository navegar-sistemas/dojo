---
sidebar_position: 2
title: O enum e o modelo
---

# O enum e o modelo

Crie o arquivo `ex1/alien_contact.py`. Ele começa pelos `import`, pelo Enum e pelos campos do
modelo, no mesmo formato do exercício 0. As próximas páginas acrescentam, nesta ordem: o
método das regras, dentro do modelo ([As regras](./03-as-regras.md)); a função da mensagem de
erro ([A mensagem do erro](./04-a-mensagem-do-erro.md)); e a demonstração
([A demonstração](./05-a-demonstracao.md)).

```python
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False
```

## Os import

Em relação ao exercício 0, entram `Enum`, do módulo `enum` da biblioteca padrão, e
`model_validator`, do Pydantic, usado na [próxima página](./03-as-regras.md).

## ContactType

Os valores dos membros são os textos do enunciado, em minúsculas: `"radio"`, `"visual"`,
`"physical"` e `"telepathic"`. São esses textos que chegam nos dados de fora e que a saída
mostra (`Type: radio`). Os nomes dos membros, em maiúsculas, são o costume do Python para
constantes.

## Os campos

Cada campo segue a tabela do enunciado, como no exercício 0:

- `contact_type: ContactType` aceita um membro do Enum ou o valor dele em texto
  ([Enum](../02-conceitos/05-enum.md#o-que-aconteceu));
- `message_received` é o campo opcional, de até 500 caracteres;
- `is_verified` tem o padrão `False`: um relato só é verificado quando alguém diz que é.

`timestamp`, o momento do contato, é um campo como os outros: o nome não tem nada de especial
para o Pydantic.
