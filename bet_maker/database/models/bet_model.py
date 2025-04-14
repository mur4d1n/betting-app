from enum import Enum

from sqlalchemy.orm import Mapped

from .base_model import Base, intpk, numeric


class BetStatus(Enum):
    IN_PROGRESS = -1
    WIN = 1
    LOSE = 0


class Bet(Base):
    __tablename__ = "bet_model"

    id: Mapped[intpk]
    event_id: Mapped[int]
    sum: Mapped[numeric]
    status: Mapped[BetStatus]
