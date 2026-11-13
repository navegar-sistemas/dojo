---
sidebar_position: 5
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(.venv/bin/python ex0/space_station.py) - <<'FIM'
Space Station Data Validation
========================================
Valid station created:
ID: ISS001
Name: International Space Station
Crew: 6 people
Power: 85.5%
Oxygen: 92.3%
Status: Operational

========================================
Expected validation error:
Input should be less than or equal to 20
FIM
```

- `<(.venv/bin/python ex0/space_station.py)` entrega ao `diff` a saída do programa como se fosse
  um arquivo;
- o `-` diz ao `diff` para ler o segundo texto da entrada do comando, em vez de um arquivo;
- `<<'FIM'` escreve nessa entrada as linhas seguintes, até a linha `FIM`: a saída copiada do
  enunciado. Cole o bloco inteiro, até a linha `FIM`; sem ela, o terminal fica esperando mais
  linhas;
- o `diff` compara os dois textos linha a linha e só imprime as diferenças.

Sem nenhuma linha impressa, a saída é a esperada, inclusive a linha vazia antes do segundo
separador.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex0
.venv/bin/mypy --disallow-untyped-defs ex0
```

```text
Success: no issues found in 1 source file
```

O flake8 não imprime nada, e o mypy não acha problema.

## Testar cada limite

A demonstração só testa o limite da tripulação. Um arquivo de teste em `experimentos/` testa os
outros campos, sem mexer no arquivo entregue. Crie `experimentos/testar_space_station.py`:

```python title="experimentos/testar_space_station.py"
from typing import Any

from pydantic import ValidationError
from space_station import SpaceStation

VALID: dict[str, Any] = {
    "station_id": "ISS001",
    "name": "International Space Station",
    "crew_size": 6,
    "power_level": 85.5,
    "oxygen_level": 92.3,
    "last_maintenance": "2024-01-15T10:30:00",
}


def attempt(label: str, changes: dict[str, Any]) -> None:
    try:
        SpaceStation.model_validate(VALID | changes)
        print(f"{label}: OK")
    except ValidationError as error:
        print(f"{label}: {error.errors()[0]['msg']}")


print(repr(SpaceStation.model_validate(VALID)))
attempt("station_id 'AB'", {"station_id": "AB"})
attempt("station_id with 11 characters", {"station_id": "ISS00000001"})
attempt("empty name", {"name": ""})
attempt("crew_size 0", {"crew_size": 0})
attempt("crew_size 20", {"crew_size": 20})
attempt("power_level -0.1", {"power_level": -0.1})
attempt("oxygen_level 100.0", {"oxygen_level": 100.0})
attempt("oxygen_level 100.1", {"oxygen_level": 100.1})
attempt("last_maintenance 'soon'", {"last_maintenance": "soon"})
attempt("notes with 200 characters", {"notes": "x" * 200})
attempt("notes with 201 characters", {"notes": "x" * 201})
```

- `from space_station import SpaceStation` importa o modelo do arquivo `ex0/space_station.py`.
  O `if __name__ == "__main__":` impede que a demonstração rode nesse `import`;
- `VALID` é o relatório da estação válida, como chegaria de fora: com a data em texto. O nome em
  maiúsculas é o costume do Python para um valor que não muda;
- `VALID | changes` junta dois dicionários num novo: as chaves de `changes` substituem as de
  `VALID`, e `VALID` continua igual. Cada teste muda só um campo;
- cada linha de `attempt` testa um limite: o valor logo fora (que deve falhar) ou o próprio limite
  (que deve passar).

O Python procura os módulos importados na pasta do arquivo rodado (`experimentos`), e não na
`ex0`. A variável **`PYTHONPATH`**, escrita antes do comando, acrescenta a pasta `ex0` à
procura. O `-B` impede que o Python grave na pasta `ex0` a pasta de cache `__pycache__`, que ele
cria ao importar um arquivo:

```bash
PYTHONPATH=ex0 .venv/bin/python -B experimentos/testar_space_station.py
```

```text
SpaceStation(station_id='ISS001', name='International Space Station', crew_size=6, power_level=85.5, oxygen_level=92.3, last_maintenance=datetime.datetime(2024, 1, 15, 10, 30), is_operational=True, notes=None)
station_id 'AB': String should have at least 3 characters
station_id with 11 characters: String should have at most 10 characters
empty name: String should have at least 1 character
crew_size 0: Input should be greater than or equal to 1
crew_size 20: OK
power_level -0.1: Input should be greater than or equal to 0
oxygen_level 100.0: OK
oxygen_level 100.1: Input should be less than or equal to 100
last_maintenance 'soon': Input should be a valid datetime or date, input is too short
notes with 200 characters: OK
notes with 201 characters: String should have at most 200 characters
```

- a primeira linha mostra a estação válida: a data em texto virou `datetime`, e os dois campos
  que ficaram de fora têm os padrões `True` e `None`;
- cada limite recusa o valor logo fora dele e aceita o próprio limite.

O mypy também precisa achar o `space_station`. Para ele, a variável é a **`MYPYPATH`**:

```bash
.venv/bin/flake8 experimentos/testar_space_station.py
MYPYPATH=ex0 .venv/bin/mypy --disallow-untyped-defs experimentos/testar_space_station.py
```

```text
Success: no issues found in 1 source file
```
