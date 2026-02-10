from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from src.data.repositories import (
    HorseRepository,
    JockeyRepository,
    OwnerRepository,
    ParticipantRepository,
    RaceRepository,
)


class UnitOfWork:
    """
    Unit of Work паттерн для управления транзакциями
    Обеспечивает атомарность операций и управление репозиториями
    """

    def __init__(self, session: AsyncSession):
        self.session = session
        self._races: Optional[RaceRepository] = None
        self._jockeys: Optional[JockeyRepository] = None
        self._horses: Optional[HorseRepository] = None
        self._owners: Optional[OwnerRepository] = None
        self._participants: Optional[ParticipantRepository] = None

    @property
    def races(self) -> RaceRepository:
        if self._races is None:
            self._races = RaceRepository(self.session)
        return self._races

    @property
    def jockeys(self) -> JockeyRepository:
        if self._jockeys is None:
            self._jockeys = JockeyRepository(self.session)
        return self._jockeys

    @property
    def horses(self) -> HorseRepository:
        if self._horses is None:
            self._horses = HorseRepository(self.session)
        return self._horses

    @property
    def owners(self) -> OwnerRepository:
        if self._owners is None:
            self._owners = OwnerRepository(self.session)
        return self._owners

    @property
    def participants(self) -> ParticipantRepository:
        if self._participants is None:
            self._participants = ParticipantRepository(self.session)
        return self._participants

    async def commit(self):
        """Зафиксировать транзакцию"""
        await self.session.commit()

    async def rollback(self):
        """Откатить транзакцию"""
        await self.session.rollback()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.rollback()
        await self.session.close()
