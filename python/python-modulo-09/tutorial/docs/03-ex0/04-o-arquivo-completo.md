---
sidebar_position: 4
title: O arquivo completo
---

# O arquivo completo

```python title="ex0/space_station.py"
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


def show_station(station: SpaceStation) -> None:
    status = "Operational" if station.is_operational else "Non-operational"
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Status: {status}")


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)
    station = SpaceStation(
        station_id="ISS001",
        name="International Space Station",
        crew_size=6,
        power_level=85.5,
        oxygen_level=92.3,
        last_maintenance=datetime(2024, 1, 15, 10, 30),
    )
    print("Valid station created:")
    show_station(station)
    print()
    print("=" * 40)
    try:
        # crew_size=25 is above le=20: Pydantic refuses to build the object.
        SpaceStation(
            station_id="ISS002",
            name="Overcrowded Station",
            crew_size=25,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime(2024, 1, 15, 10, 30),
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(error.errors()[0]["msg"])


if __name__ == "__main__":
    main()
```

O que o arquivo usa: `pydantic` (`BaseModel`, `Field` e `ValidationError`), o tipo `datetime` do
módulo `datetime` da biblioteca padrão e a função embutida `print`. Nenhum outro `import`.
