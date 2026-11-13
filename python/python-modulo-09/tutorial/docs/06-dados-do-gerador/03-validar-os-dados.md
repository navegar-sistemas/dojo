---
sidebar_position: 3
title: Validar os dados
---

# Validar os dados

Com os três modelos prontos e os dados gerados, falta passar cada registro pelo modelo certo e ver
quais são aceitos. Um experimento lê os arquivos JSON e valida registro por registro, com os
modelos importados dos três exercícios.

## O experimento

Crie `experimentos/validar_gerados.py`:

```python title="experimentos/validar_gerados.py"
import json
from typing import Any

from alien_contact import AlienContact
from pydantic import BaseModel, ValidationError
from space_crew import SpaceMission, validation_message
from space_station import SpaceStation

FOLDER = "tools/generated_data"


def check_file(name: str, model: type[BaseModel], key: str) -> None:
    with open(f"{FOLDER}/{name}", encoding="utf-8") as file:
        records: list[dict[str, Any]] = json.load(file)
    print(f"{name}: {len(records)} records")
    for record in records:
        try:
            model.model_validate(record)
            print(f"  OK       {record[key]}")
        except ValidationError as error:
            print(f"  REJECTED {record[key]} "
                  f"(error_count={error.error_count()}): "
                  f"{validation_message(error)}")


def main() -> None:
    check_file("space_stations.json", SpaceStation, "station_id")
    check_file("invalid_stations.json", SpaceStation, "station_id")
    check_file("alien_contacts.json", AlienContact, "contact_id")
    check_file("invalid_contacts.json", AlienContact, "contact_id")
    check_file("space_missions.json", SpaceMission, "mission_id")


if __name__ == "__main__":
    main()
```

- `json` é o módulo da biblioteca padrão que lê e escreve JSON. O enunciado permite importar os
  dados JSON e CSV da pasta de ferramentas;
- `with open(...) as file:` abre o arquivo para leitura e o fecha sozinho no fim do bloco.
  `encoding="utf-8"` diz como os caracteres estão gravados;
- `json.load(file)` lê o JSON e devolve o valor em Python: aqui, uma lista de dicionários. O
  type hint `list[dict[str, Any]]` registra isso, porque o `json.load` não diz o tipo do que leu;
- o parâmetro `model` recebe a **classe** do modelo, e não um objeto: `type[BaseModel]` quer dizer
  "`BaseModel` ou qualquer classe filha dela". Assim a mesma função valida estações, relatos e
  missões, chamando `model.model_validate(record)`;
- `key` é o campo usado para identificar o registro na saída;
- `validation_message` vem do `space_crew`; é a mesma função do exercício 1
  ([A mensagem do erro](../04-ex1/04-a-mensagem-do-erro.md)).

O experimento importa dos três exercícios. O `PYTHONPATH` aceita várias pastas, separadas por
`:` ([Testar cada limite](../03-ex0/05-rodar-e-conferir.md#testar-cada-limite)):

```bash
PYTHONPATH=ex0:ex1:ex2 .venv/bin/python -B experimentos/validar_gerados.py
```

```text
space_stations.json: 10 records
  OK       LGW125
  OK       QCH189
  OK       ISS674
  OK       ISS877
  OK       LGW194
  OK       ISS847
  OK       QCH400
  OK       ERS891
  OK       ABR266
  OK       LGW723
invalid_stations.json: 2 records
  REJECTED TOOLONG123456 (error_count=2): String should have at most 10 characters
  REJECTED TS (error_count=5): String should have at least 3 characters
alien_contacts.json: 15 records
  OK       AC_2024_001
  OK       AC_2024_002
  OK       AC_2024_003
  OK       AC_2024_004
  OK       AC_2024_005
  OK       AC_2024_006
  OK       AC_2024_007
  OK       AC_2024_008
  OK       AC_2024_009
  OK       AC_2024_010
  OK       AC_2024_011
  OK       AC_2024_012
  OK       AC_2024_013
  OK       AC_2024_014
  OK       AC_2024_015
invalid_contacts.json: 2 records
  REJECTED WRONG_FORMAT (error_count=1): Contact ID must start with "AC" (Alien Contact)
  REJECTED AC_2024_002 (error_count=1): Telepathic contact requires at least 3 witnesses
space_missions.json: 5 records
  OK       M2024_TITAN
  OK       M2024_MARS
  OK       M2024_EUROPA
  OK       M2024_LUNA
  OK       M2024_EUROPA
```

## O que os dados mostram

**Todos os registros normais passam**: 10 estações, 15 relatos e 5 missões, com as datas em
texto convertidas, os tipos de contato e as patentes trocados pelos membros dos Enums, e os
tripulantes de cada missão validados como `CrewMember`.

**Os casos inválidos são recusados**, e a contagem mostra a diferença entre os dois tipos de
erro:

- `TOOLONG123456` tem 2 erros de campo (o ID com 13 caracteres e a tripulação de 25), e `TS` tem
  5. Os erros de campo são todos conferidos e contados juntos
  ([ValidationError](../02-conceitos/02-validationerror.md#o-que-a-validationerror-traz));
- `WRONG_FORMAT` quebra duas regras de negócio (o ID sem `AC` e o sinal forte sem mensagem), mas
  tem `error_count=1`: o método das regras para no primeiro `raise`
  ([Uma regra de cada vez](../04-ex1/03-as-regras.md#uma-regra-de-cada-vez)).

**Uma diferença de leitura que os dados não mostram.** Para a regra das missões longas, o gerador
garante `len(crew) // 2` tripulantes experientes: com 5 tripulantes, 2 bastam para ele. Pela
leitura do tutorial, "50%" é pelo menos metade, e com 5 tripulantes são necessários 3
([As regras da missão](../05-ex2/04-as-regras-da-missao.md#regra-a-regra)). Nas 5 missões geradas a
diferença não aparece: todas passam.

```bash
.venv/bin/flake8 experimentos/validar_gerados.py
MYPYPATH=ex0:ex1:ex2 .venv/bin/mypy --disallow-untyped-defs experimentos/validar_gerados.py
```

```text
Success: no issues found in 1 source file
```
