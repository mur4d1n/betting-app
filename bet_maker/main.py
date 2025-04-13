from typing import Annotated

import uvicorn

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from bet_maker.dependencies import (
    get_bets_service,
    post_bet_service
)
from bet_maker.schemas import PostBetSchema
from bet_maker.services import (
    GetBetsService,
    PostBetService
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/events")
async def get_events():
    return 200


@app.post("/bet")
async def post_bet(schema: PostBetSchema, service: Annotated[PostBetService, Depends(post_bet_service)]):
    return await service.post_bet(bet_schema=schema)


@app.get("/bets")
async def get_bets(service: Annotated[GetBetsService, Depends(get_bets_service)]):
    return await service.get_bets()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
