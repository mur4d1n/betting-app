from fastapi import HTTPException, status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.database.repository.bet_crud import (
    add_bet,
    get_bets,
)
from bet_maker.schemas import PostBetSchema


class BetService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_bets(self) -> list[dict]:
        return await get_bets(session=self._session)

    async def post_bet(self, bet_schema: PostBetSchema) -> dict:
        async with AsyncClient() as client:
            response = await client.get(
                f"http://line_provider:8080/event/{bet_schema.event_id}"
            )

        if response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unknown event_id",
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Internal server error",
            )

        bet_id = await add_bet(session=self._session, schema=bet_schema)

        return {"bet_id": bet_id}
