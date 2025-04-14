from typing import Annotated

import uvicorn

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from line_provider.dependencies import event_service
from line_provider.schemas import (
    PatchEventSchema,
    PostEventSchema,
)
from line_provider.services import (
    EventService,
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/event")
async def post_event(
    schema: PostEventSchema, service: Annotated[EventService, Depends(event_service)]
):
    return await service.post_event(event=schema)


@app.get("/event")
async def get_events(service: Annotated[EventService, Depends(event_service)]):
    return await service.get_events()


@app.get("/event/{event_id}")
async def get_event(
    service: Annotated[EventService, Depends(event_service)], event_id: int
):
    return await service.get_event(event_id=event_id)


@app.patch("/event/{event_id}")
async def patch_event(
    service: Annotated[EventService, Depends(event_service)],
    event_id: int,
    event_schema: PatchEventSchema,
):
    return await service.update_event(event_id=event_id, event_schema=event_schema)


@app.get("/health")
async def healthcheck():
    return 200


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
