from sqlalchemy.ext.asyncio import AsyncSession

from src.data.models import Owner
from src.data.repositories.base import BaseRepository


class OwnerRepository(BaseRepository[Owner]):
    """Репозиторий для работы с владельцами"""

    def __init__(self, session: AsyncSession):
        super().__init__(Owner, session)
