import logging

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.database.models import Bet, BetStatus
from bet_maker.schemas import PostBetSchema


async def add_bet(session: AsyncSession, schema: PostBetSchema) -> int:
    bet = Bet(
        event_id=schema.event_id, sum=schema.bet_sum, status=BetStatus.IN_PROGRESS
    )

    session.add(bet)

    await session.commit()

    return bet.id


async def get_bets(session: AsyncSession) -> list[dict]:
    stmt = select(Bet.id, Bet.status).select_from(Bet)

    result = await session.execute(stmt)

    return [dict(row) for row in result.mappings()]


async def update_bet_status(session: AsyncSession, event_id: int, status: int):
    logging.warning(f"event_id: {event_id}\nstatus: {status}")
    if status == 1:
        stmt = update(Bet).where(Bet.event_id == event_id).values(status=BetStatus.WIN)
    else:
        stmt = update(Bet).where(Bet.event_id == event_id).values(status=BetStatus.LOSE)

    await session.execute(stmt)
    await session.commit()
