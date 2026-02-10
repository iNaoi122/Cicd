from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.data.models import Race, RaceParticipant
from src.data.repositories.base import BaseRepository


class RaceRepository(BaseRepository[Race]):
    """Репозиторий для работы с состязаниями"""

    def __init__(self, session: AsyncSession):
        super().__init__(Race, session)

    async def get_by_jockey_id(self, jockey_id: int) -> List[Race]:
        """
        Получить все состязания, в которых участвовал жокей
        Функция 6 из ТЗ
        """
        query = (
            select(Race)
            .join(Race.participants)
            .where(RaceParticipant.jockey_id == jockey_id)
            .order_by(Race.date.desc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().unique().all())

    async def get_by_horse_id(self, horse_id: int) -> List[Race]:
        """
        Получить все состязания, в которых участвовала лошадь
        Функция 7 из ТЗ
        """
        query = (
            select(Race)
            .join(Race.participants)
            .where(RaceParticipant.horse_id == horse_id)
            .order_by(Race.date.desc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().unique().all())

    async def get_with_participants(self, race_id: int) -> Optional[Race]:
        """
        Получить состязание со всеми участниками
        Функция 1 из ТЗ
        """
        query = (
            select(Race)
            .where(Race.id == race_id)
            .options(
                selectinload(Race.participants).selectinload(RaceParticipant.jockey),
                selectinload(Race.participants).selectinload(RaceParticipant.horse),
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
