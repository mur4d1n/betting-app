import json
import logging

from asyncio import sleep

from fastapi import HTTPException, status
from redis.asyncio import Redis, RedisError
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
        self._max_retries = 3
        self._retry_delay = 0.5
        self._logger = logging.getLogger(__name__)

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

            for attempt in range(1, self._max_retries + 1):
                try:
                    await self._redis.xadd(
                        name="events_stream",
                        fields={
                            "data": json.dumps(redis_data),
                        },
                        maxlen=1000,
                    )

                    break
                except RedisError as e:
                    self._logger.warning(f"Attempt {attempt}/{self._max_retries} failed: {str(e)}")
                    await sleep(self._retry_delay)
                except Exception as e:
                    self._logger.warning(f"Unexpected error: {str(e)}")

            self._logger.info(f"Event sent to Redis: {json.dumps(redis_data)}")

        return {"status": "OK"}
