from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, field_validator


class PostBetSchema(BaseModel):
    event_id: int | str
    bet_sum: Annotated[
        Decimal,
        Field(gt=0, decimal_places=2)
    ]

    # TODO: научить модель принимать числа типа 10.00, 1.10 и т.д.
    @field_validator("bet_sum")
    @classmethod
    def validate_bet_sum(cls, v: Decimal) -> Decimal:
        if abs(v.as_tuple().exponent) != 2:
            raise ValueError("bet_sum must contain exactly 2 decimal digits (e.g. 10.00)")

        return v

    @field_validator("event_id")
    @classmethod
    def validate_event_id(cls, v: int | str) -> int | str:
        """
        Не уточнил, должен ли event_id в строковом виде быть представлением числа,
        так что на всякий случай оставил тут код валидатора
        """

        # if type(v) == str:
        #     if not v.isdigit():
        #         raise ValueError("event_id must be an integer or string repr of an integer")

        return v
