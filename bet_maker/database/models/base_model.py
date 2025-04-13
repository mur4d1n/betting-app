from decimal import Decimal
from typing import Annotated

from sqlalchemy import Integer, Numeric
from sqlalchemy.orm import DeclarativeBase, mapped_column

intpk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
numeric = Annotated[Decimal, mapped_column(Numeric(10, 2))]


class Base(DeclarativeBase):
    """Базовый класс моделей."""

    type_annotation_map = {
        intpk: Integer,
        numeric: Numeric
    }
