from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from line_provider.database.models import Event, EventState
from line_provider.schemas import PatchEventSchema, PostEventSchema


async def get_event(session: AsyncSession, event_id: int) -> Event:
    stmt = select(Event).where(Event.id == event_id)

    return await session.scalar(stmt)


async def get_available_events(session: AsyncSession) -> list[Event]:
    stmt = select(Event).where(Event.deadline >= datetime.utcnow())

    result = await session.scalars(stmt)

    return list(result)


async def add_event(session: AsyncSession, event: PostEventSchema):
    event = Event(
        id=event.event_id,
        state=EventState.IN_PROGRESS,
        coefficient=event.coefficient,
        deadline=event.deadline,
    )

    session.add(event)

    await session.commit()

    return event.id


async def update_event(
    session: AsyncSession, event: Event, event_schema: PatchEventSchema
):
    deadline = event.deadline if not event_schema.deadline else event_schema.deadline
    coefficient = (
        event.coefficient if not event_schema.coefficient else event_schema.coefficient
    )
    state = (
        event.state if not event_schema.state else EventState(event_schema.state.value)
    )

    event.deadline = deadline
    event.coefficient = coefficient
    event.state = state

    await session.commit()
