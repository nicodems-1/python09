from pydantic import BaseModel, Field, model_validator, ValidationError
from datetime import datetime
from typing import Optional
from typing_extensions import Self
from enum import Enum


class ContactTypes(Enum):
    radio = 1
    physical = 3
    telepathic = 4
    visual = 2


class BaseStation(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactTypes
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def custom_validation(self) -> Self:
        if self.contact_id.startswith("AC") is not True:
            raise ValueError("Contact ID must start with 'AC'(Alien Contact)")
        if self.contact_type == ContactTypes.physical and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (
            self.contact_type == ContactTypes.telepathic
            and self.witness_count < 3
        ):
            raise ValueError("Telepathic contact require at least 3 witnesses")
        if self.signal_strength > 7.0 and self.message_received is None:
            raise ValueError(
                "Strong signals (> 7.0) should include received messages"
            )
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")
    try:
        valid = BaseStation(
            contact_id="AC_2024-001",
            timestamp=datetime.now(),
            contact_type=ContactTypes.radio,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="'Greetings from Zeta Reticuli'",
        )
    except ValueError as e:
        print(e)
    print("Valid contact report:")
    print(f"ID: {valid.contact_id}")
    print(f"Type: {valid.contact_type.name}")
    print(f"Location: {valid.location}")
    print(f"Signal: {valid.signal_strength}/10")
    print(f"Duration: {valid.duration_minutes} minutes")
    print(f"Witnesses: {valid.witness_count}")
    print(f"Message: {valid.message_received}")
    print("\n======================================")
    invalid = None
    print("Expected validation error:")
    try:
        invalid = BaseStation(
            contact_id="AC_2024-001",
            timestamp=datetime.now(),
            contact_type=ContactTypes.telepathic,
            location="Area 51, Nevada",
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli",
        )
    except ValidationError as e:
        for error in e.errors():
            print(error["msg"].replace("Value error, ", ""))
    if invalid is not None:
        print("no mistakes detected for the second batch")


if __name__ == "__main__":
    main()
