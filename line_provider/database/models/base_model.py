from datetime import datetime
from decimal import Decimal
from typing import Annotated

from sqlalchemy import DateTime, Integer, Numeric
from sqlalchemy.orm import DeclarativeBase, mapped_column

dt = Annotated[datetime, mapped_column(DateTime())]
intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
numeric = Annotated[Decimal, mapped_column(Numeric(10, 2))]


class Base(DeclarativeBase):
    """Базовый класс моделей."""

    type_annotation_map = {dt: datetime, intpk: Integer, numeric: Numeric}
