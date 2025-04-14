import asyncio
import logging

from contextlib import asynccontextmanager
from typing import Annotated

import uvicorn

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bet_maker.dependencies import (
    bet_service,
    get_events_service,
)
from bet_maker.schemas import PostBetSchema
from bet_maker.services import (
    BetService,
    GetEventsService,
)

from bet_maker.redis_consumer import EventConsumer


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(event_consumer.consume_events())

    yield

    await event_consumer.close()


event_consumer = EventConsumer()
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/events")
async def get_events(service: Annotated[GetEventsService, Depends(get_events_service)]):
    return await service.get_events()


@app.post("/bet")
async def post_bet(
    schema: PostBetSchema, service: Annotated[BetService, Depends(bet_service)]
):
    return await service.post_bet(bet_schema=schema)


@app.get("/bets")
async def get_bets(service: Annotated[BetService, Depends(bet_service)]):
    return await service.get_bets()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
