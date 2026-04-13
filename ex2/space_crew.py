from enum import Enum
from typing_extensions import Self
from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime


class CrewRank(Enum):
    cadet = 1
    officer = 2
    lieutenant = 3
    captain = 4
    commander = 5


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Enum
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=300)
    destination: str = Field(min_length=3, max_length=50)
    lauch_date: datetime
    duration_days: int = Field(ge=1, le=3560)
    crew: list
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def mission_validation(self) -> Self:
        if self.mission_id.startswith("M") is False:
            raise ValueError("Mission ID must start with 'M'")
        status = False
        experienced_crew = 0
        for crew_member in self.crew:
            if crew_member.is_active is False:
                raise ValueError("All crew members must be active")
            if crew_member.rank.value == 5 or crew_member.rank.value == 4:
                status = True
            if crew_member.years_experience >= 5:
                experienced_crew += 1
        if status is False:
            raise ValueError(
                "Mission must have at least one commander or Captain"
            )
        if self.duration_days > 365:
            if experienced_crew / len(self.crew) < 0.5:
                raise ValueError(
                    "Long mission (>365 days) need "
                    "50% experienced crew (5+ years)"
                )
        return self


def main() -> None:
    sarah = CrewMember(
        member_id="32_acdf",
        name="Sarah Connor",
        rank=CrewRank.commander,
        age=45,
        specialization="Mission command",
        years_experience=15,
        is_active=True,
    )
    john = CrewMember(
        member_id="34_bfgd",
        name="John Smith",
        rank=CrewRank.lieutenant,
        age=32,
        specialization="Navigation",
        years_experience=12,
        is_active=True,
    )
    alice = CrewMember(
        member_id="568_rtfg",
        name="Alice Johnson",
        rank=CrewRank.officer,
        age=27,
        specialization="Engineering",
        years_experience=5,
        is_active=True,
    )
    crew_people = [sarah, john, alice]
    valid_mission = SpaceMission(
        mission_id="M2024_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        lauch_date=datetime.now(),
        duration_days=900,
        crew=crew_people,
        mission_status="planned",
        budget_millions=2500.0,
    )
    print("Space Mission Crew Validation")
    print("=========================================")
    print("Valid mission created:")
    print(f"Mission: {valid_mission.mission_name}")
    print(f"ID: {valid_mission.mission_id}")
    print(f"Destination: {valid_mission.destination}")
    print(f"Duration: {valid_mission.duration_days} days")
    print(f"Budget: {valid_mission.budget_millions}M")
    print(f"Crew size: {len(valid_mission.crew)}")
    print("Crew members:")
    for i, crew in enumerate(valid_mission.crew):
        print(
            f"{valid_mission.crew[i].name}"
            f"({valid_mission.crew[i].rank.name})- "
            f"{valid_mission.crew[i].specialization}"
        )
    print("\n=========================================")
    print("Expected validation errors")
    invalid_mission = None
    try:
        peter = CrewMember(
            member_id="32_acdf",
            name="Sarah Connor",
            rank=CrewRank.cadet,
            age=45,
            specialization="Mission command",
            years_experience=2,
            is_active=True,
        )
        elena = CrewMember(
            member_id="34_bfgd",
            name="John Smith",
            rank=CrewRank.lieutenant,
            age=32,
            specialization="Navigation",
            years_experience=2,
            is_active=True,
        )
        paul = CrewMember(
            member_id="568_rtfg",
            name="Alice Johnson",
            rank=CrewRank.commander,
            age=27,
            specialization="Engineering",
            years_experience=5,
            is_active=True,
        )
        crew_people = [peter, elena, paul]
        invalid_mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            lauch_date=datetime.now(),
            duration_days=900,
            crew=crew_people,
            mission_status="planned",
            budget_millions=2500.0,
        )
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"])
    if invalid_mission is not None:
        print("no mistakes detected for the second batch")


if __name__ == "__main__":
    main()
