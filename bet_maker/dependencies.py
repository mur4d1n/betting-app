from typing import Type, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from bet_maker.database import get_session
from bet_maker.services import (
    GetBetsService,
    PostBetService,
)

# Для определения типа по мере выполнения.
T = TypeVar("T")


class ServiceFactory:
    """Сервис-фабрика."""

    def __init__(self, service_class: Type[T]):
        """Инициируем фабрику с сервисом на вход."""
        self.service_class = service_class

    async def __call__(self) -> T:
        """Создаём сервис без зависимостей."""
        return self.service_class()


class ServiceDBFactory:
    """Сервис-фабрика с прокидыванием сессии БД."""

    def __init__(self, service_class: Type[T]):
        """Инициируем фабрику с сервисом на вход."""
        self.service_class = service_class

    async def __call__(
        self,
        session: AsyncSession = Depends(get_session),
    ) -> T:
        """Объявление зависимостей - БД."""
        return self.service_class(session)


get_bets_service = ServiceDBFactory(GetBetsService)
post_bet_service = ServiceDBFactory(PostBetService)
