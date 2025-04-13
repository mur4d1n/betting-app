from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.database.repository.bet_crud import get_bets


class GetBetsService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_bets(self) -> list[dict]:
        return await get_bets(session=self._session)
