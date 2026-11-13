---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(.venv/bin/python ex2/space_crew.py) - <<'FIM'
Space Mission Crew Validation
=========================================
Valid mission created:
Mission: Mars Colony Establishment
ID: M2024_MARS
Destination: Mars
Duration: 900 days
Budget: $2500.0M
Crew size: 3
Crew members:
- Sarah Connor (commander) - Mission Command
- John Smith (lieutenant) - Navigation
- Alice Johnson (officer) - Engineering

=========================================
Expected validation error:
Mission must have at least one Commander or Captain
FIM
```

Sem nenhuma linha impressa, a saída é a esperada.

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex2
.venv/bin/mypy --disallow-untyped-defs ex2
```

```text
Success: no issues found in 1 source file
```

## Testar cada regra

As missões do teste chegam como dicionários, com os tripulantes também como dicionários, como
viriam de um arquivo JSON. Crie `experimentos/testar_space_crew.py`:

```python title="experimentos/testar_space_crew.py"
from typing import Any

from pydantic import ValidationError
from space_crew import SpaceMission, validation_message

BASE: dict[str, Any] = {
    "mission_id": "M2024_TEST",
    "mission_name": "Test Mission",
    "destination": "Moon",
    "launch_date": "2024-09-01T00:00:00",
    "duration_days": 30,
    "budget_millions": 100.0,
}


def member(rank: str, years: int, active: bool = True) -> dict[str, Any]:
    return {"member_id": "CM001", "name": "Test Crew", "rank": rank,
            "age": 30, "specialization": "Research",
            "years_experience": years, "is_active": active}


def attempt(label: str, crew: list[dict[str, Any]],
            changes: dict[str, Any]) -> None:
    try:
        SpaceMission.model_validate(BASE | {"crew": crew} | changes)
        print(f"{label}: OK")
    except ValidationError as error:
        print(f"{label}: {validation_message(error)}")
        location = error.errors()[0]["loc"]
        if location:
            print(f"    loc: {location}")


leader = member("captain", 10)
attempt("valid", [leader], {})
attempt("mission_id 'X2024_TEST'", [leader], {"mission_id": "X2024_TEST"})
attempt("no commander or captain", [member("lieutenant", 10)], {})
attempt("400 days, 1 of 3 experienced",
        [leader, member("cadet", 1), member("cadet", 2)],
        {"duration_days": 400})
attempt("400 days, 2 of 4 experienced",
        [leader, member("officer", 5), member("cadet", 1), member("cadet", 2)],
        {"duration_days": 400})
attempt("365 days, 1 of 3 experienced",
        [leader, member("cadet", 1), member("cadet", 2)],
        {"duration_days": 365})
attempt("inactive member", [leader, member("officer", 3, False)], {})
attempt("empty crew", [], {})
attempt("13 members", [leader] * 13, {})
attempt("member aged 17", [leader, member("cadet", 0) | {"age": 17}], {})
attempt("rank 'admiral'", [member("admiral", 10)], {})
```

- `BASE` tem os campos da missão, menos a tripulação, que cada teste monta;
- `member` monta o dicionário de um tripulante com a patente, os anos de experiência e, se
  preciso, `active=False`. Os outros campos são fixos e válidos;
- `attempt` junta a missão, a tripulação e as mudanças do teste. Quando o erro tem um caminho
  (`loc` não vazio), imprime o caminho também. Uma tupla vazia conta como falsa num `if`, e os
  erros das regras, que têm `loc` igual a `()`, não imprimem a linha;
- `[leader] * 13` é uma lista com 13 vezes o mesmo tripulante;
- `member("cadet", 0) | {"age": 17}` é um tripulante com 17 anos, abaixo do limite de 18.

```bash
PYTHONPATH=ex2 .venv/bin/python -B experimentos/testar_space_crew.py
```

```text
valid: OK
mission_id 'X2024_TEST': Mission ID must start with "M"
no commander or captain: Mission must have at least one Commander or Captain
400 days, 1 of 3 experienced: Long missions (> 365 days) need 50% experienced crew (5+ years)
400 days, 2 of 4 experienced: OK
365 days, 1 of 3 experienced: OK
inactive member: All crew members must be active
empty crew: List should have at least 1 item after validation, not 0
    loc: ('crew',)
13 members: List should have at most 12 items after validation, not 13
    loc: ('crew',)
member aged 17: Input should be greater than or equal to 18
    loc: ('crew', 1, 'age')
rank 'admiral': Input should be 'cadet', 'officer', 'lieutenant', 'captain' or 'commander'
    loc: ('crew', 0, 'rank')
```

- as quatro regras falham quando devem e passam nos casos de borda: 2 de 4 é exatamente metade,
  e passa; 365 dias não é "mais de 365", e a regra da experiência nem se aplica;
- os limites da lista contam tripulantes (`'crew'` no `loc`);
- um erro **dentro** de um tripulante aparece na missão com o caminho completo: o tripulante de
  posição 1, campo `age`. É a resposta, na prática, à pergunta do enunciado sobre um `CrewMember`
  que falha dentro de uma `SpaceMission`
  ([Perguntas de revisão](../07-fechamento/03-perguntas-de-revisao.md)).

```bash
.venv/bin/flake8 experimentos/testar_space_crew.py
MYPYPATH=ex2 .venv/bin/mypy --disallow-untyped-defs experimentos/testar_space_crew.py
```

```text
Success: no issues found in 1 source file
```
