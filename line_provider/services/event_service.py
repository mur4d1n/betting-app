import json

from datetime import datetime

from fastapi import HTTPException, status
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from line_provider.database.repository.event_crud import (
    add_event,
    get_available_events,
    get_event,
    update_event,
)
from line_provider.schemas import PatchEventSchema, PostEventSchema
from line_provider.schemas.event_schemas import EventState


class EventService:
    def __init__(self, session: AsyncSession, redis: Redis):
        self._session = session
        self._redis = redis

    async def post_event(self, event: PostEventSchema):
        return await add_event(session=self._session, event=event)

    async def get_events(self):
        return await get_available_events(session=self._session)

    async def get_event(self, event_id: int):
        event = await get_event(session=self._session, event_id=event_id)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event with given id not found",
            )

        return event

    async def update_event(self, event_id: int, event_schema: PatchEventSchema):
        event = await get_event(session=self._session, event_id=event_id)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event with given id not found",
            )

        await update_event(
            session=self._session, event=event, event_schema=event_schema
        )

        if event_schema.state in (EventState.FIRST_WIN, EventState.SECOND_WIN):
            redis_data = {"event_id": event_id, "state": event_schema.state.value}

            await self._redis.xadd(
                name="events_stream",
                fields={
                    "data": json.dumps(redis_data),
                    "timestamp": str(datetime.utcnow()),
                },
                maxlen=1000,
            )

        return {"status": "OK"}
