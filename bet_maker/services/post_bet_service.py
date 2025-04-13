from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.database.repository.bet_crud import add_bet
from bet_maker.schemas import PostBetSchema


class PostBetService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def post_bet(self, bet_schema: PostBetSchema) -> dict:
        bet_id = await add_bet(session=self._session, schema=bet_schema)

        return {"bet_id": bet_id}
