from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator, model_validator, ValidationInfo


class EventState(Enum):
    IN_PROGRESS = 0
    FIRST_WIN = 1
    SECOND_WIN = 2


class PostEventSchema(BaseModel):
    event_id: int
    coefficient: Decimal
    deadline: datetime

    @field_validator("coefficient")
    @classmethod
    def validate_coefficient(cls, v: Decimal) -> Decimal:
        if v is not None and v <= Decimal("1.00"):
            raise ValueError("Coefficient must be greater than 1.00")

        return v


class PatchEventSchema(BaseModel):
    state: Optional[EventState] = None
    coefficient: Optional[Decimal] = None
    deadline: Optional[datetime] = None

    @field_validator("coefficient")
    @classmethod
    def validate_coefficient(cls, v: Decimal) -> Decimal:
        if v is not None and v <= Decimal("1.00"):
            raise ValueError("Coefficient must be greater than 1.00")

        return v


    @model_validator(mode="before")
    def check_at_least_one(cls, data: dict):
        if all(data.get(value) is None for value in data.keys()):
            raise ValueError("At least one field must be provided")

        return data
