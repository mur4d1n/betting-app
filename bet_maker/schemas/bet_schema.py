from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class PostBetSchema(BaseModel):
    event_id: int | str
    bet_sum: Annotated[Decimal, Field(gt=0, decimal_places=2)]

    @field_validator("bet_sum")
    @classmethod
    def validate_bet_sum(cls, v: Decimal) -> Decimal:
        if abs(v.as_tuple().exponent) > 2:
            raise ValueError(
                "bet_sum must contain not more than 2 decimal digits"
            )

        return v

    @field_validator("event_id")
    @classmethod
    def validate_event_id(cls, v: int | str) -> int | str:
        if isinstance(v, str):
            if not v.isdigit():
                raise ValueError(
                    "event_id must be an integer or string repr of an integer"
                )

        return v
