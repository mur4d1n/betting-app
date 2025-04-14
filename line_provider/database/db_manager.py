import contextlib
from typing import AsyncIterator

from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


DB_URL = "postgresql+asyncpg://line_provider_user:password@database_line_provider:5432/line_provider"

# Создаём движок и фабрику сессий.
engine = create_async_engine(url=DB_URL, poolclass=NullPool)
session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)


@contextlib.asynccontextmanager
async def init_session() -> AsyncIterator[AsyncSession]:
    """Создаем и возвращаем сессию для работы с БД."""
    session: AsyncSession = session_factory()
    try:
        yield session
    except Exception as error:
        await session.rollback()
        raise error
    finally:
        await session.close()


async def close_engine() -> None:
    """Закрываем соединение с БД."""
    await engine.dispose()


async def get_session() -> AsyncIterator[AsyncSession]:
    """Создаем сессию для работы с БД."""
    async with init_session() as session:
        yield session
