---
sidebar_position: 6
title: O arquivo completo
---

# O arquivo completo

O Enum, os dois modelos, a função da mensagem e a demonstração, nesta ordem:

```python title="ex2/space_crew.py"
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

    @model_validator(mode="after")
    def check_safety_requirements(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
        leaders = 0
        experienced = 0
        inactive = 0
        for member in self.crew:
            if member.rank in (Rank.COMMANDER, Rank.CAPTAIN):
                leaders += 1
            if member.years_experience >= 5:
                experienced += 1
            if not member.is_active:
                inactive += 1
        if leaders == 0:
            raise ValueError(
                "Mission must have at least one Commander or Captain")
        # "At least half the crew", in integers: experienced / size >= 0.5.
        if self.duration_days > 365 and experienced * 2 < len(self.crew):
            raise ValueError("Long missions (> 365 days) need 50% "
                             "experienced crew (5+ years)")
        if inactive > 0:
            raise ValueError("All crew members must be active")
        return self


def validation_message(error: ValidationError) -> str:
    detail = error.errors()[0]
    # A ValueError raised by a validator shows up in msg as
    # "Value error, <text>"; ctx keeps the original exception.
    if detail["type"] == "value_error":
        return str(detail["ctx"]["error"])
    return detail["msg"]


def show_mission(mission: SpaceMission) -> None:
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(f"- {member.name} ({member.rank.value}) - "
              f"{member.specialization}")


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 41)
    mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime(2024, 9, 1),
        duration_days=900,
        crew=[
            CrewMember(member_id="CM001", name="Sarah Connor",
                       rank=Rank.COMMANDER, age=45,
                       specialization="Mission Command",
                       years_experience=20),
            CrewMember(member_id="CM002", name="John Smith",
                       rank=Rank.LIEUTENANT, age=36,
                       specialization="Navigation", years_experience=12),
            CrewMember(member_id="CM003", name="Alice Johnson",
                       rank=Rank.OFFICER, age=29,
                       specialization="Engineering", years_experience=4),
        ],
        budget_millions=2500.0,
    )
    print("Valid mission created:")
    show_mission(mission)
    print()
    print("=" * 41)
    try:
        SpaceMission(
            mission_id="M2024_LUNA",
            mission_name="Lunar Survey",
            destination="Moon",
            launch_date=datetime(2024, 11, 1),
            duration_days=30,
            crew=[
                CrewMember(member_id="CM004", name="Maria Garcia",
                           rank=Rank.LIEUTENANT, age=33,
                           specialization="Pilot", years_experience=9),
                CrewMember(member_id="CM005", name="David Brown",
                           rank=Rank.CADET, age=22,
                           specialization="Research", years_experience=1),
            ],
            budget_millions=150.0,
        )
    except ValidationError as error:
        print("Expected validation error:")
        print(validation_message(error))


if __name__ == "__main__":
    main()
```

O que o arquivo usa: `pydantic` (`BaseModel`, `Field`, `ValidationError` e `model_validator`),
`datetime` e `enum` (`Enum`), da biblioteca padrão, as funções embutidas `print`, `len` e `str`,
e o método de texto `startswith`. Nenhum outro `import`.
