---
sidebar_position: 6
title: O arquivo completo
---

# O arquivo completo

O Enum, o modelo com as regras, a função da mensagem e a demonstração, nesta ordem:

```python title="ex1/alien_contact.py"
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

    # Runs only after every field passed its own checks, so all the
    # attributes of self already hold valid values here.
    @model_validator(mode="after")
    def check_business_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC" (Alien Contact)')
        if self.contact_type is ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (self.contact_type is ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages")
        return self


def validation_message(error: ValidationError) -> str:
    detail = error.errors()[0]
    # A ValueError raised by a validator shows up in msg as
    # "Value error, <text>"; ctx keeps the original exception.
    if detail["type"] == "value_error":
        return str(detail["ctx"]["error"])
    return detail["msg"]


def show_contact(contact: AlienContact) -> None:
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    if contact.message_received is not None:
        print(f"Message: '{contact.message_received}'")


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 38)
    contact = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime(2024, 1, 15, 14, 30),
        location="Area 51, Nevada",
        contact_type=ContactType.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli",
    )
    print("Valid contact report:")
    show_contact(contact)
    print()
    print("=" * 38)
    try:
        AlienContact(
            contact_id="AC_2024_002",
            timestamp=datetime(2024, 1, 16, 9, 15),
            location="Roswell, New Mexico",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=6.2,
            duration_minutes=30,
            witness_count=1,
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(validation_message(error))


if __name__ == "__main__":
    main()
```

O que o arquivo usa: `pydantic` (`BaseModel`, `Field`, `ValidationError` e `model_validator`),
`datetime` e `enum` (`Enum`), da biblioteca padrão, as funções embutidas `print` e `str`, e o
método de texto `startswith`. Nenhum outro `import`.
