---
sidebar_position: 3
title: SpaceMission
---

# SpaceMission

O modelo da missão entra depois de `CrewMember`. Nesta página, só os campos; as regras vêm na
[próxima](./04-as-regras-da-missao.md), dentro da mesma classe.

```python
class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    # Each item goes through the whole CrewMember validation.
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)
```

## O campo crew

`crew: list[CrewMember]` é o campo aninhado: uma lista em que cada item é um `CrewMember`.

- `min_length=1` e `max_length=12` contam **tripulantes**: de 1 a 12, como o enunciado pede;
- cada item passa pela validação inteira de `CrewMember`: tipos, limites e Enum. Um item que
  chega como dicionário vira um objeto `CrewMember`; um item inválido recusa a missão inteira, com
  o caminho até o erro no `loc`, como `('crew', 1, 'age')`
  ([Modelos aninhados](../02-conceitos/07-modelos-aninhados.md#o-que-aconteceu));
- dentro da missão, `self.crew[0].rank` é a patente do primeiro tripulante, já como membro de
  `Rank`.

## A ordem dos campos

`mission_status` tem o padrão `"planned"` e vem antes de `budget_millions`, que é obrigatório.
Numa função comum do Python, um parâmetro com padrão não pode vir antes de um sem padrão; num
modelo do Pydantic pode, porque os campos são sempre passados pelo nome. Os campos seguem a ordem
do enunciado.

`mission_status` é um texto livre: o enunciado só fixa o padrão, e não uma lista de estados
possíveis.
