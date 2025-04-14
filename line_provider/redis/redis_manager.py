import contextlib

from typing import AsyncIterator

from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool

REDIS_URL = "redis://redis:6379/0"


class RedisTool:
    """Менеджер для управления соединением с Redis."""

    def __init__(self, url: str):
        """Создаём объект Redis."""

        self._connection_pool: ConnectionPool = ConnectionPool.from_url(
            url,
            health_check_interval=10,  # Проверка состояния соединения.
            socket_connect_timeout=5,  # Время на установление соединения.
            retry_on_timeout=True,  # Переподключение в случае тайм-аута.
            socket_keepalive=True,  # Поддерживание активного сокета.
        )

    async def close(self):
        """Закрываем соединение с Redis."""

        if self._connection_pool is None:
            raise Exception("Redis is not working.")

        await self._connection_pool.disconnect()

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[Redis]:
        """Создаём подключение к Redis."""

        redis: Redis = await Redis(connection_pool=self._connection_pool)
        try:
            yield redis
        except Exception as er:
            raise er
        finally:
            await redis.aclose()


# Создаём объект RedisTool с указанием URL.
redis_tool = RedisTool(url=REDIS_URL)


async def get_redis_session():
    """Создаём асинхронную сессию с подключением к Redis."""

    async with redis_tool.connect() as redis:
        yield redis
