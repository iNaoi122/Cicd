from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models import RaceParticipant
from src.data.repositories.base import BaseRepository


class ParticipantRepository(BaseRepository[RaceParticipant]):
    """Репозиторий для работы с участниками"""

    def __init__(self, session: AsyncSession):
        super().__init__(RaceParticipant, session)

    async def get_by_race_id(
        self, race_id: int, with_relations: bool = False
    ) -> List[RaceParticipant]:
        """Получить всех участников состязания"""
        query = select(RaceParticipant).where(RaceParticipant.race_id == race_id)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_by_race_and_pair(
        self, race_id: int, jockey_id: int, horse_id: int
    ) -> Optional[RaceParticipant]:
        """Проверить, участвует ли пара в состязании"""
        query = select(RaceParticipant).where(
            and_(
                RaceParticipant.race_id == race_id,
                RaceParticipant.jockey_id == jockey_id,
                RaceParticipant.horse_id == horse_id,
            )
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
