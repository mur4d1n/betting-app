from enum import Enum

from sqlalchemy.orm import Mapped

from .base_model import Base, datetime, intpk, numeric


class EventState(Enum):
    IN_PROGRESS = 0
    FIRST_WIN = 1
    SECOND_WIN = 2


class Event(Base):
    __tablename__ = "event"

    id: Mapped[intpk]
    state: Mapped[EventState]
    coefficient: Mapped[numeric]
    deadline: Mapped[datetime]
