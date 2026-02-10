from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models import Jockey
from src.data.repositories.base import BaseRepository


class JockeyRepository(BaseRepository[Jockey]):
    """Репозиторий для работы с жокеями"""

    def __init__(self, session: AsyncSession):
        super().__init__(Jockey, session)
