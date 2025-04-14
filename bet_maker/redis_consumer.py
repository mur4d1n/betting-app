import asyncio
import json
import logging

from redis.asyncio import Redis

from bet_maker.database import get_session
from bet_maker.database.repository.bet_crud import update_bet_status


class EventConsumer:
    def __init__(self):
        self._redis = Redis(host="redis", port=6379)
        self._logger = logging.getLogger(__name__)

    async def close(self):
        await self._redis.close()

    async def consume_events(self):
        last_id = "$"

        while True:
            try:
                response = await self._redis.xread(
                    streams={"events_stream": last_id},
                    count=10,
                    block=5000,
                )

                if not response:
                    continue

                for stream in response:
                    stream_name, messages = stream

                    for message_id, message_data in messages:
                        self._logger.info(f"New event: {message_data[b'data'].decode()}")

                        last_id = message_id
                        event_data = json.loads(message_data[b"data"].decode())
                        await self.process_event(event_data=event_data)

            except Exception as e:
                self._logger.warning(f"Error while processing event: {e}")
                await asyncio.sleep(5)

    async def process_event(self, event_data: dict):
        async for session in get_session():
            event_id = event_data.get("event_id")

            await update_bet_status(
                session=session, event_id=event_id, status=event_data.get("state")
            )
