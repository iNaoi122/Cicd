from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models import Horse
from src.data.repositories.base import BaseRepository


class HorseRepository(BaseRepository[Horse]):
    """Репозиторий для работы с лошадьми"""

    def __init__(self, session: AsyncSession):
        super().__init__(Horse, session)
