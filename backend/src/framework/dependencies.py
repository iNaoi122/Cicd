from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.data.database import async_session_maker
from src.data.uow import UnitOfWork


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получить сессию БД"""
    async with async_session_maker() as session:
        yield session


async def get_uow(session: AsyncSession) -> UnitOfWork:
    """Получить Unit of Work"""
    return UnitOfWork(session)
