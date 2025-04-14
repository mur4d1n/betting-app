from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, field_validator


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
    state: Optional[EventState] = EventState.IN_PROGRESS
    coefficient: Optional[Decimal] = None
    deadline: Optional[datetime] = None

    @field_validator("coefficient")
    @classmethod
    def validate_coefficient(cls, v: Decimal) -> Decimal:
        if v is not None and v <= Decimal("1.00"):
            raise ValueError("Coefficient must be greater than 1.00")

        return v
