from pydantic import BaseModel, Field  # type: ignore
from typing import Optional
from datetime import date


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: date
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    try:
        valid_space = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2023-01-01",
            is_operational=True,
        )
    except ValueError as e:
        print(e)
    print(f"ID: {valid_space.station_id}")
    print(f"Name: {valid_space.name}")
    print(f"Crew:{valid_space.crew_size} people")
    print(f"Power: {valid_space.power_level}%")
    print(f"Oxygen:{valid_space.oxygen_level}%")
    print("Status:", end="")
    print(
        "Operational"
        if (valid_space.is_operational) is True
        else "Not Operational"
    )
    print("========================================")
    try:
        invalid_space = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=26,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance="2023-01-01",
            is_operational=True,
        )
        print(f"ID: {invalid_space.station_id}")
    except ValueError as e:
        print(e)


if __name__ == "__main__":
    main()
