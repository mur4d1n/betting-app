from typing import Type, TypeVar

from fastapi import Depends
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from line_provider.database.db_manager import get_session
from line_provider.redis.redis_manager import get_redis_session
from line_provider.services import (
    EventService,
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


class ServiceDBRedisFactory:
    """Сервис-фабрика с прокидыванием сессий БД и Redis."""

    def __init__(self, service_class: Type[T]):
        """Инициируем фабрику с сервисом на вход."""
        self.service_class = service_class

    async def __call__(
        self,
        session: AsyncSession = Depends(get_session),
        redis: Redis = Depends(get_redis_session),
    ) -> T:
        """Объявление зависимостей - БД и Redis."""
        return self.service_class(session, redis)


event_service = ServiceDBRedisFactory(EventService)
