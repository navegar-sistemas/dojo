---
sidebar_position: 7
title: Rodar e conferir
---

# Rodar e conferir

## Comparar com o enunciado

```bash
diff <(.venv/bin/python ex1/alien_contact.py) - <<'FIM'
Alien Contact Log Validation
======================================
Valid contact report:
ID: AC_2024_001
Type: radio
Location: Area 51, Nevada
Signal: 8.5/10
Duration: 45 minutes
Witnesses: 5
Message: 'Greetings from Zeta Reticuli'

======================================
Expected validation error:
Telepathic contact requires at least 3 witnesses
FIM
```

Sem nenhuma linha impressa, a saída é a esperada
([Comparar com o enunciado, no exercício 0](../03-ex0/05-rodar-e-conferir.md#comparar-com-o-enunciado)).

## Conferir estilo e tipos

```bash
.venv/bin/flake8 ex1
.venv/bin/mypy --disallow-untyped-defs ex1
```

```text
Success: no issues found in 1 source file
```

## Testar cada regra

Como no exercício 0, um arquivo de teste tenta criar relatos a partir de um relato válido com um
campo trocado. Crie `experimentos/testar_alien_contact.py`:

```python title="experimentos/testar_alien_contact.py"
from typing import Any

from alien_contact import AlienContact, validation_message
from pydantic import ValidationError

VALID: dict[str, Any] = {
    "contact_id": "AC_2024_001",
    "timestamp": "2024-01-15T14:30:00",
    "location": "Area 51, Nevada",
    "contact_type": "radio",
    "signal_strength": 8.5,
    "duration_minutes": 45,
    "witness_count": 5,
    "message_received": "Greetings from Zeta Reticuli",
}


def attempt(label: str, changes: dict[str, Any]) -> None:
    try:
        AlienContact.model_validate(VALID | changes)
        print(f"{label}: OK")
    except ValidationError as error:
        print(f"{label}: {validation_message(error)}")


print(repr(AlienContact.model_validate(VALID)))
attempt("contact_id 'XC_2024_001'", {"contact_id": "XC_2024_001"})
attempt("contact_id 'AC1'", {"contact_id": "AC1"})
attempt("contact_type 'laser'", {"contact_type": "laser"})
attempt("duration_minutes 1441", {"duration_minutes": 1441})
attempt("physical, not verified", {"contact_type": "physical"})
attempt("physical, verified",
        {"contact_type": "physical", "is_verified": True})
attempt("telepathic, 2 witnesses",
        {"contact_type": "telepathic", "witness_count": 2})
attempt("telepathic, 3 witnesses",
        {"contact_type": "telepathic", "witness_count": 3})
attempt("signal 7.5, no message",
        {"signal_strength": 7.5, "message_received": None})
attempt("signal 7.5, empty message",
        {"signal_strength": 7.5, "message_received": ""})
attempt("signal 7.0, no message",
        {"signal_strength": 7.0, "message_received": None})
attempt("two broken rules",
        {"contact_id": "XC_2024_001", "contact_type": "physical"})
```

- o tipo de contato chega como texto (`"radio"`, `"physical"`), como num arquivo de dados, e o
  Pydantic o troca pelo membro do Enum;
- `validation_message` vem do próprio `alien_contact`: o teste mostra as mensagens como a
  demonstração as mostraria;
- cada regra é testada dos dois lados: o caso que falha e o caso logo ao lado, que passa.

```bash
PYTHONPATH=ex1 .venv/bin/python -B experimentos/testar_alien_contact.py
```

```text
AlienContact(contact_id='AC_2024_001', timestamp=datetime.datetime(2024, 1, 15, 14, 30), location='Area 51, Nevada', contact_type=<ContactType.RADIO: 'radio'>, signal_strength=8.5, duration_minutes=45, witness_count=5, message_received='Greetings from Zeta Reticuli', is_verified=False)
contact_id 'XC_2024_001': Contact ID must start with "AC" (Alien Contact)
contact_id 'AC1': String should have at least 5 characters
contact_type 'laser': Input should be 'radio', 'visual', 'physical' or 'telepathic'
duration_minutes 1441: Input should be less than or equal to 1440
physical, not verified: Physical contact reports must be verified
physical, verified: OK
telepathic, 2 witnesses: Telepathic contact requires at least 3 witnesses
telepathic, 3 witnesses: OK
signal 7.5, no message: Strong signals (> 7.0) should include received messages
signal 7.5, empty message: Strong signals (> 7.0) should include received messages
signal 7.0, no message: OK
two broken rules: Contact ID must start with "AC" (Alien Contact)
```

- as mensagens das regras saem sem o `Value error, `, e as dos campos saem como o Pydantic as
  escreve: a mesma função serve para os dois tipos de erro;
- `contact_id 'AC1'` falha no limite do campo (5 caracteres), e não na regra do `AC`: com um
  campo inválido, as regras nem rodam;
- no último caso, o relato quebra a regra 1 e a regra 2, e só a primeira aparece
  ([Uma regra de cada vez](./03-as-regras.md#uma-regra-de-cada-vez)).

```bash
.venv/bin/flake8 experimentos/testar_alien_contact.py
MYPYPATH=ex1 .venv/bin/mypy --disallow-untyped-defs experimentos/testar_alien_contact.py
```

```text
Success: no issues found in 1 source file
```
