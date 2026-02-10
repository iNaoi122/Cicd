from typing import Optional

from src.business.dto.owner_dto import OwnerCreateDTO, OwnerDTO
from src.data.uow import UnitOfWork


async def create_owner(uow: UnitOfWork, data: OwnerCreateDTO) -> OwnerDTO:
    """
    Создать нового владельца

    Args:
        uow: Unit of Work
        data: Данные владельца

    Returns:
        OwnerDTO: Созданный владелец
    """
    async with uow:
        owner = await uow.owners.create(
            {"name": data.name, "address": data.address, "phone": data.phone}
        )
        await uow.commit()
        return OwnerDTO.model_validate(owner)


async def get_owner_by_id(uow: UnitOfWork, owner_id: int) -> Optional[OwnerDTO]:
    """
    Получить владельца по ID

    Args:
        uow: Unit of Work
        owner_id: ID владельца

    Returns:
        OwnerDTO или None
    """
    async with uow:
        owner = await uow.owners.get_by_id(owner_id)
        if not owner:
            return None
        return OwnerDTO.model_validate(owner)


async def list_owners(
    uow: UnitOfWork, skip: int = 0, limit: int = 100
) -> list[OwnerDTO]:
    """
    Получить список владельцев

    Args:
        uow: Unit of Work
        skip: Пропустить записей
        limit: Максимум записей

    Returns:
        Список OwnerDTO
    """
    async with uow:
        owners = await uow.owners.list(skip=skip, limit=limit)
        return [OwnerDTO.model_validate(o) for o in owners]
