from fastapi import HTTPException, status
from httpx import AsyncClient


class GetEventsService:
    def __init__(self):
        pass

    async def get_events(self):
        async with AsyncClient() as client:
            result = await client.get("http://line_provider:8080/event")

        if result.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

        return result.json()
